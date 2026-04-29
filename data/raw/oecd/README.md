# OECD raw source exports

The original OECD-derived export used for the build is kept locally and excluded from Git tracking.

Reason:

- the raw export may be useful for auditability and reproducibility;
- the public portfolio should avoid redistributing complete third-party raw files;
- derived data, code, outputs and documentation are sufficient for public review.

Use `source_manifest.sha256` to verify that a local raw file matches the version used during the build.
