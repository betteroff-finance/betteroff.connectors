<img src="../../assets/clients/zapier.ico" alt="" width="40" height="40" align="absmiddle">

# BetterOff Zapier private preview

[Directory listings](../../README.md#directory-listings) · [Connector reference](../../docs/connector.md) · [Directory guide](../directories/README.md)

**Private preview — not submitted for public listing.** Integration `247763`, version `1.0.0`, has two read actions. API-token authentication, both actions, and token revocation passed with a synthetic household on October 13, 2026. Zapier's publishing requirements remain open; see [listing materials and remaining work](#listing-materials-and-remaining-work).

Open the integration from **My integrations** in the [Zapier Developer Platform](https://developer.zapier.com/) while signed in as its Admin account.

## Included operations

| Zapier action | BetterOff tool | Required permissions |
| --- | --- | --- |
| Get Financial Overview | `betteroff_get_overview` | `accounts:read`, `networth:read` |
| Get Net Worth History | `betteroff_get_net_worth_history` | `networth:read` |

These are retrieval actions. Zapier’s `create` operation type describes their placement in a Zap, not a financial write. Each snippet fixes its destination and tool name. There is no generic tool runner, transfer operation, correction proposal, feedback submission, or user-supplied URL.

The listing draft uses BetterOff’s public REST tool adapter and API token authentication. This is separate from the OAuth MCP connection test. Create a dedicated token with only `accounts:read` and `networth:read`; the adapter does not inspect a token’s other permissions. Never use a token with write or transfer permissions. Tokens expire, so users must reconnect with a replacement before expiry.

No dependencies are required to generate or test these Platform UI snippets. This is not a CLI upload package or a Platform UI import format.

## Generate and verify

Run from the repository root:

```sh
node --test integrations/zapier/draft.test.cjs
node integrations/zapier/build-draft.cjs
```

The generator writes configuration and Code Mode snippets to `.private/zapier-draft/`. It does not contact Zapier or include credentials. Tests use mocked responses and cannot establish live compatibility.

## Test the MCP connection first

Use a dedicated synthetic BetterOff owner account. Confirm its household identity before granting access. Do not connect a real household for this test.

1. In Zapier Apps, add an MCP Client connection with URL `https://api.betteroff.finance/mcp`, Streamable HTTP transport, and OAuth enabled.
2. Sign in to the synthetic BetterOff account. Select only `accounts:read` and `networth:read` in consent if the client permits scope selection. If it requests broader access that cannot be narrowed, stop and record the limitation.
3. Confirm tool discovery and run `betteroff_get_setup_status`, `betteroff_get_overview`, and `betteroff_get_net_worth_history` with `period: "30d"`.
4. Compare account coverage and net worth with the known synthetic fixture. Preserve incomplete-data warnings. Record the date, tool names, Zap IDs, and successful run IDs without tokens or real financial data.
5. Disconnect the test grant in BetterOff and verify that a new read fails. Reconnect only the synthetic account if a retained test connection is needed.

## Prepare the private integration

1. Create or reuse the BetterOff integration in Developer Platform. Keep it private. Copy the name, description, homepage, and API documentation URL from `platform-ui-draft.json`.
2. Choose API Key authentication and create the required password field `api_token` with the supplied help text. Paste `authentication.js.txt` into the authentication test’s Code Mode. Replace Zapier's generated request template with the supplied credential-free template. Verify the saved source has no token in URL parameters or action input fields.
3. Connect a synthetic account with a dedicated token carrying only the two read permissions above. The authentication test reads the overview, which exercises both permissions.
4. Add the two actions using the generated definitions and Code Mode snippets. For history, use the supplied period choices. Keep the complete response envelope, including currency, `asOf`, quality, warnings, and pagination.
5. Obtain samples from successful synthetic runs. Define output fields from those responses. For overview, expose `data.identity.name`, `data.valuation.netWorth`, and `data.valuation.baseCurrency`; valuation may be null. For history, expose `data.period` and the `data.dataPoints` line items. Also expose envelope currency, freshness, quality, and warnings. Do not claim fabricated samples are live test evidence.
6. Run each action in an enabled test Zap with a harmless destination containing only synthetic data. Retain successful history. Test expired/revoked access and missing permissions without weakening authorization.
7. Run Zapier validation. Record every unresolved error and publishing task. Submit only after all requirements are met and submission is authorized. The user has authorized submission, but the requirements below remain unresolved.

## Listing materials and remaining work

At the end of testing on October 13, 2026, Zapier listed five publishing tasks: the logo, a company-domain user, three users with live Zaps (zero after cleanup), and at least one live Zap for each action. Both successful-task checks have cleared. The last code validation reported zero errors and zero warnings. No readiness attestation or public listing submission was made.

- Name: **BetterOff**.
- Description: **BetterOff is a household finance app for tracking accounts, net worth, spending, investments, and debt.**
- Homepage: <https://betteroff.finance>.
- API documentation: <https://betteroff.finance/developers>.
- Support: <https://betteroff.finance/contact>.
- Logo: the public [BetterOff icon](https://api.betteroff.finance/.well-known/betteroff-icon.png) was downloaded to `.private/zapier-draft/betteroff-icon.png` and verified as a 512 × 512 PNG with an alpha channel. Upload is unfinished: the Chrome file chooser timed out, and native Chrome control was not approved.
- Category selected in Zapier: **Accounting**.
- Add or verify an integration admin with an approved company-domain email. The requested Gmail login alone does not meet this publication requirement.
- Arrange three genuine users with successful live Zaps. Do not create fake users to satisfy this check.
- Provision the required non-expiring reviewer account for `integration-testing@zapier.com`, populated exclusively with synthetic data. An existing reviewer account for another directory is not sufficient evidence.
- Confirm the publicly launched product and documented API meet Zapier’s requirements. BetterOff documents its API as beta; obtain clarification if Zapier considers that a publication blocker.
- Provide user setup documentation and disclose token expiry/reconnection. Record live test evidence and final validation before considering submission.

## Sources

- [Connect remote MCP servers](https://help.zapier.com/hc/en-us/articles/38777069364109-Connect-remote-MCP-servers-to-Zapier-using-MCP-Client)
- [API key authentication](https://docs.zapier.com/integrations/build/apikeyauth)
- [Publication requirements](https://docs.zapier.com/integrations/publish/integration-publishing-requirements)
- [Validation checks](https://docs.zapier.com/integrations/publish/integration-checks-reference)
