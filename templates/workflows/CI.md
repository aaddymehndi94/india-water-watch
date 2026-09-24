# CI implementation specification (not an enabled workflow)
Codex creates the actual YAML after resolving the real package commands and verifying current official action SHAs and platform syntax.

Run on trusted branch pushes and pull requests with read-only permissions by default. Install frozen dependencies and run type/schema/reference/unit/end-to-end checks against production builds. Test a root prefix and a repository prefix. Save source-free test evidence and screenshots within a bounded artifact retention policy. Do not publish on a pull request.

Pin third-party actions to reviewed immutable commit SHAs. Untrusted fork code must receive no publication credentials. Do not use `pull_request_target` to execute a contributor's code with secrets. Keep source-adapter network refresh separate from deterministic fixture CI. Do not treat a cached test report as proof that a changed release passed.
