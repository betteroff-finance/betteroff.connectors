# Unsent directory drafts

Drafted November 2, 2026. Nothing here has been submitted or sent.

## Microsoft 365 Copilot Agent Store

Package: [microsoft-copilot/](microsoft-copilot/), a declarative agent that calls the remote MCP server.

Before submitting:

1. FinSync enrolls in Partner Center (Microsoft 365 and Copilot program) and passes business verification.
2. Register the BetterOff OAuth client in the Teams Developer Portal (authorization URL, token URL, client ID, scope). Put its reference ID in `ai-plugin.json`.
3. Validate and sideload with Microsoft 365 Agents Toolkit. The `RemoteMCPServer` runtime is new; check the schema versions against the toolkit's current templates.
4. Run the synthetic acceptance procedure in Copilot, then zip the folder and submit in Partner Center with the shared listing copy and reviewer credentials.

## Google

Use the [shared listing copy](../README.md#shared-listing-copy). Before submitting, FinSync opens the publisher account and accepts Google's terms. Then confirm which form applies: a Gemini connected app, or a Google Cloud Marketplace listing. Fill these fields from the shared copy:

| Field | Value |
| --- | --- |
| App name | BetterOff |
| Developer | FinSync LLC |
| Support email | zach@betteroff.finance |
| Short description | Review household accounts, spending, net worth, investments, and debt. |
| Long description | Shared full description |
| MCP endpoint | https://api.betteroff.finance/mcp (Streamable HTTP, OAuth with PKCE) |
| Privacy / Terms | https://betteroff.finance/legal/privacy, https://betteroff.finance/legal/terms |
| Icon | https://api.betteroff.finance/.well-known/betteroff-icon.png |

## xAI email

To: xAI partnerships (confirm the address before sending)
Subject: Listing BetterOff's MCP connector in Grok

Hi,

I run BetterOff, a household finance app from FinSync LLC. We have a remote MCP server that lets an assistant read a household's bank, brokerage, exchange, and wallet accounts, with per-user OAuth consent. Users approve any changes or transfers in BetterOff, never in the assistant.

It's listed in the ChatGPT directory and the official MCP Registry as `finance.betteroff/mcp`. We'd like Grok users to be able to connect it too. Is there a connector directory or partner program we can apply to?

Endpoint: https://api.betteroff.finance/mcp
Docs: https://betteroff.finance/developers

Thanks,
Zach
BetterOff
zach@betteroff.finance
