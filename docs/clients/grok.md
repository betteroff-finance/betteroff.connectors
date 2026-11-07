<img src="../../assets/clients/grok.png" alt="" width="40" height="40" align="absmiddle">

# Connect Grok to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Connect BetterOff in Grok Build, grok.com, or Grok Bot.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Use BetterOff’s OAuth sign-in. Leave custom headers empty; do not add an `Authorization` header or an API key.

## Connect in Grok Build

To load both tools and skills, clone or download [this repository](https://github.com/betteroff-finance/betteroff.connectors). Run this command from its root:

```sh
grok --plugin-dir ./plugins/betteroff
```

Inspect `/plugins`, `/skills`, and `/mcps` to confirm that Grok loaded BetterOff.

To add only the MCP tools, use this alternative:

```sh
grok mcp add --transport http betteroff https://api.betteroff.finance/mcp
grok mcp doctor betteroff
```

Sign-in starts on first use. To sign in again, open `/mcps` and press `i`.

## Connect on grok.com

1. Open [Grok connectors](https://grok.com/connectors).
2. Select **New Connector** > **Custom**.
3. Name the connector `BetterOff`.
4. Enter `https://api.betteroff.finance/mcp` as the server URL and leave the headers empty.
5. Complete the BetterOff sign-in prompt.

## Connect in Grok Bot

For a Team Bot, OAuth uses each person’s sign-in. A key or token grants shared Bot access, so keep BetterOff on its OAuth route.

1. Send “Add a custom MCP server called betteroff at https://api.betteroff.finance/mcp”.
2. Check that the proposed URL is `https://api.betteroff.finance/mcp`.
3. Select **Add it**.
4. Select **Authorize** on the card Grok Bot posts.
5. Complete the BetterOff sign-in prompt.

The web and Bot procedures configure MCP access. They do not install this repository’s workflow skills.

## Restore the connection

If Grok reports a connection without opening BetterOff sign-in, remove the connector and add it again.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, complete authenticated BetterOff connection tests remain unfinished for Build, grok.com, and Bot. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [Grok Build plugins and skills](https://docs.x.ai/build/features/skills-plugins-marketplaces), [Build MCP](https://docs.x.ai/build/features/mcp-servers), [Grok web connectors](https://docs.x.ai/grok/connectors), and [Team Bot access](https://docs.x.ai/grok-bot/team-bots).

[Choose another client](../../README.md#install-the-connector)
