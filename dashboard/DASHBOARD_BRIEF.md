# Dashboard Brief

## Goal

Build a competitive dashboard that is immediately usable by an EdRAM analyst to compare 2026 outlooks across asset managers.

The dashboard must make it easy to answer three questions:

1. Where does EdRAM align with the market?
2. Where does EdRAM clearly stand out?
3. Which source and evidence support each conclusion?

The dashboard is not meant to be a generic BI tool. It should be a focused comparison product built around EdRAM as the benchmark.

## Primary Data Source

The dashboard should use:

- [`foundation/asset_manager_master.csv`](/Users/milo/Desktop/BDD_EDR/foundation/asset_manager_master.csv)

This file is the canonical one-row-per-manager dataset for the UI.

## Core Product Logic

The dashboard should have **two main experiences**:

### 1. Asset Manager Comparison

Purpose:

- compare EdRAM against one selected competitor
- optionally extend later to compare EdRAM against two competitors
- inspect differences at the indicator level

What this page must do:

- pin `EdRAM` on the left by default
- let the user choose a competitor
- compare macro, positioning, currencies, commodities, and themes
- show source evidence for every usable row
- surface similarity and divergence clearly

### 2. EdRAM vs Consensus

Purpose:

- compare EdRAM against the market view, not just one manager
- show where EdRAM is aligned with consensus
- show where EdRAM is differentiated
- work across macro forecasts, positioning, and themes

What this page must do:

- compute market consensus from all competitors excluding EdRAM
- show consensus strength and coverage
- show whether EdRAM is:
  - aligned
  - different
  - standout
- make this readable by section:
  - macro
  - equities
  - fixed income
  - currencies
  - commodities
  - themes

## Required Features

### Shared Features

- EdRAM always visible as the benchmark
- clear section navigation
- search by indicator or theme
- direct source traceability:
  - page
  - wording
  - PDF link
  - extracted text link
- explicit handling of missing values
- consistent visual language across all sections

### Features For Asset Manager Comparison

- competitor selector
- side-by-side comparison table
- strongest divergences highlighted first
- evidence panel for clicked row
- similarity score based only on overlapping disclosed rows
- optional market matrix to view all managers at once

### Features For EdRAM vs Consensus

- consensus summary cards
- section-level alignment summary
- ranked list of EdRAM standouts
- ranked list of high-alignment areas
- indicator-by-indicator comparison between:
  - EdRAM view
  - consensus view
  - coverage
  - signal strength
- support both:
  - quantitative macro consensus
  - qualitative positioning/theme consensus

## Missing Data Rules

Missing data is a major part of this project and should be handled explicitly, not hidden.

### General Rules

- `ND` should be shown as a muted status, not as an empty blank cell
- rows with missing data should not dominate the screen
- coverage should always be visible so the user knows how strong a comparison really is

### Pairwise Comparison Rules

Rows should be grouped in this order:

1. `Both disclosed`
2. `Only EdRAM disclosed`
3. `Only competitor disclosed`
4. `Both ND`

`Both ND` should be collapsed by default.

### Macro Rules

For macro fields:

- `quantitative` means a numeric comparison is possible
- `qualitative` still counts as usable disclosure
- blank numeric `value` does **not** always mean missing

The UI should rely on `status`, not only on numeric emptiness.

### Consensus Rules

Consensus should only be shown as strong when coverage is good enough.

Examples:

- if a macro metric has enough quantitative peer disclosures, show a market median or central range
- if coverage is weak, show that consensus is weak rather than pretending precision
- for qualitative topics, show the dominant market stance and how many peers support it

## Desired Layout

The dashboard should feel simple and analyst-oriented.

### Top Level Structure

- `Header`
  - title
  - short description
  - high-level coverage stats
- `Left sidebar`
  - page selector
  - section selector
  - competitor selector when relevant
  - search
  - methodology notes
- `Main content area`
  - overview cards
  - standout / alignment blocks
  - main comparison table
  - evidence drawer or side panel

### Page 1: Asset Manager Comparison Layout

- overview row:
  - similarity score
  - overlap count
  - divergence count
- standout cards:
  - biggest splits between EdRAM and selected manager
- comparison table:
  - EdRAM column
  - competitor column
  - signal column
- evidence panel:
  - page
  - why
  - raw wording
  - source links

### Page 2: EdRAM vs Consensus Layout

- overview row:
  - number of aligned items
  - number of standout items
  - consensus coverage
  - strongest conviction areas
- section summary:
  - macro
  - equities
  - fixed income
  - currencies
  - commodities
  - themes
- consensus comparison table:
  - indicator
  - EdRAM
  - consensus
  - coverage
  - signal
  - note
- standout blocks:
  - where EdRAM differs most from the market
- alignment blocks:
  - where EdRAM is most in line with peers

## Design Principles

- easy to use without explanation
- strong defaults
- minimal clutter
- missing data handled honestly
- evidence always close to the insight
- comparison first, not decoration first

## MVP Scope

The MVP should include:

- one page for `EdRAM vs selected asset manager`
- one page for `EdRAM vs consensus`
- section filtering
- source-backed evidence panel
- explicit missing-data handling
- consistent visual system

The MVP does **not** need:

- advanced export
- saved views
- full custom analytics builder
- complex charting library behavior

## Success Criteria

The dashboard is successful if a reviewer can open it and quickly understand:

- what the market consensus is
- where EdRAM is differentiated
- which competitor is closest or farthest
- what evidence supports each statement

## Build Priority

Recommended order:

1. stable data transformation layer
2. asset manager comparison page
3. EdRAM vs consensus page
4. evidence and sourcing polish
5. visual polish and optional charts
