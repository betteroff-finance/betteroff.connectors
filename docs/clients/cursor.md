<img src="../../assets/clients/cursor.svg" alt="" width="40" height="40" align="absmiddle">

# Connect Cursor to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Connect BetterOff to Cursor with its workflow skills, or add only its financial tools.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Install the plugin

Your organization must allow local plugin imports where that policy applies. Check **Allow Local Plugin Imports** before proceeding.

1. Clone or download [this repository](https://github.com/betteroff-finance/betteroff.connectors).
2. Copy `plugins/betteroff` into `~/.cursor/plugins/local/` so the plugin directory is `~/.cursor/plugins/local/betteroff`.
3. Restart Cursor or run **Developer: Reload Window**.
4. Open **Customize** and confirm that BetterOff is available.
5. Complete the BetterOff OAuth sign-in prompt.

A marketplace plugin with the same name can take precedence over the local copy. Check which copy Cursor loaded if your changes do not appear.

## Add only the MCP server

This option adds financial tools without the workflow skills. Merge the following entry into `~/.cursor/mcp.json`, preserving existing servers:

```json
{
  "mcpServers": {
    "betteroff": {
      "url": "https://api.betteroff.finance/mcp"
    }
  }
}
```

Complete the OAuth sign-in prompt after adding the server. Cursor asks before running each BetterOff tool unless you add it to your allowlist.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, a complete authenticated BetterOff connection test remains unfinished. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [Cursor plugins](https://prod.cursor.com/docs/plugins) and [Cursor MCP](https://prod.cursor.com/docs/mcp).

[Choose another client](../../README.md#install-the-connector)
