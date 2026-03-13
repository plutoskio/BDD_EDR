# Dashboard Ideas

## Goal

Build a dashboard for Deliverable 1 that lets EdRAM compare competitor 2026 outlooks quickly, visually, and with direct traceability to the original source documents.

The dashboard should help answer three questions:

1. What is the market consensus?
2. Where does EdRAM differ from competitors?
3. Which sources support each conclusion?

## Product Principles

- Keep the interface compact and analyst-friendly.
- Avoid a gallery of disconnected charts.
- Prioritize traceability: every important datapoint should link back to its source.
- Make comparison faster than reading PDFs manually.
- Use one highly flexible charting area rather than many static charts.

## Core Objects

The main comparison object for Deliverable 1 is the asset manager / outlook, not the fund.

- Primary comparison unit: asset manager outlook
- Benchmark unit: EdRAM outlook
- Data types:
  - quantitative forecasts
  - qualitative positioning
  - thematic calls
  - metadata about sources and coverage

Fund comparison becomes more relevant in Deliverable 3, but some design patterns can be reused later.

## Must-Have Features

- Open the original source file for each outlook from inside the dashboard.
- Open the extracted text version from inside the dashboard.
- Compare 2 managers side by side.
- Pin EdRAM as the benchmark in any comparison view.
- Filter by manager, country relevance, macro topic, asset class, and theme.
- Show whether a datapoint is quantitative, qualitative, or not disclosed.
- Search across all outlooks and extracted text.
- Show source traceability for each datapoint.
- Display a structured competitor profile:
  - manager name
  - AUM
  - markets covered
  - source file
  - source type

## Important Analytical Features

- Consensus view:
  - show where most competitors align
  - highlight median / average quantitative expectations
- Divergence vs EdRAM:
  - show where EdRAM is more bullish, more cautious, or uniquely positioned
- Missing data view:
  - show which managers did not publish a given metric
- Coverage quality:
  - show whether the datapoint was directly extracted, manually validated, or missing

## Visual Comparison Features

- Heatmap for bullish / neutral / cautious positioning by manager and topic
- Sortable comparison tables for macro forecasts
- Sortable comparison tables for asset allocation views
- Theme matrix for AI, healthcare, energy transition, geopolitics, defense, and related themes
- Summary cards for numeric dispersion:
  - average
  - median
  - min / max
  - number of managers with disclosed values

## Flexible Charting Area

### Idea

Instead of building many separate charts, create one chart area that users can reconfigure.

Users should be able to choose:

- x-axis variable
- y-axis variable
- color
- point size
- point label
- manager subset

Possible dimensions:

- quantitative metric on x
- quantitative metric on y
- qualitative bucket as color
- conviction level as size
- manager group or geography as filter

### Examples

- `US GDP forecast` vs `EUR/USD forecast`
- `Eurozone growth` vs `Fed terminal rate`
- `China growth view` vs `EM preference`
- `Quantitative forecast` vs `dispersion from consensus`

### Plausibility Check

This is plausible and worth doing, but only if scoped correctly.

Plausible for MVP:

- one scatter / dot chart
- up to 2 numeric axes
- 1 categorical color dimension
- filters and drag/drop field assignment

Risky if attempted too early:

- too many chart types
- fully generic BI-tool behavior
- messy support for qualitative-only data in the same chart
- advanced drag/drop interactions before the data model is stable

Recommended approach:

1. Build one configurable scatterplot first.
2. Restrict it to variables that have enough quantitative coverage.
3. Use separate table views for qualitative data.
4. Add more chart flexibility only after the schema is stable.

So the editable multi-variable chart is a strong idea, but it should be a focused chart builder, not a full custom analytics platform.

## Possible User Flows

### Flow 1: Compare EdRAM vs 2 competitors

- select EdRAM, Manager A, Manager B
- choose a macro topic
- see side-by-side table
- open source PDF or source text

### Flow 2: Find consensus

- choose a metric such as `EUR/USD`
- show all available manager forecasts
- visualize distribution
- identify mean, median, and outliers

### Flow 3: Find EdRAM differentiation

- filter on topic such as `AI`, `healthcare`, or `Europe`
- show where EdRAM differs from the majority
- open supporting source text

## Suggested Information Architecture

- `Overview`
  - market consensus
  - EdRAM divergence
  - coverage summary
- `Competitors`
  - manager cards
  - source files
  - metadata
- `Macro`
  - numeric forecasts
  - flexible chart area
  - comparison table
- `Allocation`
  - equities, fixed income, FX, commodities
- `Themes`
  - AI
  - healthcare
  - energy transition
  - geopolitics / defense
- `Sources`
  - original files
  - extracted text
  - citations / page references

## MVP Recommendation

For a first usable version, prioritize:

1. Source file access
2. Side-by-side manager comparison
3. Filters and search
4. Numeric comparison table
5. One configurable chart for quantitative forecasts
6. EdRAM vs consensus view

## Later Enhancements

- export views to PDF or PowerPoint-friendly snapshots
- save named comparison views
- annotations for validated insights
- country-specific lens for Deliverable 3 reuse
- fund-level comparison mode for the sales recommendation phase
