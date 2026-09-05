# Contributing

## Change workflow

1. Describe the component, problem, and intended change in a GitHub issue or pull request. Identify dimensions and affected variants.
2. Create a branch for the change. Use a new `variant_*` directory for a different design concept; use Git commits for refinements to an existing variant.
3. Update manufacturing exports, component instructions, and parts lists together. Publish revised `.shapr` sources to the project's GCS bucket if you have maintainer access, then refresh download tables. Git does not store those source files.
4. Record physical validation evidence in [Validation Status](docs/validation.md), identifying the variant and exact commit tested. Keep untested changes marked experimental.
5. Run the checks below and summarize their results in the pull request. Automated checks do not validate hardware strength or quick-release operation.
6. Have the maintainer review the change before merging. When publishing a release, identify its Git commit, component variants, cloud source hashes, and validation limitations in the release notes.

## Local setup and checks

Install hooks from the repository root:

```bash
./scripts/hooks/install_hooks.sh
```

Run the local documentation and hook checks:

```bash
python3 check_links.py
bash -n scripts/hooks/install_hooks.sh scripts/hooks/pre-commit.sh
```

The pre-commit hook can stage entire READMEs when their generated download tables change. Review the staged diff before committing. Cloud asset synchronization is a separate manual operation described in [Scripts](scripts/README.md).

Contributions must be compatible with the repository's [CC BY-NC 4.0 license](LICENSE.md).
