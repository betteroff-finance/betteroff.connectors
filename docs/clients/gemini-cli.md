<img src="../../assets/clients/gemini-cli.png" alt="" width="40" height="40" align="absmiddle">

# Connect Gemini CLI to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Install the BetterOff extension to use its financial tools and workflow skills in Gemini CLI.

**Tested:** installation and skill loading only; sign-in and reads are not yet tested. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Use a machine with a browser that can reach Gemini’s `localhost` sign-in callback. A headless machine without browser support is not a verified setup route.

## Install and sign in

1. Install the extension:

   ```sh
   gemini extensions install https://github.com/betteroff-finance/betteroff.connectors
   ```

2. Restart Gemini CLI.
3. Run `/mcp auth betteroff` if sign-in does not start when you first use BetterOff.
4. Complete the browser sign-in prompt.

Tool approvals depend on Gemini CLI policy and trusted-tool settings.

## Resolve configuration conflicts

A `betteroff` server in Gemini’s `settings.json` overrides the extension’s server. Check for an older entry if Gemini connects to the wrong server.

Gemini reads the root `gemini-extension.json` and `skills/<name>/SKILL.md` files. Maintainers must update those skills through the [skill sync procedure](../../CONTRIBUTING.md#agent-workflow-sources).

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

Extension installation and skill discovery passed on October 6, 2026. Authentication and financial tool calls remain unverified. Tests cover only the recorded configuration. Client versions, policies, and extensions can change behavior.

Official documentation reviewed October 13, 2026: [Gemini extension reference](https://geminicli.com/docs/extensions/reference/) and [Gemini MCP authentication](https://geminicli.com/docs/tools/mcp-server/).

[Choose another client](../../README.md#install-the-connector)
