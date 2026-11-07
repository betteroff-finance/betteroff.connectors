<img src="assets/icon.png" alt="" width="40" height="40" align="absmiddle">

# BetterOff plugin

Review household finances and prepare corrections for approval in BetterOff.

Install in Claude Code 2.1.275 or later from inside a session:

```
/plugin install betteroff --marketplace betteroff-finance/betteroff.connectors
```

For Codex and other clients, follow the [client setup guides](https://github.com/betteroff-finance/betteroff.connectors#install-the-connector). Each guide states what has been tested for that client. See the [tool reference](https://github.com/betteroff-finance/betteroff.connectors/blob/main/docs/tools.md) for every tool's access and scopes.

This package contains portable Agent Plugins manifests (`plugin.json` and `mcp.json`), client compatibility manifests, and eight standalone workflow skills. It contains no credentials or local server. The client manages OAuth credentials after you approve access.

To change the plugin, follow the [contributor guide](https://github.com/betteroff-finance/betteroff.connectors/blob/main/CONTRIBUTING.md).
