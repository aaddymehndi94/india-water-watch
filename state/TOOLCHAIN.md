# G0 toolchain · 24 September 2026

- Ubuntu Linux 6.8, x86_64; Git repository initially clean at `6f3ddca`.
- Codex CLI `0.156.1`. Project `.codex/config.toml` and standalone `.codex/agents/*.toml` match the current [official subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference). The present session exposes native custom roles. No global config was changed. Live parent permissions may override a custom role's read-only default; path ownership and independent review remain necessary.
- Node `22.17.1`, npm `11.6.0`, Python `3.12.3`. Astro's [install guide](https://docs.astro.build/en/install-and-setup/) requires Node 22.12 or newer. `pnpm` was absent; `npm exec --package=pnpm@12.6.0 -- pnpm` runs a project-pinned CLI without a global install.
- Registry versions checked on 24 September: Astro 7.3.4, React 19.3.0, `@astrojs/react` 7.0.0, Tailwind 4.3.3, Pagefind 1.5.2, D3 7.9.0, TypeScript 6.0.3. Exact versions and transitive integrity hashes are in `package.json` / `pnpm-lock.yaml`. `@astrojs/check` does not accept TypeScript 7, so 6.0.3 was selected. Peer check passes.
- Tailwind 4 uses `@tailwindcss/vite` per the current [Astro styling guide](https://docs.astro.build/en/guides/styling/). pnpm 12 requires explicit esbuild build-script approval; `pnpm-workspace.yaml` allowlists only esbuild.
- Source access: official IMD pages and npm registry reachable. `git ls-remote origin refs/heads/main` returned no remote branch. `gh` CLI is absent. Git remote exists at `git@github.com-aaddymehndi94:aaddymehndi94/india-water-watch.git`.
- Starter validation passed; 60 Python unit tests passed on this machine. Those checks do not verify reporting or the app.

Repeat install: `npm exec --yes --package=pnpm@12.6.0 -- pnpm install --frozen-lockfile`.
