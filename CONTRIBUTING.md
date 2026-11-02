<picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# Contributing to BetterOff connectors

[All clients](README.md#install-the-connector) · [Connector reference](docs/connector.md)

Use this guide to find the source for each kind of documentation and run repository checks.

## Documentation map

| Reader or task | Canonical document |
| --- | --- |
| Install a client and choose a workflow | [Installation guide](README.md) |
| Check client verification and its limits | [Client guides](README.md#install-the-connector) and [status vocabulary](#client-status-vocabulary) |
| Understand permissions, data, and approval boundaries | [Connector reference](docs/connector.md) |
| Look up a tool's access and scopes | [tools.json](tools.json), rendered as the [tool reference](docs/tools.md) |
| Connect an agent or work in this repository as an agent | [Agent guide](AGENTS.md) |
| Change an agent workflow | `betteroff.finance/plugins/betteroff/skills/<name>/SKILL.md`; see [Agent workflow sources](#agent-workflow-sources) |
| Prepare directory submissions | [Directory guide](integrations/directories/README.md) |
| Build and validate the Zapier integration | [Zapier private preview guide](integrations/zapier/README.md) |
| Investigate Glama's OAuth callback | [Glama status](integrations/directories/README.md#glama) |
| Report a vulnerability | [Security policy](SECURITY.md) |
| Check client artwork attribution | [Logo sources](assets/clients/README.md) |

Edit the document that owns the information:

- Use the root README to help readers choose a client or workflow.
- Keep each client’s setup, sign-in, troubleshooting, and test limits in `docs/clients/<client>.md`. Group related apps and command-line tools in that guide.
- Keep shared capabilities, permissions, approval rules, and data limits in `docs/connector.md`.
- Keep submission fields and publication status in the directory guide. Keep dated test logs, request IDs, and deployment records in the dated evidence files beside the JSON results.
- Keep the tool catalog in `tools.json`. Run `python3 scripts/tools_catalog.py` to regenerate `docs/tools.md`.
- Link to these documents from the packaged README instead of copying their contents.

Apply the [functional writing standard](https://github.com/raintree-technology/raintree.standards/blob/main/writing/functional.md) when editing documentation. Put prerequisites before numbered steps and state how readers can check the result. Preserve exact commands, permissions, and qualifications.

Use relative links between repository documents and local assets. Link to a section when readers need a specific procedure. Keep absolute GitHub links in the packaged plugin README because installed copies do not include the repository’s documentation. Keep logos outside headings so heading anchors remain stable, and use empty image alternatives when nearby text names the client.

Show each client's test status in one line before its setup steps, and keep the details in the guide's **Verification and sources** section. Distinguish private tests, unsubmitted drafts, approval status, and published metadata. Do not upgrade a status without dated evidence for that destination.

### Client status vocabulary

Each client guide's status line uses one of these levels, from the strongest:

| Level | Status line | Meaning |
| --- | --- | --- |
| Full lifecycle | **Tested:** full lifecycle | Installation, skill loading, consent, scoped discovery, populated and missing-data reads, correction preparation, token renewal, and denial after disconnection all passed. No client has reached this level. |
| Partial | **Tested:** sign-in and synthetic reads | Authenticated reads passed with a synthetic household; part of the lifecycle remains untested. |
| Installation only | **Tested:** installation only | The plugin or extension installed and skills loaded; sign-in and reads remain untested. |
| Untested | **Not yet tested** | The guide follows vendor documentation; no BetterOff sign-in has completed. |

Date official-source reviews separately from BetterOff tests. A documentation review does not verify a working connection. Preserve earlier test dates and limits when adding new evidence.

`todo-mcp.txt` and `.private/` are ignored local operational material. Keep credentials and private reviewer material out of public documentation.

## Agent workflow sources

`betteroff.finance` owns the plugin manifests, skills, agent metadata, and ChatGPT package generator. This repository distributes them. Root `skills/` mirrors the plugin skills for Gemini CLI. Both distributions need complete, standalone workflows, including their interpretation and approval rules.

Maintainers need sibling checkouts of `betteroff.finance` and `betteroff.connectors`. Contributors without finance access should describe the proposed plugin change in an issue so a maintainer can apply it at the source.

1. Review both working trees. Reconcile connector-only plugin changes in finance before syncing so they are not overwritten.
2. In finance, edit `plugins/betteroff/skills/<name>/SKILL.md` and its `agents/openai.yaml` when applicable. Edit manifests under `plugins/betteroff/` and the ChatGPT generator at `tools/connectors/package-chatgpt.py`. Wrap transfer-only text in `<!-- transfers -->` and `<!-- /transfers -->` lines; the ChatGPT package removes those blocks.
3. From finance, run `bun tools/connectors/sync-public.ts ../connectors`, then repeat with `--check`. This updates the distributed plugin, root Gemini metadata and skills, marketplace manifests, and `scripts/package_chatgpt.py`.
4. When shared rules change, update them in each applicable finance skill and align this repository's `scripts/core_rules.md` with those rules. Run `python3 scripts/sync_skills.py --check` here to verify the mirror. Do not run its write mode with stale rules: it overwrites the distributed skills. `household-review` has its own fuller rules.
5. Run the package audit below. CI checks every distributed file, including agent metadata. Review unexpected files manually; the finance sync command refuses to remove target-only plugin files.

Keep both copies as regular files. Do not replace a workflow with a link to another skill: clients can install each workflow independently.

## Contribution checks

Changes reach `main` only through squash-merged pull requests. A repository ruleset with no bypass blocks force-pushes and deletion, requires signed commits, linear history, and resolved review threads, and requires the `package`, `analyze (python)`, `analyze (actions)`, and `review` checks to pass on an up-to-date branch.

The **Audit** workflow in `.github/workflows/audit.yml` runs two jobs:

- **`package`** runs on pull requests, pushes to `main`, and manual runs. It tests and runs the public-content, package, skill-sync, and tool-catalog audits, scans the full Git history with gitleaks, and validates the marketplace and the plugin with `claude plugin validate --strict`.
- **`server`** runs daily and on manual runs. It checks the live MCP endpoint's OAuth discovery, token rejection, HTTPS redirect, HSTS, and CORS behavior, and compares `tools.json` with the tool operations in the public OpenAPI document. A scheduled failure opens or updates a **Scheduled server audit failed** issue, and the next passing scheduled run closes it. The job does not run on pull requests, so a server outage cannot block a merge.

To run the same checks before you open a pull request, run these commands from the repository root. The server check needs `curl` and `jq`.

```sh
python3 scripts/test_audit_public.py && python3 scripts/audit_public.py
python3 scripts/test_audit_package.py && python3 scripts/audit_package.py
python3 scripts/test_package_chatgpt.py
python3 scripts/test_sync_skills.py && python3 scripts/sync_skills.py --check
python3 scripts/test_tools_catalog.py && python3 scripts/tools_catalog.py --check
python3 scripts/test_audit_server.py
gitleaks git --redact --no-banner .
claude plugin validate --strict . && claude plugin validate --strict plugins/betteroff
scripts/audit_server.sh && python3 scripts/tools_catalog.py --live
```

Two more workflows run on pull requests. Each job has no token permissions beyond the ones it declares.

- **CodeQL** (`.github/workflows/codeql.yml`) scans the Python scripts and the workflows with the `security-extended` queries. It also runs on pushes to `main` and weekly.
- **Dependency review** (`.github/workflows/dependency-review.yml`) fails a pull request that adds a dependency, including a GitHub Action, with a known vulnerability of moderate severity or worse.

`audit_server.sh` exits with status 2 and a single `SKIP` line when the runner cannot resolve the API host or its proxy (curl exit 5 or 6). That result is a network problem, not a server regression. A timeout, refused connection, or TLS failure exits with status 1 as a server failure.

Dependabot proposes GitHub Actions updates weekly and waits seven days after each release. Update the other two pinned tools by hand in `audit.yml`:

- **gitleaks:** change `GITLEAKS_VERSION` and `GITLEAKS_SHA256` together. Take the hash from the `linux_x64` line of the release's `checksums.txt`.
- **Claude Code:** change `CLAUDE_CODE_VERSION` and `CLAUDE_CODE_SHA256` together, and confirm that `--strict` validation still passes. The job downloads the `@anthropic-ai/claude-code-linux-x64` tarball from the npm registry without running install scripts. Take the hash with `curl -fsSL <dist.tarball> | sha256sum`, and check that the tarball's SHA-512 matches `npm view @anthropic-ai/claude-code-linux-x64@<version> dist.integrity`. Pick a release at least three days old.

## Releases

Update plugin versions in finance and sync them here before updating `tools.json`. Keep the version equal in `plugins/betteroff/plugin.json`, its Claude and Cursor manifests, `gemini-extension.json`, and `tools.json`; the package audit checks them. `tools.json` records the hosted API version separately as `serverVersion`; the live catalog check compares that field with OpenAPI. `integrations/directories/server.json` carries the Registry record's own version, which rises for each Registry republish, including metadata-only changes. After the release merges to `main`, tag it as `v<version>` and publish a GitHub release.

## ChatGPT submission package

**Approved October 22, 2026; version 0.5.2 published and listed publicly November 2, 2026.** A generated ZIP is not an approved directory integration.

Generate the ChatGPT ZIP separately from the shared client plugin:

```sh
python3 scripts/package_chatgpt.py /tmp/betteroff-chatgpt.zip
```

The generator uses `https://api.betteroff.finance/mcp`, the URL fixed at OpenAI registration. It removes transfer tools and transfer instructions from the ZIP. The generator documents a server restriction for the verified ChatGPT client; verify that restriction through an authenticated ChatGPT test before uploading for review. Package filtering alone does not establish server enforcement.

## Client verification

Earlier HTTP checks with synthetic data covered the tool catalog, permission enforcement, correction review and undo, token rotation, and denied access after disconnection. These server checks do not verify each client’s behavior.

Full client verification must cover installation, skill loading, consent,
permitted tool discovery, populated reads, missing-data responses, correction
preparation, token renewal, and denial after disconnection. Record the client
version, package revision, and test date when publishing results.

Check the [directory guide](integrations/directories/README.md) for publication status and directory acceptance tests. Installing this repository does not mean BetterOff is available in the ChatGPT or Claude connector directories.

### Instinct

An Instinct connection is not yet verified. On October 6, 2026, [Instinct's public site](https://instinct.com/) provided no custom MCP setup instructions, and its account app required phone sign-in before settings could be inspected. Instinct's ability to operate applications does not establish support for this connector.

Before documenting an installation route:

1. Confirm a custom MCP connection option in Instinct account settings or obtain official integration instructions.
2. Connect the endpoint using OAuth and approve the intended household and permissions in BetterOff.
3. Discover the permitted tools and run `betteroff_get_setup_status`, then `betteroff_get_overview`, against a synthetic household.
4. Verify token renewal and denied access after disconnecting in BetterOff.

Do not claim Instinct support until those checks pass. Do not paste BetterOff credentials or access tokens into an Instinct conversation.

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
