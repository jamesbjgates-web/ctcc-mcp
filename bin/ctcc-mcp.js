#!/usr/bin/env node

/**
 * CTCC MCP Server launcher.
 * Bridges Node-based MCP runners (Smithery CLI, npx, Claude Desktop)
 * directly to the zero-dependency Python stdio server.
 */

const { spawn } = require('child_process');
const path = require('path');

const serverDir = path.resolve(__dirname, '..');
const pythonCmd = process.env.PYTHON_BIN || 'python3';

const child = spawn(pythonCmd, ['-m', 'ctcc_mcp.server', ...process.argv.slice(2)], {
  cwd: serverDir,
  stdio: 'inherit',
  env: process.env
});

child.on('error', (err) => {
  console.error(`[ctcc-mcp] Failed to launch ${pythonCmd}:`, err.message);
  process.exit(1);
});

child.on('exit', (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
  } else {
    process.exit(code || 0);
  }
});
