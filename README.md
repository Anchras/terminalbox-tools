# Terminalbox tools for remote agent work

Open, inspectable agent skills for deciding when persistent development infrastructure is useful
and connecting the official Codex app to it safely.

## Configure Codex Remote SSH

`configure-codex-remote-ssh` prepares one concrete SSH host entry for a paid Terminalbox pane,
verifies the published gateway fingerprint, tests that Codex is available through the remote login
shell, and hands the verified alias off to Codex Settings → Connections.

The skill never reads, copies, or uploads a private key. It does not create a Terminalbox account,
start a paid subscription, or change SSH configuration without the user's explicit approval.

Install it with any compatible Agent Skills client:

```sh
npx skills add Anchras/terminalbox-tools --skill configure-codex-remote-ssh
```

Review the
[`SKILL.md`](https://github.com/Anchras/terminalbox-tools/blob/main/plugins/codex-remote-ssh/skills/configure-codex-remote-ssh/SKILL.md)
before installing. Terminalbox hosting starts at €6/month; OpenAI access is separate.

[See setup details](https://terminalbox.ai/codex-hosting), or
[start Base for €6/month](https://terminalbox.ai/pricing?source=codex_remote_ssh_skill).

## Remote Workspace Fit

`workspace-fit` is a free, read-only repository audit. It recommends exactly one of three paths:

- use a rebuildable remote-agent task;
- use a persistent development workspace when live processes or interactive state justify it; or
- gather more evidence before choosing infrastructure.

The audit remains provider-neutral. It has no scripts, hooks, MCP servers, telemetry, network
calls, or required service integration.

Install it with any compatible Agent Skills client:

```sh
npx skills add Anchras/terminalbox-tools --skill workspace-fit
```

[Review the indexed skill, install count, and security scans on
skills.sh.](https://www.skills.sh/anchras/terminalbox-tools/workspace-fit)

## Client-native plugin installs

GitHub Copilot CLI:

```sh
copilot plugin install Anchras/terminalbox-tools:plugins/codex-remote-ssh
copilot plugin install Anchras/terminalbox-tools:plugins/remote-workspace-fit
```

Claude Code:

```sh
claude plugin marketplace add Anchras/terminalbox-tools
claude plugin install codex-remote-ssh@terminalbox-tools
claude plugin install remote-workspace-fit@terminalbox-tools
```

## Trust boundary

All skill instructions are plain text in this repository. Review the source and your agent
client's permissions before use. Repository and SSH configuration context is handled by the
installed client under its existing provider settings and is not sent to the plugin author.

## License

MIT. See [`LICENSE`](./LICENSE).
