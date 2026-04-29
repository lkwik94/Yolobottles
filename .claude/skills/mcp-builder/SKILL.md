---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

# Process

## High-Level Workflow

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

Start with the sitemap: `https://modelcontextprotocol.io/sitemap.xml`
Then fetch specific pages with `.md` suffix.

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support, good compatibility, AI models generate TypeScript well)
- **Transport**: Streamable HTTP for remote servers (stateless JSON). stdio for local servers.

**Load framework documentation:**
- [MCP Best Practices](./reference/mcp_best_practices.md)
- **TypeScript SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [TypeScript Guide](./reference/node_mcp_server.md)
- **Python SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [Python Guide](./reference/python_mcp_server.md)

### Phase 2: Implementation

#### 2.1 Set Up Project Structure
See language-specific guides for project setup.

#### 2.2 Implement Core Infrastructure
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:** Use Zod (TypeScript) or Pydantic (Python). Include constraints and clear descriptions.

**Output Schema:** Define `outputSchema` where possible. Use `structuredContent` in responses.

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

### Phase 3: Review and Test

**TypeScript:**
```bash
npm run build
npx @modelcontextprotocol/inspector
```

**Python:**
```bash
python -m py_compile your_server.py
```

### Phase 4: Create Evaluations

Load [Evaluation Guide](./reference/evaluation.md) for complete guidelines.

Create 10 realistic test questions:
- Independent (not dependent on other questions)
- Read-only (non-destructive operations only)
- Complex (requiring multiple tool calls)
- Verifiable (single, clear answer)
- Stable (answer won't change over time)

Output format:
```xml
<evaluation>
  <qa_pair>
    <question>Complex question requiring multiple tool calls...</question>
    <answer>specific answer</answer>
  </qa_pair>
</evaluation>
```

---

# Reference Files

Load these as needed:

- [MCP Best Practices](./reference/mcp_best_practices.md) — Server/tool naming, response formats, pagination, transport selection
- [Python Implementation Guide](./reference/python_mcp_server.md) — FastMCP patterns, Pydantic models, complete examples
- [TypeScript Implementation Guide](./reference/node_mcp_server.md) — Zod schemas, tool registration, complete examples
- [Evaluation Guide](./reference/evaluation.md) — Question creation, answer verification, XML format
