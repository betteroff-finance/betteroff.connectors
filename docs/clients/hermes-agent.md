<img src="../../assets/clients/hermes-agent.png" alt="" width="40" height="40" align="absmiddle">

# Connect Hermes Agent to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Add BetterOff’s financial tools and install its workflow skills in Hermes Agent.

**Tested:** sign-in and synthetic reads passed on October 6, 2026. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Configure and sign in

1. Merge this server into `~/.hermes/config.yaml`, preserving existing settings:

   ```yaml
   mcp_servers:
     betteroff:
       url: "https://api.betteroff.finance/mcp"
       auth: oauth
       trust: untrusted
       sampling:
         enabled: false
   ```

   Keep `trust: untrusted`. Hermes then asks before running tools that are not marked read-only, including correction proposals and transfer requests.

2. Start the BetterOff sign-in flow:

   ```sh
   hermes mcp login betteroff
   ```

3. Install the 11 skills:

   ```sh
   for skill in household-review monthly-review subscription-audit categorize-transactions debt-plan portfolio-check connect-and-setup financial-checkup spending-changes upcoming-bills net-worth-change; do
     hermes skills install "betteroff-finance/betteroff.connectors/plugins/betteroff/skills/$skill"
   done
   ```

4. Start a new session or run `/reload-mcp` to refresh available tools.

MCP configuration and skill installation are separate. Each skill source above points to a GitHub directory containing `SKILL.md`.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

Authenticated checks with synthetic data passed on October 6, 2026. The full connection lifecycle remains unverified for the current client version. Tests cover only the recorded configuration. Client versions, policies, and extensions can change behavior.

Official documentation reviewed October 13, 2026: [Hermes MCP setup](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp), [MCP configuration reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference), and [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

[Choose another client](../../README.md#install-the-connector)
