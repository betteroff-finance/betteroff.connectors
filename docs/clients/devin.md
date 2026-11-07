<img src="../../assets/clients/devin.svg" alt="" width="40" height="40" align="absmiddle">

# Connect Devin to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Connect BetterOff through your personal Devin account in the web app or CLI.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Use **Personal** access. **Organization** access shares one BetterOff sign-in across members’ sessions, allowing them to read your household finances. Other members can still interact with your personal sessions. Use BetterOff only in an organization whose members you trust with this data.

## Connect in the web app

1. Open **Customize** > **Plugins** and select **Personal**.
2. Choose **Add plugin** > **From repository**.
3. Enter `betteroff-finance/betteroff.connectors` with the subdirectory `plugins/betteroff`.
4. Wait for indexing to finish.
5. Open **Customize** > **MCPs**, select **betteroff**, and choose **Connect**.
6. Complete the BetterOff sign-in prompt.
7. Start a new session and mention `/betteroff:household-review` or `/betteroff:monthly-review` to load a skill.

If the web listing is stale, use **Reindex plugins** in **Customize**. Updating the CLI plugin does not refresh the web index.

## Connect in the CLI

Sign in to Devin before installing plugins. By default, installation synchronizes to your personal Devin manifest. Add `--local` to the install command to install on only this machine.

```sh
devin plugins install betteroff-finance/betteroff.connectors#plugins/betteroff
devin mcp login betteroff
```

Complete the separate BetterOff sign-in prompt. The CLI asks before each BetterOff tool call unless you allow it.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, a complete authenticated BetterOff connection test remains unfinished. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [Devin web plugins](https://docs.devin.ai/product-guides/plugins), [CLI plugins](https://docs.devin.ai/cli/extensibility/plugins/overview), [CLI MCP authentication](https://docs.devin.ai/cli/extensibility/mcp/configuration), and [MCP access scopes](https://docs.devin.ai/work-with-devin/mcp).

[Choose another client](../../README.md#install-the-connector)
