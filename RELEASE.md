# Release Process

This project follows [Semantic Versioning](https://semver.org) for all published versions.
The change history is maintained in [CHANGELOG.md](CHANGELOG.md).

## Bumping the Version

1. Update `setup.cfg` and `docs/conf.py` with the new version number.
2. Add a new section in `CHANGELOG.md` describing the changes.
3. Commit the updates with a message like `Release vX.Y.Z`.

## Tagging

After committing the version bump, tag the commit so GitHub release pages
align with the changelog:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

Replace `X.Y.Z` with the actual version number.

## Final Checks

Run the full test suite before publishing a release:

```bash
pytest -q
```

Only publish the tag once all tests pass.
