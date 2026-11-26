# CTCC™ MCP Server (`ctcc-mcp`)

**Deterministic Smart-Contract Authority & Control Inspection for AI Agents on Base Mainnet.**

`ctcc-mcp` is an official [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server wrapper for **CTCC™ (Cinqueport Token Control Check)**, developed by [Cinqueport](https://cinqueport.net), the specialist international trade and evidential due-diligence division of **Pavilion (Stockport) Ltd** (`pspt.ltd`).

---

## Overview

As autonomous AI agents execute treasury operations, swap assets, and interact with smart contracts on **Base Mainnet (eip155:8453)**, retail "risk scores" and crowd-sourced badges fail to provide corporate-grade protection. A score of 95/100 does not prevent a developer pause function or an unannounced implementation upgrade from freezing company funds.

`ctcc-mcp` gives LLMs and autonomous agents deterministic structural observations directly from the blockchain before corporate capital is committed:
- **Contract Bytecode**: Existence and bytecode length in bytes (detects unverified addresses and EOAs).
- **ERC-20 Metadata**: Confirms standard methods (`name`, `symbol`, `decimals`, `totalSupply`).
- **Authority & Governance**: Identifies active `owner()` / `admin()` addresses.
- **Circuit Breakers**: Verifies active `paused()` states.
- **Proxy Architecture**: Detects EIP-1967 proxy implementation slots and beacon pointers.

CTCC returns **factual structural observations** rather than subjective "safe/scam" advice. Calling agents apply their own internal governance policies to the returned JSON facts.

---

## Micro-Settlement via x402 v2 Protocol

CTCC operates on a zero-signup, pay-per-check model:
- **Network**: Base Mainnet (`eip155:8453`)
- **Asset**: Canonical USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Price**: $0.01 USDC (`10000` atomic units) per check
- **Settlement Beneficiary**: `0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75`
- **Protocol**: HTTP 402 Payment Required (`x402 v2`)

When invoked without payment, `check_token_control` returns the raw HTTP 402 challenge specifying the exact parameters required for settlement. Agents equipped with an on-chain wallet sign an EIP-3009 transfer authorization, pass the Base64 `payment_signature`, and receive settled deterministic evidence in milliseconds.

---

## Exposed MCP Tools

### `check_token_control`
Inspects a Base Mainnet smart contract address for deterministic control and authority markers.

#### Arguments:
| Argument | Type | Required | Description |
|---|---|---|---|
| `contract_address` | string | **Yes** | 42-character 0x-prefixed hex address on Base Mainnet (e.g. `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`). |
| `payment_signature` | string | No | Optional Base64-encoded x402 v2 `PAYMENT-SIGNATURE` header. When omitted, returns the HTTP 402 payment requirements. |

---

## Installation & Configuration

### 1. Claude Desktop
Add `ctcc-mcp` to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ctcc": {
      "command": "python3",
      "args": ["-m", "ctcc_mcp.server"],
      "cwd": "/path/to/ctcc-mcp"
    }
  }
}
```

### 2. Cursor IDE
Add to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ctcc": {
      "command": "python3",
      "args": ["-m", "ctcc_mcp.server"],
      "cwd": "${workspaceFolder}/ctcc-mcp"
    }
  }
}
```

### 3. Smithery
Install directly via Smithery CLI:

```bash
npx -y @smithery/cli install ctcc-mcp --client claude
```

### 4. Official MCP Registry
`ctcc-mcp` is published to the official [Model Context Protocol Registry](https://registry.modelcontextprotocol.io) under the namespace:
```
io.github.jamesbjgates-web/ctcc-mcp
```

### 5. Docker Container
Build and run the lightweight container:

```bash
docker build -t ctcc-mcp .
docker run -i --rm ctcc-mcp
```

### 6. Direct CLI Smoke Testing
You can inspect any contract or test the x402 payment challenge directly from your shell without running an MCP client:

```bash
# Test USDC canonical contract challenge
python3 -m ctcc_mcp.server --check 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

---

## Machine Discovery Endpoints

CTCC is natively indexed and discoverable across the autonomous agent ecosystem:
- **Production API**: `POST https://cinqueport.net/check`
- **OpenAPI 3.1 Specification**: `https://cinqueport.net/openapi.json`
- **AI Plugin Manifest**: `https://cinqueport.net/.well-known/ai-plugin.json`
- **x402 Protocol Manifest**: `https://cinqueport.net/.well-known/x402.json`
- **CTCC Machine Descriptor**: `https://cinqueport.net/ctcc.json`
- **LLM Context Descriptor**: `https://cinqueport.net/llms.txt`

## Official SDKs & Agent Discovery

- **Python SDK:** [`ctcc-x402`](https://pypi.org/project/ctcc-x402/) (`pip install ctcc-x402`)
- **TypeScript SDK:** [`@cinqueport/ctcc-x402`](https://www.npmjs.com/package/@cinqueport/ctcc-x402) (`npm install @cinqueport/ctcc-x402`)
- **ElizaOS Plugin:** [`@cinqueport/plugin-ctcc`](https://www.npmjs.com/package/@cinqueport/plugin-ctcc)
- **A2A Agent Card:** `https://cinqueport.net/.well-known/agent.json`
- **OpenAPI 3.1 Spec:** `https://cinqueport.net/openapi.json`
---

## Corporate Governance

CTCC™ is engineered and operated by **Cinqueport**, the sovereign international trade and due-diligence practice of **Pavilion (Stockport) Ltd** (`pspt.ltd`).

- **Company**: Pavilion (Stockport) Ltd (Registered in England and Wales · No. 14997067)
- **Practice Website**: [pspt.ltd](https://pspt.ltd)
- **Division Website**: [cinqueport.net](https://cinqueport.net)
- **Enquiries**: `hello@pspt.ltd` / `hello@cinqueport.net`
- **License**: Copyright (c) 2026 Pavilion (Stockport) Ltd. Licensed under the MIT License.
## Official SDKs & Agent Discovery

- **Python SDK:** [`ctcc-x402`](https://pypi.org/project/ctcc-x402/) (`pip install ctcc-x402`)
- **TypeScript SDK:** [`@cinqueport/ctcc-x402`](https://www.npmjs.com/package/@cinqueport/ctcc-x402) (`npm install @cinqueport/ctcc-x402`)
- **ElizaOS Plugin:** [`@cinqueport/plugin-ctcc`](https://www.npmjs.com/package/@cinqueport/plugin-ctcc)
- **A2A Agent Card:** `https://cinqueport.net/.well-known/agent.json`
- **OpenAPI 3.1 Spec:** `https://cinqueport.net/openapi.json`
