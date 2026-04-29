# Data Notice

This repository is an independent portfolio case study based on OECD-derived data related to treaty-based withholding tax rates.

## Source

Main source used for the global build:

> OECD, Treaty-based withholding tax rates, OECD Data Explorer / OECD Corporate Income Tax Rates Database.

The raw export used during development was obtained through the OECD Data Explorer using the dataset identifier visible in the original download path:

OECD.CTP.TPS / DSD_WHT@DF_WHT_TREATY / version 1.0

Original Data Explorer URL used during development:

https://data-explorer.oecd.org/vis?pg=0&bp=true&snb=14&tm=Treaty&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_WHT%40DF_WHT_TREATY&df[ag]=OECD.CTP.TPS&df[vs]=1.0

The OECD Data Explorer interface and dataset URLs may change over time. Users should verify the current official source, metadata, access conditions and citation requirements directly through the OECD Data Explorer.

## Public repository policy

This repository does not intentionally redistribute the full original raw OECD export in the current public branch.

Instead, it provides:

- scripts used to process the source export;
- derived processed datasets;
- network tables;
- charts and visual outputs;
- documentation of the analytical workflow;
- a checksum manifest for local reproducibility checks.

## Attribution and reuse

OECD data may be subject to the OECD Terms and Conditions and to dataset-specific restrictions or third-party rights.

Users remain responsible for checking the relevant metadata, source tab and applicable restrictions before reusing or redistributing data.

## Independence disclaimer

This project is independent and is not affiliated with, endorsed by, or approved by the OECD.

The analysis describes the structure of treaty-based relationships between jurisdictions as a network. It does not assess the legal quality, tax convenience, economic effectiveness or practical impact of individual tax treaties.

Nothing in this repository should be interpreted as legal, tax, financial or investment advice.
