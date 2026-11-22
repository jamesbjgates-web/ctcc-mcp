# CTCC™ Multi-Directory Submission Pack

This submission pack contains exact, copy-paste-ready titles, descriptions, categories, JSON snippets, and instructions to list **Cinqueport Token Control Check (CTCC™)** and the **`ctcc-mcp`** server across AI agent directories, MCP registries, API catalogs, and package indexes.

---

## Master Metadata Summary
- **Product Name**: Cinqueport Token Control Check (CTCC™)
- **MCP Package Name**: `ctcc-mcp`
- **Provider**: Cinqueport (Specialist division of Pavilion (Stockport) Ltd, Company No. 14997067)
- **Website**: https://cinqueport.net
- **Primary Tool**: `check_token_control`
- **Core Technology**: Base Mainnet (eip155:8453) · x402 v2 HTTP 402 Protocol · Model Context Protocol (MCP) 2024-11-05
- **Pricing**: $0.01 USDC (10,000 atomic units) per check
- **Receiving Address**: `0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75`
- **Canonical Endpoints**:
  - Protected API: `POST https://cinqueport.net/check`
  - OpenAPI Specification: `https://cinqueport.net/openapi.json`
  - Machine Descriptor: `https://cinqueport.net/ctcc.json`
  - LLMs Context: `https://cinqueport.net/llms.txt`
  - Agent Workflow Registry: `https://cinqueport.net/agents.json`
  - AI Plugin Manifest: `https://cinqueport.net/.well-known/ai-plugin.json`
  - x402 Protocol Manifest: `https://cinqueport.net/.well-known/x402.json`
  - A2A Agent Card: `https://cinqueport.net/.well-known/agent-card.json`
  - XML Sitemap: `https://cinqueport.net/sitemap.xml`
- **GitHub Repository**: `https://github.com/jamesbjgates-web/ctcc-mcp`

---

## 1. Coinbase x402 Bazaar & CDP Agentic Payments Directory
- **Listing Portal**: https://bazaar.x402.org/ and automatic indexing via CDP Facilitator
- **Manifest URL to Submit**: `https://cinqueport.net/.well-known/x402.json`
- **Title**: `Cinqueport Token Control Check (CTCC™)`
- **Short Tagline**: `Deterministic smart-contract authority and control inspection on Base Mainnet via x402 v2 micropayments.`
- **Category**: `Blockchain Security / AI Agent Treasury Governance`
- **Protocol**: `x402 v2`
- **Payment Method**: `POST https://cinqueport.net/check`
- **Network**: `eip155:8453` (Base Mainnet)
- **Settlement Asset**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (Canonical USDC)
- **Amount**: `10000` ($0.01 USDC)
- **PayTo**: `0x14d4035290a31B81E99e2DEE26ef0a10e5Aa4d75`
- **Automated Indexing**: CTCC returns the official `extensions.bazaar.info` block in every 402 Payment Required challenge and header. Any settled transaction on Base Mainnet automatically prompts indexing into the Bazaar registry.

---

## 2. APIs.guru (OpenAPI Directory)
- **Submission Repository**: https://github.com/APIs-guru/openapi-directory
- **Submission Method**: Fork repo, create PR adding specification.
- **Spec URL**: `https://cinqueport.net/openapi.json`
- **Target Path in Repo**: `APIs/cinqueport.net/2.0.0/openapi.yaml`
- **PR Title**: `Add Cinqueport Token Control Check (CTCC) API`
- **PR Description**:
```markdown
Adds Cinqueport Token Control Check (CTCC™) OpenAPI 3.1 specification.
- Provider: Cinqueport / Pavilion (Stockport) Ltd
- Live Spec: https://cinqueport.net/openapi.json
- Capability: Deterministic smart-contract control inspection on Base Mainnet via x402 v2 micropayments.
```

---

## 3. Postman Public API Network
- **Listing Portal**: https://www.postman.com/explore
- **Workspace Name**: `Cinqueport Commercial Intelligence`
- **Collection Name**: `CTCC™ Token Control Check API`
- **Import Method**: Import from URL $\rightarrow$ `https://cinqueport.net/openapi.json`
- **Collection Summary**:
```text
Official Postman Collection for CTCC™ (Cinqueport Token Control Check).
Provides deterministic authority and control inspection for Base Mainnet smart contracts, including bytecode verification, ERC-20 metadata, owner/admin addresses, pause states, and EIP-1967 proxy pointers. Operates via x402 v2 HTTP 402 micro-settlements ($0.01 USDC).
```
- **Environment Variables**:
  - `baseUrl`: `https://cinqueport.net`
  - `sampleContract`: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

---

## 4. Official Model Context Protocol (MCP) Registry
- **Repository**: https://github.com/modelcontextprotocol/servers
- **Submission Method**: Submit PR to `modelcontextprotocol/servers` or register in the official catalog.
- **Server Name**: `ctcc` (or `cinqueport-ctcc`)
- **Package**: `ctcc-mcp`
- **Description**: `Deterministic Base Mainnet smart-contract authority and control inspection via x402 v2 protocol.`
- **Transport**: `stdio`
- **Claude Desktop Configuration Snippet**:
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

---

## 5. Smithery (`smithery.ai`)
- **Listing Portal**: https://smithery.ai/new
- **Repository URL**: `https://github.com/jamesbjgates-web/ctcc-mcp`
- **Configuration**: Automatically detected from `smithery.yaml` located in `ctcc-mcp/smithery.yaml`.
- **Display Name**: `Cinqueport Token Control Check (CTCC™)`
- **One-Click Installation Command**:
```bash
npx -y @smithery/cli install ctcc-mcp --client claude
```
- **Description**:
```text
Deterministic smart-contract authority and control inspection for AI agents on Base Mainnet (eip155:8453). Evaluates bytecode existence, ERC-20 metadata, admin/owner presence, pause state, and EIP-1967 proxy implementation pointers. Operates via x402 v2 micropayments ($0.01 USDC).
```

---

## 6. Glama MCP Registry (`glama.ai`)
- **Listing Portal**: https://glama.ai/mcp/servers $\rightarrow$ **Submit Server**
- **Repository URL**: `https://github.com/jamesbjgates-web/ctcc-mcp`
- **Package Path**: `ctcc-mcp`
- **Server Name**: `ctcc-mcp`
- **Category**: `Blockchain`, `Security`, `Finance`
- **Keywords**: `mcp`, `base`, `x402`, `smart-contracts`, `token-security`, `ai-agents`, `cinqueport`
- **Parsed Metadata**: Reads `package.json` and `smithery.yaml` directly from repository.

---

## 7. PulseMCP (`pulsemcp.com`)
- **Listing Portal**: https://pulsemcp.com/submit
- **Server Title**: `Cinqueport Token Control Check (CTCC™)`
- **Tool Name**: `check_token_control`
- **Transport**: `stdio`
- **Repository**: `https://github.com/jamesbjgates-web/ctcc-mcp`
- **Website**: `https://cinqueport.net`
- **Documentation**: `https://cinqueport.net/openapi.json`
- **Description**:
```text
Autonomous AI agent tool for deterministic smart-contract authority inspection on Base Mainnet (eip155:8453). Analyzes bytecode, ERC-20 methods, admin addresses, pause circuit breakers, and EIP-1967 upgradeable proxy slots without subjective risk scoring. Uses the x402 v2 protocol for $0.01 USDC micro-settlements.
```

---

## 8. mcp.so & Awesome-MCP-Servers
- **Repositories / Portals**:
  - https://github.com/punkpeye/awesome-mcp-servers
  - https://mcp.so/submit
- **Table Row Markdown Entry**:
```markdown
| [CTCC™ Token Control Check](https://github.com/jamesbjgates-web/ctcc-mcp) | Deterministic Base Mainnet smart-contract authority, bytecode, and proxy inspection via x402 v2 micropayments ($0.01 USDC). | `python3 -m ctcc_mcp.server` |
```

---

## 9. Python Package Index (PyPI) — `ctcc-mcp`
- **Package Name**: `ctcc-mcp`
- **Prerequisites**: `pip install build twine`
- **Build Command**:
```bash
cd ctcc-mcp
python3 -m build
```
- **Publish Command**:
```bash
twine upload dist/*
```
- **User Installation**:
```bash
pip install ctcc-mcp
ctcc-mcp --check 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

---

## 10. npm Registry — `@cinqueport/ctcc-mcp` / `ctcc-mcp`
- **Package Name**: `ctcc-mcp` (or scoped `@cinqueport/ctcc-mcp`)
- **Build & Publish Command**:
```bash
cd ctcc-mcp
npm publish --access public
```
- **User Execution (npx)**:
```bash
npx ctcc-mcp --check 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```
