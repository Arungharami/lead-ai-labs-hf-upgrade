# Security Policy

## Protected information

Never commit, upload, paste, or log:

- Kaggle access tokens;
- ARC API keys;
- Hugging Face tokens;
- private competition data;
- private leaderboard outputs;
- personal or institutional credentials.

The supported Kaggle token location is:

```text
.runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
```

The entire `.runtime/` directory is ignored by Git.

## Required token permissions

On Unix-like systems:

```bash
chmod 600 .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
```

Run:

```bash
python3.12 scripts/preflight.py --require-token
```

The preflight checks token shape and permissions without printing the token.

## Suspected credential exposure

1. Revoke the exposed token immediately in the provider's settings.
2. Create a replacement token.
3. Remove the secret from the working tree.
4. If committed, purge it from Git history using an approved history-rewrite tool.
5. Re-run the secret scan and all CI gates.
6. Document the incident without reproducing the secret.

Deleting a secret from the latest commit is not sufficient when it remains in
Git history.

## Dependency and upstream risk

The project pins the official starter, official agent framework, ARC toolkit,
and Kaggle CLI. Changes to those locks require:

- a dedicated pull request;
- official-runtime smoke validation;
- notebook regeneration;
- local verification;
- a documented experiment or maintenance reason.

## Reporting

Open a private security report through the repository's GitHub Security tab
when available. Do not open a public issue containing credentials, exploit
details, or private competition artifacts.
