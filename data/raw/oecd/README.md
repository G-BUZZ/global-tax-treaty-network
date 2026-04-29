# OECD raw source exports

The original OECD-derived export used for the build is kept locally and excluded from Git tracking.

Reason:

- the raw export may be useful for auditability and reproducibility;
- the public portfolio should avoid redistributing complete third-party raw files;
- derived data, code, outputs and documentation are sufficient for public review.

Use `source_manifest.sha256` to verify that a local raw file matches the version used during the build.

## Source availability note

The original OECD Data Explorer URL used during development may change or become temporarily unavailable. Users should verify the current dataset through the OECD Data Explorer or the OECD Corporate Income Tax Rates Database.

The local raw export is not tracked in this public repository. A checksum manifest is provided only to document the source snapshot used during development.
