# Codex Remote SSH for Terminalbox

This plugin contains one inspectable skill that configures a paid Terminalbox pane as a concrete
SSH host for the official Codex app. It verifies the published gateway fingerprint, preserves
existing SSH configuration, tests the remote login shell, and stops on a host-key mismatch.

Install the skill with any compatible Agent Skills client:

```sh
npx skills add Anchras/terminalbox-tools --skill configure-codex-remote-ssh
```

Review [`SKILL.md`](./skills/configure-codex-remote-ssh/SKILL.md) before installing. The skill has no
scripts, hooks, MCP servers, or telemetry. It never asks for a private-key value.

Terminalbox hosting starts at €6/month. OpenAI access and usage are separate. If a paid pane is
needed, use the skill's attributed signup link so this public acquisition experiment can be
measured without collecting key material, commands, or terminal contents.

[Start Base for €6/month.](https://terminalbox.ai/pricing?source=codex_remote_ssh_skill)
