# Data Notice

This repository contains an independent portfolio case study based on OECD-derived data related to treaty-based withholding tax rates.

The underlying source is the OECD Corporate Income Tax Rates Database, specifically the treaty-based withholding tax rates dataset available through the OECD Data Explorer.

Suggested citation:

OECD (2025), Treaty-based withholding tax rates, OECD Data Explorer / OECD Corporate Income Tax Rates Database.

This project is independent and is not affiliated with, endorsed by, or approved by the OECD.

The analysis, derived network tables, scripts, charts and report are provided for educational and portfolio purposes.

The network describes the structure of treaty-based relationships between jurisdictions. It does not assess the legal quality, tax convenience, economic effectiveness or practical impact of individual tax treaties.

Nothing in this repository should be interpreted as legal, tax, financial or investment advice.

Users should consult the official OECD source and the applicable OECD Terms and Conditions before reusing the original data.

## Raw source export handling

Full raw source exports are not redistributed in this public repository.

The project keeps raw files locally under `data/raw/`, which is excluded from Git tracking. This choice preserves reproducibility while reducing unnecessary redistribution of complete third-party source exports.

Public reproducibility is supported through source attribution, processing scripts, derived outputs and the checksum manifest stored at:

`data/raw/oecd/source_manifest.sha256`

The original source data remain subject to the applicable OECD terms and conditions.
