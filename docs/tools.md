<!-- Generated from tools.json by scripts/tools_catalog.py. Edit tools.json, then run the script. -->
<picture><source media="(prefers-color-scheme: dark)" srcset="../assets/betteroff-mark-white.svg"><img src="../assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff tools

[All clients](../README.md#install-the-connector) · [Connector reference](connector.md)

Connector package 0.6.1 describes hosted server 0.8.0 at `https://api.betteroff.finance/mcp` and defines 40 tools: 29 read tools and 11 write tools. A client sees only the tools its granted scopes allow.

- **Read** tools return data and change nothing.
- **Write** tools save a pending correction or transfer request, cancel a pending request, or send feedback. None can apply a correction, approve a transfer, or sign a transaction. You do those in BetterOff. Cancellation and feedback take effect when called.
- Tools work on every plan, including Free, over MCP or REST. Better-only tools return `CORE_REQUIRED` on Free. Insurance needs the Best plan, which is in early access.

The same catalog is available as [tools.json](../tools.json). With an API token, call any tool at `POST https://api.betteroff.finance/v1/tools/{name}`; see the [developer documentation](https://betteroff.finance/developers) and the [tool OpenAPI document](https://api.betteroff.finance/openapi/tools.json).

| Tool | Access | Scopes | Description |
| --- | --- | --- | --- |
| `betteroff_get_overview` | Read | `accounts:read`, `networth:read` | Household valuation, data coverage, identity, and connection health. |
| `betteroff_get_setup_status` | Read | `accounts:read` | Remaining setup steps, billing status, and reconnect links. |
| `betteroff_list_accounts` | Read | `accounts:read` | Accounts with balances and balance observation dates. |
| `betteroff_get_net_worth_history` | Read | `networth:read` | Stored net-worth valuations over a period. |
| `betteroff_explain_net_worth_change` | Read | `networth:read` | Reconciles the change between two stored valuations. |
| `betteroff_search_transactions` | Read | `transactions:read` | Finds transactions and totals a filtered set, including merchant history. |
| `betteroff_analyze_spending` | Read | `transactions:read` | Spending by category or merchant, with an optional period comparison. |
| `betteroff_detect_spending_patterns` | Read | `transactions:read` | Spending habits, trends, and unusual transactions. |
| `betteroff_get_account_flows` | Read | `accounts:read`, `transactions:read` | Gross deposits and withdrawals for specific accounts. |
| `betteroff_get_cash_flow` | Read | `cashflow:read` | Household income, expenses, and savings rate. |
| `betteroff_preview_cash_plan` | Read | `cashflow:read` | Read-only cash-plan scenario from amounts the user confirmed. Moves no money. |
| `betteroff_get_cash_rules` | Read | `accounts:read` | The household's order for idle cash, amount kept back, and bank, brokerage and onchain split. |
| `betteroff_list_recurring` | Read | `cashflow:read` | Observed recurring bills, subscriptions, and income. |
| `betteroff_get_portfolio` | Read | `investments:read` | Investment positions, allocation, and concentration. |
| `betteroff_get_defi_positions` | Read | `investments:read` | DeFi lending, staking, and liquidity positions with assets and liabilities. |
| `betteroff_get_vault_yields` | Read | `investments:read` | Reported APY of vaults available in Investing; not recommendations. |
| `betteroff_list_debts` | Read | `debts:read` | Debt balances, terms, and missing terms. |
| `betteroff_simulate_debt_payoff` | Read | `debts:read` | Arithmetic payoff scenarios; refuses when terms are missing. |
| `betteroff_get_checklist` | Read | `checklist:read` | Financial checklist progress, such as insurance, estate documents, and emergency fund. |
| `betteroff_list_deadlines` | Read | `checklist:read` | Recorded household deadlines, insurance renewals, and federal tax dates. |
| `betteroff_list_insurance` | Read | `checklist:read` | Insurance policies the household recorded, with coverage, premium, and renewal date. |
| `betteroff_get_budgets` | Read | `transactions:read`, `accounts:read` | Category budgets against this month's spending, and savings goal progress. |
| `betteroff_estimate_quarterly_tax` | Read | `cashflow:read` | US federal safe-harbor estimated tax from figures the user states. |
| `betteroff_get_giving_and_fees` | Read | `transactions:read` | Yearly charitable giving, personal gifts, bank fees, and investment fees. |
| `betteroff_search_activity` | Read | `activity:read` | Recorded financial record changes and correction proposals. |
| `betteroff_list_observations` | Read | `accounts:read`, `networth:read`, `transactions:read`, `cashflow:read`, `investments:read`, `debts:read` | Stored financial findings and their status. |
| `betteroff_propose_category_change` | Write | `transactions:read`, `corrections:prepare` | Saves a pending category correction for approval in BetterOff. |
| `betteroff_propose_recurring_kind` | Write | `cashflow:read`, `corrections:prepare` | Saves a pending bill-or-subscription classification for approval in BetterOff. |
| `betteroff_propose_debt_details` | Write | `debts:read`, `corrections:prepare` | Saves user-stated debt terms for approval in BetterOff. |
| `betteroff_propose_allocation_targets` | Write | `investments:read`, `corrections:prepare` | Saves user-stated target allocation for approval in BetterOff. |
| `betteroff_propose_budget` | Write | `transactions:read`, `corrections:prepare` | Saves a user-stated category budget for approval in BetterOff. |
| `betteroff_request_transfer` | Write | `accounts:read`, `transfers:prepare` | Requests a USDC transfer between the household's own wallets; the user signs in BetterOff. |
| `betteroff_request_bank_transfer` | Write | `accounts:read`, `transfers:bank` | Requests a transfer between the user's own linked accounts; the user confirms with a passkey. Not available right now. |
| `betteroff_request_vault_deposit` | Write | `investments:read`, `transfers:vault` | Requests a USDC or USDT vault deposit; the user signs in BetterOff. |
| `betteroff_get_action_request` | Read | `transfers:read` | Status of a transfer or deposit request. |
| `betteroff_get_money_activity` | Read | `accounts:read`, `transactions:read` | Natural wallet balances and the status of payments, requests, and transfers. |
| `betteroff_cancel_action_request` | Write | `transfers:prepare` or `transfers:bank` or `transfers:vault` | Cancels a pending request before it is signed. |
| `betteroff_track_wallet` | Write | `wallets:track` | Adds a public wallet address the user provides. |
| `betteroff_submit_feedback` | Write | `feedback:submit` | Sends a user-approved diagnostic report to BetterOff support. |
| `betteroff_get_checkout_link` | Read | `billing:checkout` | Sign-in-protected link to start a BetterOff plan checkout. |
