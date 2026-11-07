<img src="../../assets/clients/openclaw.svg" alt="" width="40" height="40" align="absmiddle">

# Connect OpenClaw to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Connect BetterOff to OpenClaw and install its workflow skills for the household owner.

**Not yet tested** with a BetterOff sign-in. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Restrict access to the household owner and use a direct chat. OpenClaw shares one BetterOff sign-in by default. Anyone else who can message the agent could read that household’s finances.

Clone or download [this repository](https://github.com/betteroff-finance/betteroff.connectors) and open a terminal at its root.

## Configure and sign in

1. Add the server and require tool prompts for Gateway-hosted Codex runs:

   ```sh
   openclaw mcp add betteroff --url https://api.betteroff.finance/mcp --transport streamable-http --auth oauth
   openclaw mcp configure betteroff --approval prompt
   ```

   Other agent runtimes use their own approval settings. Check those settings before using the connection.

2. Start the BetterOff sign-in flow:

   ```sh
   openclaw mcp login betteroff
   ```

   Use the printed loopback callback address. If your browser cannot reach it, finish with `openclaw mcp login betteroff --code <code>`. Replace `<code>` with the returned authorization code.

3. Check that the server exposes tools:

   ```sh
   openclaw mcp doctor betteroff --probe
   ```

4. Install the skills from the repository root:

   ```sh
   for skill in plugins/betteroff/skills/*/; do openclaw skills install "./$skill" --global; done
   ```

5. Run `openclaw skills check` to confirm that the selected agent can use the installed skills.

Local skill installation requires `SKILL.md` at each source directory’s root. An installed skill can still be unavailable to the selected agent.

## Separate sign-in for each sender

OpenClaw documents `oauth.identity: "per-requester"` with `gateway.publicOrigin` for separate sign-ins. This route has not been tested with BetterOff.

Shared channels still require mutually trusted participants. Another participant can open a sign-in link and bind an account to its intended sender. See [OpenClaw OAuth and transports](https://docs.openclaw.ai/cli/mcp/transports) before configuring this route.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

As of October 6, 2026, a complete authenticated BetterOff connection test remains unfinished. These instructions are based on client documentation; they are not a record of a successful BetterOff connection.

Official documentation reviewed October 13, 2026: [MCP registry and approvals](https://docs.openclaw.ai/cli/mcp/registry), [OAuth and transports](https://docs.openclaw.ai/cli/mcp/transports), and [Skill installation](https://docs.openclaw.ai/cli/skills).

[Choose another client](../../README.md#install-the-connector)
