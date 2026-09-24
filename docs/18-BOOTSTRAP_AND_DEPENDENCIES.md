# 18 · Cross-platform bootstrap

The starter itself needs only Python standard library for its checks. The site is deliberately not bootstrapped with guessed dependency versions. Codex performs this once at G0 using current official documentation and the local environment.

## Inspect first

Run safe version checks for Git, Codex, Node, package manager and Python. Detect Windows/Linux/macOS and shell. Inspect current repo and preserve user changes. Check whether the Node runtime meets the chosen current Astro release's minimum requirement; do not assume the machine's installed version does. Review current React/Tailwind/Astro integration instructions. Record results and installed versions.

## Install policy

Use a project-local environment/lockfiles. Verify package identity and stable compatibility before installing. Prefer the documented current Node LTS compatible with the selected framework, but do not silently change the user's global runtime. Explain genuine manual installation/privilege barriers and continue other safe work. No arbitrary `curl | sh` from untrusted sites.

Choose a specific pnpm version and record it in `packageManager`; create `pnpm-lock.yaml`. Choose a supported Python version, isolate it and freeze dependencies through a reviewed tool such as uv. If a system package or native geospatial dependency would complicate the setup, first test whether a simpler format/library suffices. Do not require GPU/cloud compute.

## Codex agent config

Read the project's `.codex` files and verify their format against the installed CLI. The starter uses a minimal concurrency configuration and standalone custom-agent files, with no pinned model. OpenAI's source links are listed in the technical registry. Adapt project configuration only when necessary and record the reason. Never overwrite `~/.codex/config.toml` without explicit permission.

## Required bootstrap evidence

`state/TOOLCHAIN.md` with tool/version/source/date; lockfiles; dependency-license/security review; tested `pnpm dev` and `pnpm verify` interface; OS-specific notes only where needed. Do not report a command works unless it actually ran or label it clearly as not tested.

## Commands for the current starter

```text
python tools/validate_starter.py
python -m unittest discover -s tests -v
python tools/release_gate.py
```

The release gate initially rejects the pack because there is no built publication. That failure is intentional. Do not “repair” it by editing approval flags or creating empty passing reports. Implement the real site and collect real review evidence.
