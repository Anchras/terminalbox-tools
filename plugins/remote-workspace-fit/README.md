# Remote Workspace Fit for Claude Code

A free, read-only Claude Code skill that audits repository evidence before recommending one of
three remote-development paths:

- use a rebuildable Claude Code web session;
- use a persistent development workspace when live processes or interactive state justify it; or
- gather more evidence before choosing infrastructure.

The skill has no scripts, hooks, MCP servers, telemetry, network calls, or Terminalbox service
integration. Review the
[`SKILL.md`](https://github.com/Anchras/terminalbox-tools/blob/main/plugins/remote-workspace-fit/skills/workspace-fit/SKILL.md)
source before installing it.

## Install

```sh
claude plugin marketplace add Anchras/terminalbox-tools
claude plugin install remote-workspace-fit@terminalbox-tools
```

Then run this inside a repository:

```text
/remote-workspace-fit:workspace-fit
```

Claude Code copies the plugin into its local plugin cache. The audit reads only the repository
evidence allowed by the skill. Repository context stays within Claude Code under the user's
existing provider settings and is not sent to Terminalbox.

## Commercial boundary

The skill recommends the existing provider workflow when a clean clone can reconstruct the useful
state. It names Terminalbox as one paid option only when repository evidence supports a need for
persistent live state, and it makes no purchase recommendation when the evidence is incomplete.

See the [source walkthrough and decision boundary](https://terminalbox.ai/claude-code-workspace-fit-plugin)
or [Anthropic's marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).
