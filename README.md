# Global Tax Treaty Network

Network analysis project that models bilateral tax treaty relationships between jurisdictions using OECD-derived data.

## Overview

Global Tax Treaty Network transforms treaty-related fiscal data into a graph structure in order to study the international tax treaty system as a network.

In this project:
- each jurisdiction is treated as a **node**
- each bilateral treaty relationship is treated as an **edge**

The project began as a manually curated Italy-centered seed network and later evolved into a global build based on OECD-derived data.

## Project Goal

The goal is to map and analyze the structure of the international tax treaty network, identify the most connected jurisdictions, and highlight which countries emerge as major hubs or intermediary nodes in the system.

## Data Source

Primary source used for the global build:
- OECD export related to treaty-based withholding tax rate data

## Network Definition

### Nodes
Each node represents a jurisdiction / country.

### Edges
An undirected edge represents the existence of a bilateral treaty relationship between two jurisdictions in the OECD-derived dataset.

A directed version of the edge list is also generated for cases where directional analysis is useful.

## Current Global Dataset

- **192 nodes**
- **2793 undirected edges**
- **5026 directed edges**

## Main Outputs

### Processed datasets
- `data/processed/global/nodes_global.csv`
- `data/processed/global/edges_global_directed.csv`
- `data/processed/global/edges_global_undirected.csv`
- `data/processed/global/centrality_global.csv`

### Visual outputs
- `visuals/global/global_network_full.png`
- `visuals/global/global_top30_hubs.png`
- `visuals/global/top20_degree_bar.png`

### Supporting documentation
- `docs/global/global_checkpoint.md`
- `docs/global/key_insights.md`
- `docs/global/portfolio_blurb.md`

## Key Findings

Based on the current global network:
- **France** and the **United Kingdom** emerge as the most connected jurisdictions by degree
- **Switzerland** appears highly central, including as an intermediary node
- **Italy** is strongly connected, but does not dominate the global network once the analysis is scaled beyond the Italy-centered seed graph
- the network suggests a structure organized around multiple fiscal hubs rather than a single dominant jurisdiction

## Method Summary

The workflow is:

1. acquire OECD raw export  
2. inspect raw file structure  
3. build node and edge tables  
4. construct the global network  
5. compute centrality metrics  
6. export visual outputs  

## Repository Structure

```text
archive/
data/
  raw/
    oecd/
  processed/
  processed/global/
  intake/

docs/
  global/

scripts/
  global/

visuals/
  global/
```

## Data source and attribution

This project is based on OECD-derived data related to treaty-based withholding tax rates.

Main source:

OECD (2025), Treaty-based withholding tax rates, OECD Data Explorer / OECD Corporate Income Tax Rates Database.

The project is independent and is not affiliated with, endorsed by, or approved by the OECD.

For details, see `DATA_NOTICE.md`.

## Disclaimer

This repository is a portfolio case study in data cleaning, relational modelling, network analysis and visual communication.

The analysis describes the structure of treaty-based relationships between jurisdictions. It does not evaluate the legal quality, tax convenience, economic effectiveness or practical impact of individual treaties.

Nothing in this repository should be interpreted as legal, tax, financial or investment advice.

## License

Code in this repository is released under the MIT License.

Data are based on OECD-derived sources and remain subject to the applicable OECD terms and conditions. See `DATA_NOTICE.md`.
