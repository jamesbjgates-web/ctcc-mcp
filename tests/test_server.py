"""Unit tests for the CTCC MCP Server."""

import unittest
import json
from unittest.mock import patch, MagicMock
from ctcc_mcp.server import (
    handle_jsonrpc,
    query_ctcc,
    format_ctcc_result,
    TOOL_DEFINITION,
    SERVER_NAME,
    SERVER_VERSION
)


class TestCTCCMCPServer(unittest.TestCase):

    def test_tool_definition(self):
        """Verifies tool definition conforms to MCP tool schema."""
        self.assertEqual(TOOL_DEFINITION["name"], "check_token_control")
        schema = TOOL_DEFINITION["inputSchema"]
        self.assertEqual(schema["type"], "object")
        self.assertIn("contract_address", schema["properties"])
        self.assertIn("payment_signature", schema["properties"])
        self.assertEqual(schema["required"], ["contract_address"])

    def test_invalid_contract_address(self):
        """Verifies validation catches invalid address formats."""
        res = query_ctcc("0xInvalidShort")
        self.assertEqual(res["status_code"], 400)
        self.assertTrue(res["is_error"])
        self.assertIn("Invalid Ethereum/Base address", res["error"])

    def test_jsonrpc_initialize(self):
        """Verifies MCP initialize handshake."""
        req = {
            "jsonrpc": "2.0",
            "id": 101,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "cursor", "version": "1.0"}
            }
        }
        resp = handle_jsonrpc(req)
        self.assertEqual(resp["id"], 101)
        self.assertEqual(resp["result"]["protocolVersion"], "2024-11-05")
        self.assertEqual(resp["result"]["serverInfo"]["name"], SERVER_NAME)
        self.assertEqual(resp["result"]["serverInfo"]["version"], SERVER_VERSION)
        self.assertIn("tools", resp["result"]["capabilities"])

    def test_jsonrpc_tools_list(self):
        """Verifies tools/list returns check_token_control."""
        req = {
            "jsonrpc": "2.0",
            "id": 102,
            "method": "tools/list",
            "params": {}
        }
        resp = handle_jsonrpc(req)
        self.assertEqual(resp["id"], 102)
        tools = resp["result"]["tools"]
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["name"], "check_token_control")

    def test_jsonrpc_unknown_tool(self):
        """Verifies error on unknown tool call."""
        req = {
            "jsonrpc": "2.0",
            "id": 103,
            "method": "tools/call",
            "params": {
                "name": "non_existent_tool",
                "arguments": {}
            }
        }
        resp = handle_jsonrpc(req)
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32601)

    def test_format_ctcc_result_200(self):
        """Verifies formatting of 200 OK observations."""
        mock_res = {
            "status_code": 200,
            "payment_response": "eyJyZXN1bHQiOiJzdWNjZXNzIn0=",
            "data": {
                "timestamp": "2026-11-22T20:00:00Z",
                "observations": {
                    "has_code": True,
                    "bytecode_length_bytes": 1024,
                    "erc20": {
                        "is_erc20": True,
                        "name": "USD Coin",
                        "symbol": "USDC",
                        "decimals": 6,
                        "total_supply": "1000000000000"
                    },
                    "authority": {
                        "has_owner": True,
                        "owner": "0x1234567890123456789012345678901234567890",
                        "is_paused": False
                    },
                    "proxy": {
                        "is_proxy": False,
                        "implementation_address": None,
                        "beacon_address": None
                    }
                }
            }
        }
        text, is_err = format_ctcc_result(mock_res, "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
        self.assertFalse(is_err)
        self.assertIn("200 OK", text)
        self.assertIn("USD Coin", text)
        self.assertIn("Bytecode", text)
        self.assertIn("Owner/Admin Identified", text)

    def test_format_ctcc_result_402(self):
        """Verifies formatting of 402 challenge."""
        mock_res = {
            "status_code": 402,
            "payment_required_header": "raw_header_value",
            "decoded_challenge": {
                "accepts": [
                    {
                        "network": "eip155:8453",
                        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                        "amount": "10000",
                        "payTo": "0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75"
                    }
                ]
            }
        }
        text, is_err = format_ctcc_result(mock_res, "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
        self.assertFalse(is_err)
        self.assertIn("HTTP 402 Payment Required", text)
        self.assertIn("0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75", text)
        self.assertIn("eip155:8453", text)
        self.assertIn("10000", text)

    def test_live_402_challenge_execution(self):
        """Tests live query against cinqueport.net endpoint returns real 402 challenge."""
        res = query_ctcc("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
        self.assertEqual(res["status_code"], 402)
        self.assertIsNotNone(res.get("payment_required_header"))
        challenge = res.get("decoded_challenge")
        self.assertIsInstance(challenge, dict)
        accepts = challenge.get("accepts", [])
        self.assertGreaterEqual(len(accepts), 1)
        self.assertEqual(accepts[0].get("network"), "eip155:8453")
        self.assertEqual(accepts[0].get("amount"), "10000")
        self.assertEqual(accepts[0].get("payTo").lower(), "0x14d4035290a31b81e99e2dee26ef0a10e5aa4d75".lower())
        
        # Verify extensions.bazaar metadata from live endpoint
        extensions = challenge.get("extensions", {})
        self.assertIn("bazaar", extensions)
        bazaar_info = extensions["bazaar"].get("info", {})
        self.assertEqual(bazaar_info.get("name"), "Cinqueport Token Control Check (CTCC™)")
        self.assertEqual(bazaar_info.get("sampleInput", {}).get("contract_address"), "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")


if __name__ == "__main__":
    unittest.main()
