<img src="../../assets/clients/github-copilot.svg" alt="" width="40" height="40" align="absmiddle">

# Connect GitHub Copilot to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Install BetterOff in VS Code or Copilot CLI to use its financial tools and workflow skills.

**Tested:** CLI installation only; sign-in, reads, VS Code, and the app are not yet tested. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Your organization’s policy can restrict plugins and marketplaces. Choose one installation route below.

## Install in VS Code

1. Enable `chat.plugins.enabled` in VS Code settings.
2. Add `betteroff-finance/betteroff.connectors` to the `chat.plugins.marketplaces` array in your user `settings.json`. Preserve existing entries.
3. Open the Extensions view and search `@agentPlugins`.
4. Select **Install** for **betteroff**.
5. Review the source trust prompt.

Use marketplace installation so VS Code resolves `plugins/betteroff` within the repository. The repository root is not the standalone plugin directory.

## Install in Copilot CLI

```sh
copilot plugin marketplace add betteroff-finance/betteroff.connectors
copilot plugin install betteroff@betteroff
```

## GitHub Copilot app

Open **Customize** > **Plugins** to browse plugins. The app’s custom-marketplace controls have not been verified here. Use Copilot CLI if you cannot add this repository in the app.

## Sign in and review permissions

Open the BetterOff server in your client’s MCP controls and complete its OAuth prompt. Approval behavior depends on the client, permission settings, and organization policy. Approving a tool call does not approve its proposal in BetterOff.

For package maintenance, VS Code supports the `plugin.json`, `mcp.json`, and `skills/` layout used by this repository.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

CLI installation passed on October 6, 2026. Authenticated tests and installation through the other Copilot clients remain unfinished. Tests cover only the recorded configuration. Client versions, policies, and extensions can change behavior.

Official documentation reviewed October 13, 2026: [VS Code agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins), [Copilot CLI installation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing), and [Copilot plugin surfaces](https://docs.github.com/en/copilot/concepts/agents/about-plugins).

[Choose another client](../../README.md#install-the-connector)
