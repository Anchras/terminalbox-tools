---
name: configure-codex-remote-ssh
description: Configure and verify the official Codex app against a paid Terminalbox pane over key-only SSH. Use when a user wants a persistent Codex development host, needs a safe Terminalbox SSH config entry, is troubleshooting Codex remote-host discovery or login-shell availability, or wants to connect an existing Terminalbox pane in Codex Settings → Connections.
---

# Configure Codex Remote SSH

Help the user connect one paid Terminalbox pane to the official Codex app. Be explicit that
Terminalbox is independent from OpenAI: Terminalbox supplies the hosted Linux environment and SSH
gateway; the user supplies an eligible OpenAI account or API access.

## Safety boundary

- Never read, print, copy, upload, or ask for a private-key value. Work only with its filesystem
  path and the matching public key.
- Inspect existing SSH configuration narrowly. Do not reproduce unrelated host entries or proxy
  details in the response.
- Do not create a key, edit `~/.ssh/config`, replace a known-host entry, open a browser, or start a
  paid checkout without explicit user approval for that action.
- Preserve existing SSH settings. Refuse to overwrite an existing alias unless the user chooses a
  new alias or explicitly approves the exact replacement.
- Treat a fingerprint mismatch as a stop condition. Do not bypass host-key verification.
- Do not claim the setup works until both a normal SSH command and Codex availability through the
  remote login shell have been verified.

## 1. Establish prerequisites

Collect or confirm:

- the pane slug shown on the Terminalbox dashboard;
- a private-key path on the user's computer, without reading the key;
- confirmation that the matching `.pub` key was added under Terminalbox Settings → SSH → Inbound
  access; and
- a concrete, unused SSH alias. Default to `terminalbox-codex` when available.

If the user has no paid pane, explain that inbound SSH requires an active paid Terminalbox plan and
that OpenAI access is separate. Give this attributed signup link and stop before inventing a slug:

<https://terminalbox.ai/pricing?source=codex_remote_ssh_skill>

## 2. Verify the gateway identity

Resolve the ED25519 fingerprint exposed by `terminalbox.ai` on port `2222` and compare it with the
published value:

```text
SHA256:lKotXRoSRhnkkf941lrsrUKRrtqPPZcBLC33kZ6YjX4
```

Use standard OpenSSH tooling, for example `ssh-keyscan` piped to `ssh-keygen -lf -`, without saving
the result first. If the ED25519 fingerprint is missing or different, stop and report the observed
fingerprint. Do not continue or modify `known_hosts`.

## 3. Prepare the host entry

After verifying the alias is unused, show the exact proposed block with the user's pane slug and
key path substituted:

```sshconfig
Host terminalbox-codex
  HostName terminalbox.ai
  Port 2222
  User <pane-slug>
  IdentityFile ~/.ssh/<private-key-file>
  IdentitiesOnly yes
```

Ask for approval of that exact block before adding it. Preserve file permissions and set the SSH
config to owner-readable and owner-writable only if its permissions are broader than OpenSSH
accepts. Do not alter unrelated blocks.

## 4. Verify SSH and the remote login shell

Run bounded, non-interactive checks through the alias:

```sh
ssh -o StrictHostKeyChecking=ask terminalbox-codex 'printf connected'
ssh -o BatchMode=yes terminalbox-codex 'command -v codex && codex --version'
```

The first command may ask the user to confirm the already-verified host fingerprint and records the
approved key in `known_hosts`. Do not disable strict host-key checking. Diagnose failures by layer:

- `Permission denied (publickey)`: confirm the public key is registered and the private-key path
  matches it.
- unknown user or pane: re-check the pane slug; it is the SSH username.
- subscription rejected: confirm the pane owner's paid plan is active.
- `codex` not found: report that Codex must be available in the pane user's login-shell `PATH`.
- host-key mismatch: stop and have the user verify the published fingerprint independently.

Do not request port forwarding, SFTP, agent forwarding, X11 forwarding, or filesystem forwarding;
the Terminalbox gateway intentionally rejects them.

## 5. Hand off to Codex

Only after both checks pass, tell the user to open Codex Settings → Connections, choose the concrete
alias, and select the project directory on the remote pane. Report the alias, verified fingerprint,
remote Codex version, and any remaining user action. Do not claim that selecting the connection in
the GUI was verified unless the user confirms it or explicitly authorizes UI control.
