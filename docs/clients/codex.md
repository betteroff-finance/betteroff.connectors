<img src="../../assets/clients/codex.png" alt="" width="40" height="40" align="absmiddle">

# Connect Codex to BetterOff

[All clients](../../README.md#install-the-connector) · [Connector reference](../connector.md)

Install the BetterOff plugin to use its financial tools and workflow skills in Codex.

**Tested:** sign-in and synthetic reads passed on October 6, 2026; installation passed again on October 13. See [test record](#verification-and-sources).

Read the [account and consent requirements](../../README.md#before-you-start) before connecting. Run shell commands in a terminal and slash commands inside the client.

## Before you start

Use the Codex app or CLI. This plugin route is unavailable in the IDE extension.

## Install and sign in

1. Add the marketplace and install BetterOff:

   ```sh
   codex plugin marketplace add betteroff-finance/betteroff.connectors
   codex plugin add betteroff@betteroff
   ```

2. Start a new Codex session.
3. Open `/plugins` and confirm that BetterOff is installed.
4. Complete the BetterOff sign-in prompt before requesting financial data. Installing the plugin does not authorize access to your household.

## Verify the connection

Follow [Sign in and ask your first question](../connector.md#sign-in-and-ask-your-first-question). Confirm that the result identifies your household and includes dates or missing-data warnings. A server listed as connected does not prove that a financial read succeeded.

For failed reads, use [Connection troubleshooting](../connector.md#connection-troubleshooting). To revoke access, follow [Approval and disconnection](../connector.md#approval-and-disconnection).

## Verification and sources

Authenticated checks with synthetic data passed on October 6, 2026. On October 13, 2026, the two install commands above installed plugin 0.5.0 into an empty Codex home with codex-cli 0.162.1; that run did not sign in. Token renewal and access revocation remain unverified for the current client version. Tests cover only the recorded configuration. Client versions, policies, and extensions can change behavior.

Official documentation reviewed October 13, 2026: [Codex plugins](https://learn.chatgpt.com/docs/plugins) and [CLI plugin commands](https://learn.chatgpt.com/docs/cli/reference).

[Choose another client](../../README.md#install-the-connector)
