# Releases and automatic PyPI publishing

The package version has one source: `[project].version` in `pyproject.toml`.
`advancedprinter.__version__` reads installed distribution metadata.

## One-time setup for the existing PyPI project

Sign in as an owner of the AdvancedPrinter PyPI project. Under **Your projects →
AdvancedPrinter → Manage → Publishing**, add a GitHub Trusted Publisher:

| Field | Value |
|---|---|
| Owner | `kbkozlev` |
| Repository | `AdvancedPrinter` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

The workflow filename is the basename, not `.github/workflows/publish.yml`.
Create the `pypi` environment in GitHub repository **Settings → Environments**.
Keep the name identical on both sides. An environment may require a reviewer
if you want an additional release approval step; with no required reviewer,
publishing proceeds automatically after validation.

Trusted Publishing uses short-lived OIDC credentials. No PyPI password or API
token belongs in the repository or its secrets. The publishing job alone has
`id-token: write`; builds and tests use read-only repository permissions.

Official references:

- https://docs.pypi.org/trusted-publishers/adding-a-publisher/
- https://docs.pypi.org/trusted-publishers/using-a-publisher/

## Publish a release

1. Update `pyproject.toml` and add release notes to `CHANGELOG.md`.
2. Run the local checks in `CONTRIBUTING.md`, then merge the change after CI passes.
3. Create a GitHub Release from that tested commit with a matching tag, e.g.
   `v2.0.0` (the unprefixed `2.0.0` form is also accepted).
4. Publish the release. A draft does not upload anything.
5. Check the **Publish to PyPI** run, then verify the version on PyPI and install
   it in a fresh environment.

The release workflow calls the same CI workflow: 15 OS/Python combinations,
format/lint/type checks, a wheel and source build, strict metadata validation,
wheel installation, and a wheel rebuilt from the source distribution. In parallel,
`check_release.py` requires the release tag to match installed package metadata.
The final upload job downloads the already-built `distributions` artifact; it
has no source checkout and does not rebuild the package. Any failed prerequisite
blocks publishing. Third-party actions are pinned to commit SHAs and Dependabot
proposes updates.

GitHub prereleases follow the same path to PyPI: use a PEP 440 prerelease version
such as `2.1.0rc1` with tag `v2.1.0rc1`. A GitHub prerelease flag alone does not
change the Python package version. Ordinary pushes and pull requests only test
and build; they never publish to PyPI.

## Troubleshooting

- **Invalid publisher:** match owner, repository, `publish.yml`, and environment
  exactly. Confirm the publisher is registered on PyPI, not only TestPyPI.
- **Tag mismatch:** fix the package version/tag before publishing. The check is
  intentionally strict, including the prerelease suffix.
- **Version already exists:** PyPI does not allow replacing an uploaded file.
  Publish a new version; do not delete and try to reuse the old version.
- **Partial upload:** inspect the PyPI files and workflow log before retrying.
  The workflow does not silently skip existing files.
- **A failed release:** fix the failure and rerun appropriate jobs where safe.
  Upload is only allowed after all validation jobs succeed.

## TestPyPI (optional)

The production release workflow does not require TestPyPI. To test publishing
there, register a separate Trusted Publisher on TestPyPI with its own GitHub
environment and use the official publishing action with
`repository-url: https://test.pypi.org/legacy/` in a separate workflow. TestPyPI
accounts and publisher configuration are independent of PyPI.
