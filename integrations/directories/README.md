<picture><source media="(prefers-color-scheme: dark)" srcset="../../assets/betteroff-mark-white.svg"><img src="../../assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff MCP directory guide

[All clients](../../README.md#install-the-connector) · [Contributing](../../CONTRIBUTING.md) · [Zapier private preview](../zapier/README.md)

This guide owns directory status, submission fields, and the acceptance procedure. Dated test logs and request IDs are kept in maintainers' private records. A directory listing publishes metadata; it never grants access to a household.

## Status

Recorded October 13, 2026; the ChatGPT row was updated November 2, 2026. Do not change a status without dated evidence for that destination.

| Destination | Status | Next step |
| --- | --- | --- |
| [Official MCP Registry](#official-mcp-registry) | Published as `finance.betteroff/mcp` | Publish [server.json](server.json) with a new version for each change |
| Official MCP Registry, `finance.betteroff/public` | Deprecated October 29, 2026 at 08:13:51 UTC. Its remote `https://betteroff.finance/mcp` redirects to `/agents`, so connections failed. Glama copied this entry | Ask Glama to drop its copy |
| [Smithery](#smithery) | Published; owned by a test-account namespace | Claim vendor ownership; test token renewal |
| [Claude connector directory](#chatgpt-and-claude-connector-directories) | Not submitted | Submit through the developer portal |
| [ChatGPT directory](#chatgpt-and-claude-connector-directories) | Published and listed publicly; version 0.5.2 published November 2, 2026 from the OpenAI Plugins page | Test the transfer restriction in ChatGPT |
| [Glama](#glama) | Not submitted; OAuth callback fails in Glama's inspector | Glama fixes its popup handoff |
| [PulseMCP](#pulsemcp) | Not listed; manual submissions paused | Check for Registry ingestion when PulseMCP resumes |

The independent production lifecycle test passed: scoped sign-in, discovery, reads, refresh, and denial after disconnection. It verifies server behavior, not any destination's client.

## ChatGPT and Claude connector directories

**Claude.** Submit at [claude.ai/directory/manage](https://claude.ai/directory/manage): select **Submit new**, then **MCP connector**. The submitter needs a paid Claude plan. Before submitting:

1. Confirm every tool has a `title` and a `readOnlyHint` or `destructiveHint`. The server source sets `title`, `readOnlyHint` (true for read tools), and `destructiveHint: false` on all 29 tools; the portal's **Tools** step syncs and flags them from the live server. Confirm there before submitting.
2. Add the server as a custom connector in Claude and call each tool with a synthetic household.
3. Prepare reviewer credentials for a fully populated synthetic household. Enter them only in the portal.
4. Complete the seven compliance acknowledgments, including financial transactions and prompt injection. Use the [shared listing copy](#shared-listing-copy).

Claude Code plugin tests do not verify this destination. Source: [Submit a connector to the directory](https://claude.com/docs/connectors/building/submission), reviewed October 13, 2026.

**ChatGPT.** Build the restricted package with the [ChatGPT submission procedure](../../CONTRIBUTING.md#chatgpt-submission-package). A generated ZIP is not an approved listing. OpenAI approved BetterOff for the ChatGPT directory on October 22, 2026. Version 0.5.2 was published from the OpenAI Plugins page on November 2, 2026, replacing 0.5.1; the page shows it listed publicly. No authenticated ChatGPT test is recorded.

The same `readOnlyHint` annotations drive Hermes Agent's approval prompt for `trust: untrusted` servers and Zapier's **Read-Only** label.

## Synthetic acceptance procedure

Run this for each destination before submitting. A Glama submission may publish immediately, so do not create its connector record as a test draft.

1. Use a dedicated synthetic household owner and verify the household identity before granting access.
2. Request `accounts:read` and `networth:read`, the explicit `/mcp` resource audience, and `offline_access` only for refresh testing. Record any client that cannot narrow its scopes.
3. Initialize the connection and record server name, version, and negotiated protocol. List tools and confirm the limited grant exposes no correction, feedback, or transfer tools.
4. Call `betteroff_get_setup_status`, `betteroff_get_overview`, and `betteroff_get_net_worth_history`. Compare values with the synthetic fixture and preserve missing-data warnings. Record request IDs, not tokens or household records.
5. Refresh the connection and repeat a read to confirm renewal.
6. Disconnect in BetterOff. Confirm a new read and a refresh attempt are denied. Removing a connection from the directory client alone is insufficient.
7. Record the destination, date, scopes, version, outcomes, and sanitized request IDs. Keep credentials in private storage. Resolve failures before seeking authorization to submit.

## Shared listing copy

Use these fields for directory submissions. The official Registry and Smithery entries are published; Glama and PulseMCP remain unsubmitted in the recorded evidence. Resolve the [open items](#status) before submitting to Glama.

### Shared fields

| Field | Draft value |
| --- | --- |
| Display name | BetterOff |
| Publisher | FinSync LLC |
| Short description | Read bank, brokerage, exchange, and wallet accounts; prepare changes and transfers for approval. |
| Suggested categories | Finance; Personal finance; Productivity. Select only categories the destination actually offers. |
| Homepage | https://betteroff.finance |
| User documentation | https://betteroff.finance/agents |
| Developer documentation | https://betteroff.finance/developers |
| Connector distribution | https://github.com/raintree-technology/betteroff.connectors |
| Support | https://betteroff.finance/contact |
| Privacy policy | https://betteroff.finance/legal/privacy |
| Terms | https://betteroff.finance/legal/terms |
| Icon | https://api.betteroff.finance/.well-known/betteroff-icon.png |
| Remote URL | https://api.betteroff.finance/mcp |
| Transport | Streamable HTTP |
| Authentication | OAuth with authorization code and PKCE S256; per-user household consent |
| API key or fixed header | None for this OAuth connection |
| Server version | 0.5.0 in the recorded production initialization; verify again for a new release |
| License | MIT for the connector repository. The hosted server is proprietary and governed by the BetterOff Terms. |

### Full description

BetterOff connects an AI assistant to your household's bank, brokerage, exchange, and wallet accounts. Review balances, net worth, spending, cash flow, recurring charges, investments, and debt. Ask for a household overview, review a month of spending, or identify recurring subscriptions. Results include dates, source status, and incomplete-data warnings.

An eligible BetterOff household owner signs in and chooses permissions. All household members must consent to AI processing, and the owner must accept the applicable Terms. Financial information returned by tools is shared with the connected client. Every tool, including read tools, requires BetterOff Core. Free accounts and trials cannot use the connector.

Correction tools prepare changes for approval in BetterOff. Separate transfer permissions can expose tools that prepare wallet transfers, bank transfers, or vault deposits; the user must approve each request in BetterOff and complete the required wallet signature or passkey confirmation. MCP tools cannot approve or execute those requests themselves. A separate, opt-in feedback tool sends user-approved diagnostic reports.

Available tools depend on granted permissions. BetterOff does not provide individualized financial, tax, or legal advice through this connector.

### Example prompts

- Show my household overview and flag missing or out-of-date data.
- Review my spending and cash flow for the last complete month.
- Review recurring charges and identify bills and subscriptions.
- Summarize my investment allocation and concentration.
- Find payments that may be miscategorized and prepare corrections for review.

### Reviewer setup notes

Use a dedicated synthetic household. Start with `accounts:read` and `networth:read`; do not request transfer, correction, or feedback permissions for the initial connection check. Include the resource parameter `https://api.betteroff.finance/mcp` in OAuth authorization and token exchange. Request `offline_access` only if testing refresh.

This is a limited test grant, not a promise that the general endpoint only supports read tools. Do not describe the endpoint as read-only or claim that all its tools have passed live tests.

Keep reviewer credentials outside this public repository. The recorded Glama test used an existing synthetic reviewer; Smithery signup and limited-scope private testing are complete. Neither establishes a completed reviewer setup for another destination. A contact form URL is available; if a submission requires a named contact or email, obtain the approved business contact before completing that field.

## Official MCP Registry

**Published** as `finance.betteroff/mcp` on October 13, 2026. Version 0.5.2, which changes only the description, was published October 29, 2026 at 08:14:01 UTC through the Registry API with DNS login, and a public GET confirmed it as latest. The latest Registry record should match [server.json](server.json); the Registry needs a new version for every change, including metadata-only updates. DNS ownership of `betteroff.finance` is verified; the signing key stays in ignored local storage.

The older `finance.betteroff/public` 1.0.0 record points to a retired anonymous endpoint. It was marked deprecated on October 29, 2026. Do not use it for setup.

The repository field is omitted because this repository distributes client configuration, not the hosted server. Sources: [remote-server format](https://modelcontextprotocol.io/registry/remote-servers) and [authentication](https://modelcontextprotocol.io/registry/authentication).

## Smithery

**Published** at [smithery.ai/servers/b432acfe/betteroff](https://smithery.ai/servers/b432acfe/betteroff) after synthetic acceptance testing. Five read tools passed with `accounts:read` and `networth:read`, and disconnection was confirmed. Token renewal was not tested because `offline_access` was excluded.

| Field | Value |
| --- | --- |
| Server | `b432acfe/betteroff` |
| Owner namespace | Dedicated test-account namespace `b432acfe`; verified vendor ownership is not established |
| Hosting | Existing BetterOff hosting at `https://api.betteroff.finance/mcp` |

Smithery scans tools after authentication and proxies upstream traffic. Use only a synthetic household for scans. The optional static server card at `/.well-known/mcp/server-card.json` returns 401; do not weaken endpoint authentication to make a scan pass. See [Smithery publishing requirements](https://smithery.ai/docs/build/publish).

## Glama

**Not submitted.** Glama's inspector reaches BetterOff consent, but its callback cannot hand the authorization code back: Glama relies on the popup's opener, which BetterOff's `Cross-Origin-Opener-Policy` isolates. The recommended fix is a same-origin callback channel in Glama's client. BetterOff's opener isolation stays in place.

Use **Connector** on [Glama's connectors page](https://glama.ai/mcp/connectors). Glama publishes healthy connectors immediately, so treat **Add MCP Server → Connector** as publishing.

| Field | Value |
| --- | --- |
| Authentication | OAuth 2.0 badge; authorization code with PKCE S256 |
| Documentation, policies, icon, full description | Copy from [shared listing copy](#shared-listing-copy) |
| Private test credentials | Not supplied; use a synthetic OAuth connection if required |

Glama's gateway stores complete tool request and response payloads in call logs. Use synthetic data for evaluation, and document this data path before households connect through the gateway. Claim ownership only with Glama's issued DNS or HTTP challenge. Source: [Glama documentation](https://glama.ai/mcp/faq).

## PulseMCP

**Not listed.** On October 13, 2026, the [submission page](https://www.pulsemcp.com/submit) said manual submissions and listing changes are paused, and that its pipeline will ingest the official Registry when it resumes. When it resumes, claim or correct the ingested entry instead of creating a duplicate.

| Field | Draft value |
| --- | --- |
| Server name / provider | Use Display name / Publisher from the shared fields |
| Summary | Connect an AI assistant to BetterOff to review household accounts, spending, net worth, investments, and debt. Prepare corrections and transfer requests for approval in BetterOff. |
| Hosted endpoint / setup documentation / public connector repository | Use Remote URL / User documentation / Connector distribution from the shared fields |
| Registry name | finance.betteroff/mcp; published October 13, 2026 |
| Authentication / license / pricing | Use the shared fields and full description |

Use [shared listing copy](#shared-listing-copy) for the full description, policies, support, icon, and example prompts. These are prepared editorial fields, not a verified form or import schema.

## Listing attribution update — October 13, 2026

Registry metadata version 0.5.1 adds the consent-aware website tracking link. The hosted server remains version 0.5.0; its MCP endpoint and OAuth identifiers are unchanged. The Registry requires a new version for metadata changes. A public latest-version read confirmed the new record is active and latest. The separate `finance.betteroff/public` entry was not changed.

Smithery's homepage field was updated through its documented metadata API. Its rendered public Homepage link contains `utm_source=smithery`, `utm_medium=directory`, and `utm_campaign=mcp-listing`. Both website destinations returned HTTP 200 while preserving those parameters. No connection, release scan, or household grant was created.

Glama remains stopped and unsubmitted. The unused application relay module and tests were removed from BetterOff; the historical local experiment is not deployed.
