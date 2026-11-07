<img src="../../assets/clients/pi.svg" alt="" width="40" height="40" align="absmiddle">

# Connect Pi to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Use Pi’s built-in MCP integration to connect BetterOff, then install its workflow skills.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Use Pi 0.99.0 or later. Clone or download [this repository](https://github.com/betteroff-finance/betteroff.connectors) and open a terminal at its root.

Skills copied to `~/.agents/skills/` are also available to other compatible clients. Review existing directories before copying; the command below can overwrite files with matching names.

## Configure and sign in

1. Add the server:

   ```sh
   pi mcp add betteroff --url https://api.betteroff.finance/mcp --exposure direct
   ```

2. Complete the BetterOff sign-in flow:

   ```sh
   pi mcp login betteroff
   ```

3. Check the server connection:

   ```sh
   pi mcp list
   ```

4. Copy the skills from the repository root:

   ```sh
   mkdir -p ~/.agents/skills
   cp -R plugins/betteroff/skills/* ~/.agents/skills/
   ```

5. Run `/reload` in an open Pi session to load the skills and server configuration.
6. Open `/mcp` to inspect the connection.

Pi can run tools without prompts; permission extensions can change that behavior. Corrections and transfer requests still require approval in BetterOff.

## Resolve configuration conflicts

Pi reads user MCP configuration from `~/.pi/agent/mcp.json` and trusted-project configuration from `.pi/mcp.json`. An extension that registers `/mcp` can replace the built-in integration. Check installed extensions if the commands above behave differently.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, a complete authenticated BetterOff connection test remains unfinished. Built-in MCP requires Pi 0.99.0 or later. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [Pi MCP](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md), [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md), and [Pi changelog](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/CHANGELOG.md).

[Choose another client](../../README.md#install-the-connector)
