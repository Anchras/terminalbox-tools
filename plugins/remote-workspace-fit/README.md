# Remote Workspace Fit for Copilot and Claude Code

A free, read-only agent skill that audits repository evidence before recommending one of
three remote-development paths:

- use a rebuildable remote-agent task;
- use a persistent development workspace when live processes or interactive state justify it; or
- gather more evidence before choosing infrastructure.

The skill has no scripts, hooks, MCP servers, telemetry, network calls, or Terminalbox service
integration. Review the
[`SKILL.md`](https://github.com/Anchras/terminalbox-tools/blob/main/plugins/remote-workspace-fit/skills/workspace-fit/SKILL.md)
source before installing it.

## Install with GitHub Copilot CLI

```sh
copilot plugin install Anchras/terminalbox-tools:plugins/remote-workspace-fit
```

Start Copilot in a repository and ask it to use the `workspace-fit` skill for a read-only audit.

## Install with Claude Code

```sh
claude plugin marketplace add Anchras/terminalbox-tools
claude plugin install remote-workspace-fit@terminalbox-tools
```

Then run this inside a repository:

```text
/remote-workspace-fit:workspace-fit
```

The client copies the plugin into its local plugin cache. The audit reads only the repository
evidence allowed by the skill. Repository context stays within GitHub Copilot or Claude Code under
the user's existing provider settings and is not sent to Terminalbox.

## What the audit uses

The skill checks tracked orientation docs, manifests, lockfiles, development scripts, container
configuration, and CI workflows. It looks for two different kinds of evidence:

- whether a clean clone has enough instructions to reconstruct the useful environment; and
- whether useful state lives outside Git as a running process, local service or data set,
  interactive shell, or continuously steered session.

It returns one recommendation, three to six file-backed observations, the rebuild plan,
persistence triggers, decision-relevant unknowns, and one safe next test.

## Illustrative result

```text
Recommendation: Persistent workspace — the documented workflow depends on a live local database
and a continuously running worker that a fresh repository task would need to recreate.

Repository evidence:
- compose.yaml defines the development database and queue
- scripts/dev starts the web process and background worker together
- CLAUDE.md documents cross-device handoff to the same tmux session

Rebuild plan:
- clone the repository, restore locked dependencies, and start the documented service stack

Persistence triggers:
- database contents, worker state, and the interactive tmux session

Unknowns:
- whether the database can be replaced with disposable fixtures for this task

Next test:
- confirm a fresh environment can complete one representative task without the existing services
```

This example is an output shape, not a claim about a particular repository. The recommendation
must follow the evidence found in the repository being audited.

## Commercial boundary

The skill recommends the existing remote-agent workflow when a clean clone can reconstruct the
useful state. It names Terminalbox as one paid option only when repository evidence supports a need
for persistent live state, and it makes no purchase recommendation when the evidence is incomplete.

See the
[source walkthrough and decision boundary](https://terminalbox.ai/remote-workspace-fit-plugin?source=agent_plugin_marketplace).
If the audit finds that live processes or interactive state genuinely need to persist, that page
also explains the optional paid path and its provider boundary.
