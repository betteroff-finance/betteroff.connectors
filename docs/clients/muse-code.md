<img src="../../assets/clients/muse-code.svg" alt="" width="40" height="27" align="absmiddle">

# Connect Muse Code to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Add BetterOff’s financial tools to Muse Code user settings, then install its workflow skills.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Clone or download [this repository](https://github.com/betteroff-finance/betteroff.connectors) and open a terminal at its root. Muse supports browser and headless OAuth sign-in. This guide uses user settings; plugin and project-only sign-in routes remain unverified.

## Configure and sign in

1. Merge this server into `~/.config/muse/settings.json`, preserving existing settings and `"schema_version": 1`:

   ```json
   {
     "schema_version": 1,
     "mcp_servers": {
       "betteroff": {
         "transport": "streamable_http",
         "url": "https://api.betteroff.finance/mcp",
         "mode": "optional"
       }
     }
   }
   ```

2. Start the BetterOff sign-in flow:

   ```sh
   muse mcp login betteroff
   ```

3. Install the skills from the repository root:

   ```sh
   for skill in plugins/betteroff/skills/*/; do muse skills install "$skill" --scope user; done
   ```

4. Run `muse skills list` to confirm installation.
5. Open `/mcp` in Muse to inspect the connection.

With `mode: optional`, Muse starts even when the server connection fails. Sign-in completed in another terminal becomes available without restarting Muse.

Review each proposal tool call separately. Do not choose **Always allow** for those tools.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, a complete authenticated BetterOff connection test remains unfinished. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [Muse settings](https://dev.meta.ai/docs/muse-code/configuration) and [MCP, OAuth, and skills](https://dev.meta.ai/docs/muse-code/extending).

[Choose another client](../../README.md#install-the-connector)
