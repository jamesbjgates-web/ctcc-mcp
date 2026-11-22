#!/usr/bin/env python3
"""Cinqueport Token Control Check (CTCC™) MCP Server.

Provides the `check_token_control` tool to LLM agents for deterministic
smart-contract control inspection on Base Mainnet (eip155:8453), with
support for x402 v2 payment challenge inspection and paid execution.

Standard: Model Context Protocol (MCP) 2024-11-05
Transport: stdio (JSON-RPC 2.0)
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Tuple

DEFAULT_ENDPOINT = "https://cinqueport.net/check"
SERVER_NAME = "cinqueport-ctcc"
SERVER_VERSION = "1.0.0"

TOOL_DEFINITION = {
    "name": "check_token_control",
    "description": (
        "Inspects a Base Mainnet (eip155:8453) smart contract address for deterministic "
        "authority and control markers via CTCC™ (Cinqueport Token Control Check). "
        "Verifies bytecode existence, ERC-20 metadata, admin/owner presence, pause state, "
        "and EIP-1967 proxy implementation pointers. Returns structured observations without "
        "subjective risk scoring. Supports both 402 payment challenge inspection and paid execution "
        "via x402 v2 protocol ($0.01 USDC on Base Mainnet)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "contract_address": {
                "type": "string",
                "description": (
                    "Hex-encoded Base Mainnet contract address to inspect "
                    "(e.g., '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913' for canonical USDC)."
                )
            },
            "payment_signature": {
                "type": "string",
                "description": (
                    "Optional Base64-encoded x402 v2 PAYMENT-SIGNATURE header. "
                    "If omitted, CTCC returns the HTTP 402 Payment Required challenge "
                    "specifying the settlement requirements ($0.01 USDC on Base Mainnet to "
                    "0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75)."
                )
            }
        },
        "required": ["contract_address"]
    }
}


def log_debug(msg: str) -> None:
    """Logs internal diagnostics to stderr so stdio JSON-RPC remains untouched."""
    sys.stderr.write(f"[{SERVER_NAME}] {msg}\n")
    sys.stderr.flush()


def query_ctcc(contract_address: str, payment_signature: Optional[str] = None) -> Dict[str, Any]:
    """Calls the CTCC endpoint, returning a structured result dict."""
    endpoint = os.getenv("CTCC_ENDPOINT") or DEFAULT_ENDPOINT
    
    # Basic validation
    clean_addr = contract_address.strip()
    if not (clean_addr.startswith("0x") and len(clean_addr) == 42):
        return {
            "status_code": 400,
            "error": "Invalid Ethereum/Base address format. Expected 42-char 0x-prefixed hex string.",
            "is_error": True
        }

    payload = json.dumps({"contract_address": clean_addr}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": f"CTCC-MCP-Server/{SERVER_VERSION}"
    }
    if payment_signature:
        headers["PAYMENT-SIGNATURE"] = payment_signature.strip()

    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            status_code = resp.getcode()
            body = resp.read().decode("utf-8")
            data = json.loads(body) if body else {}
            payment_response = resp.headers.get("PAYMENT-RESPONSE")
            return {
                "status_code": status_code,
                "data": data,
                "payment_response": payment_response,
                "is_error": False
            }
    except urllib.error.HTTPError as e:
        status_code = e.code
        body = e.read().decode("utf-8")
        try:
            data = json.loads(body)
        except Exception:
            data = {"raw_body": body}

        payment_required = e.headers.get("PAYMENT-REQUIRED")
        decoded_challenge = None
        if payment_required:
            try:
                decoded_challenge = json.loads(base64.b64decode(payment_required).decode("utf-8"))
            except Exception:
                decoded_challenge = payment_required

        return {
            "status_code": status_code,
            "data": data,
            "payment_required_header": payment_required,
            "decoded_challenge": decoded_challenge,
            "is_error": status_code != 402  # 402 is an expected protocol challenge, not a hard system error
        }
    except Exception as e:
        log_debug(f"Network error querying CTCC: {e}")
        return {
            "status_code": 500,
            "error": f"Failed to connect to CTCC endpoint ({endpoint}): {str(e)}",
            "is_error": True
        }


def format_ctcc_result(res: Dict[str, Any], contract_address: str) -> Tuple[str, bool]:
    """Formats the CTCC output into a clean, human & model readable string."""
    status = res.get("status_code", 500)
    
    if status == 200:
        data = res.get("data", {})
        lines = [
            f"### CTCC™ Smart-Contract Control Report: {contract_address}",
            "**Status**: 200 OK (Settled & Verified)",
            "**Network**: Base Mainnet (eip155:8453)",
            f"**Timestamp**: {data.get('timestamp', 'N/A')}",
            ""
        ]
        if res.get("payment_response"):
            lines.append(f"**x402 Facilitator Settlement**: Verified (PAYMENT-RESPONSE present)")
            lines.append("")

        obs = data.get("observations", {})
        lines.append("#### Deterministic Observations")
        lines.append(f"- **Contract Bytecode**: {'Found' if obs.get('has_code') else 'No bytecode (EOA / empty)'} ({obs.get('bytecode_length_bytes', 0)} bytes)")
        
        erc20 = obs.get("erc20", {})
        if erc20.get("is_erc20"):
            lines.append(f"- **ERC-20 Token**: Yes — Name: `{erc20.get('name')}`, Symbol: `{erc20.get('symbol')}`, Decimals: `{erc20.get('decimals')}`, Total Supply: `{erc20.get('total_supply')}`")
        else:
            lines.append("- **ERC-20 Signals**: No ERC-20 standard methods detected")

        auth = obs.get("authority", {})
        lines.append(f"- **Owner/Admin Identified**: {'Yes (' + str(auth.get('owner')) + ')' if auth.get('has_owner') else 'No public owner/admin accessor found'}")
        lines.append(f"- **Pause State**: {'Paused / Pausable' if auth.get('is_paused') else 'Unpaused / No public pause accessor'}")

        proxy = obs.get("proxy", {})
        lines.append(f"- **EIP-1967 Proxy**: {'Yes — Implementation: ' + str(proxy.get('implementation_address')) if proxy.get('is_proxy') else 'None (Direct implementation)'}")
        if proxy.get("beacon_address"):
            lines.append(f"- **Beacon Pointer**: `{proxy.get('beacon_address')}`")

        lines.append("")
        lines.append("#### Raw Evidence JSON")
        lines.append("```json")
        lines.append(json.dumps(data, indent=2))
        lines.append("```")
        return "\n".join(lines), False

    elif status == 402:
        data = res.get("data", {})
        challenge = res.get("decoded_challenge") or {}
        accepts = challenge.get("accepts", [{}])[0] if isinstance(challenge, dict) else {}
        raw_header = res.get("payment_required_header", "")

        lines = [
            f"### CTCC™ x402 v2 Payment Challenge (HTTP 402 Payment Required)",
            f"**Target Contract**: `{contract_address}`",
            "**Protocol**: x402 v2 (Micro-settlement for autonomous machine due diligence)",
            "",
            "#### Settlement Requirements",
            f"- **Network**: {accepts.get('network', 'eip155:8453')} (Base Mainnet)",
            f"- **Asset**: Canonical USDC (`{accepts.get('asset', '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')}`)",
            f"- **Amount**: $0.01 USDC (`{accepts.get('amount', '10000')}` atomic units)",
            f"- **Pay To (Beneficiary)**: `{accepts.get('payTo', '0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75')}`",
            "",
            "#### How to Execute Settlement",
            "To execute this check and receive the verified control observations:",
            "1. Sign an EIP-3009 transfer authorization or EIP-712 permit for 10000 atomic USDC on Base to `0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75`.",
            "2. Base64-encode the signed payload matching the x402 v2 `PAYMENT-SIGNATURE` specification.",
            "3. Call `check_token_control` again providing the `payment_signature` argument.",
            "",
            "#### Raw Challenge Header (PAYMENT-REQUIRED)",
            f"`{raw_header}`",
            "",
            "#### Service Discovery",
            "- OpenAPI: https://cinqueport.net/openapi.json",
            "- Descriptor: https://cinqueport.net/ctcc.json",
            "- Manifest: https://cinqueport.net/.well-known/x402.json"
        ]
        return "\n".join(lines), False

    else:
        err_msg = res.get("error") or res.get("data", {}).get("error") or f"HTTP {status}"
        return f"CTCC Error ({status}): {err_msg}", True


def handle_jsonrpc(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handles an incoming JSON-RPC 2.0 request according to MCP 2024-11-05."""
    method = req.get("method")
    req_id = req.get("id")
    params = req.get("params", {})

    log_debug(f"Handling method: {method} (id={req_id})")

    # Notifications (no response required)
    if method == "notifications/initialized":
        log_debug("Client initialized notification received.")
        return None

    if req_id is None:
        return None

    # MCP Methods
    if method == "initialize":
        client_info = params.get("clientInfo", {})
        log_debug(f"Initialize from client: {client_info.get('name')} {client_info.get('version')}")
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                }
            }
        }

    elif method == "ping":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {}
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [TOOL_DEFINITION]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name != "check_token_control":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method/Tool '{tool_name}' not found"
                }
            }

        addr = args.get("contract_address", "")
        sig = args.get("payment_signature")
        result = query_ctcc(addr, sig)
        text_content, is_error = format_ctcc_result(result, addr)

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": text_content
                    }
                ],
                "isError": is_error
            }
        }

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not implemented"
            }
        }


def run_stdio_server() -> None:
    """Runs the main stdio loop reading JSON-RPC lines from stdin."""
    log_debug(f"Starting CTCC MCP Server v{SERVER_VERSION} on stdio...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
            continue

        resp = handle_jsonrpc(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


def main() -> None:
    """Entrypoint supporting both CLI test queries and MCP stdio loop."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ("--help", "-h"):
            print("CTCC™ MCP Server")
            print("Usage:")
            print("  python3 -m ctcc_mcp.server             # Run stdio MCP server (for Claude Desktop, Cursor, etc.)")
            print("  python3 -m ctcc_mcp.server --check <addr> [signature]  # Run direct test against CTCC endpoint")
            print("  python3 -m ctcc_mcp.server --version   # Display version")
            sys.exit(0)
        elif sys.argv[1] in ("--version", "-v"):
            print(f"CTCC MCP Server v{SERVER_VERSION}")
            sys.exit(0)
        elif sys.argv[1] == "--check":
            if len(sys.argv) < 3:
                print("Error: --check requires a contract address argument.")
                sys.exit(1)
            target = sys.argv[2]
            sig = sys.argv[3] if len(sys.argv) > 3 else None
            res = query_ctcc(target, sig)
            formatted, is_err = format_ctcc_result(res, target)
            print(formatted)
            sys.exit(1 if is_err else 0)

    run_stdio_server()


if __name__ == "__main__":
    main()
