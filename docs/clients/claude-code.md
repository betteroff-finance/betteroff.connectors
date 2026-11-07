<img src="../../assets/clients/claude-code.png" alt="" width="40" height="40" align="absmiddle">

# Connect Claude Code to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Install the BetterOff plugin to use its financial tools and workflow skills in Claude Code.

**Tested:** sign-in and synthetic reads passed on October 6, 2026. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Install and sign in

1. Add the marketplace and install BetterOff:

   ```sh
   claude plugin marketplace add betteroff-finance/betteroff.connectors
   claude plugin install betteroff@betteroff
   ```

2. Start a new session or run `/reload-plugins`.
3. Run `/mcp` and select the BetterOff server.
4. Complete the browser sign-in prompt.

If you edit the plugin’s server configuration, keep it in `.mcp.json` and retain `"type": "http"`. Claude requires an explicit transport type for a remote URL.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

Interactive authenticated checks with synthetic data passed on October 6, 2026. Automated sessions and the full connection lifecycle remain unverified for the current client version. Tests cover only the recorded configuration. Client versions, policies, and extensions can change behavior.

Official documentation reviewed October 13, 2026: [Install Claude Code plugins](https://code.claude.com/docs/en/discover-plugins) and [MCP configuration and authentication](https://code.claude.com/docs/en/mcp).

[Choose another client](../../README.md#install-the-connector)
