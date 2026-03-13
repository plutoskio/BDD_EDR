# BDD_EDR

This repository is an Edmond de Rothschild Asset Management (EdRAM) case project for 2026 competitive intelligence and country-level sales prioritization.

The core job is split into two phases:

- Phase 1: collect and compare EdRAM's 2026 house view against about 20 competitor outlooks across macro forecasts, asset allocation, and themes.
- Phase 2: turn that macro view into country-by-country sales recommendations for EdRAM funds across France, Germany, Switzerland, Italy, and Spain.

This README is the fast orientation file. Agents should start here instead of opening every file in every folder.

## What Is Already In The Repo

- The business brief is written in [business_case_brief.md](/Users/milo/Desktop/BDD_EDR/business_case_brief.md).
- The most advanced analysis file is [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md). Despite the filename, it is not just competitor selection: it is a structured Step 2 comparison matrix covering EdRAM plus 20 competitors, with macro, allocation, theme, and source-reference tables.
- The grading instructions for the written outputs are in [deliverable_2.md](/Users/milo/Desktop/BDD_EDR/deliverable_2.md) and [deliverable_3.md](/Users/milo/Desktop/BDD_EDR/deliverable_3.md).
- The dashboard folder does not contain an implemented app at this stage. It currently contains product and UX notes in [dashboard/README.md](/Users/milo/Desktop/BDD_EDR/dashboard/README.md).
- The canonical Step 2 manual data foundation now lives in [foundation/README.md](/Users/milo/Desktop/BDD_EDR/foundation/README.md), with a long evidence table, a wide master table, and a macro codebook.
- The raw outlook source pack is stored in [outlooks](/Users/milo/Desktop/BDD_EDR/outlooks).
- Agent-friendly text extractions of that source pack are stored in [outlooks_txt](/Users/milo/Desktop/BDD_EDR/outlooks_txt).
- The extraction pipeline that generated the text mirror lives in [scripts/extract_outlooks.py](/Users/milo/Desktop/BDD_EDR/scripts/extract_outlooks.py).
- A commercial holdings/distribution extract for EdRAM funds is in [Extraction Albert School 20251231.xlsx](/Users/milo/Desktop/BDD_EDR/Extraction%20Albert%20School%2020251231.xlsx).
- Two EdRAM strategy decks are present as [Stratégie d'investissement 2026 FR.pptx](/Users/milo/Desktop/BDD_EDR/Strate%CC%81gie%20d'investissement%202026%20FR.pptx) and [Stratégie d'investissement 2026  UK.pptx](/Users/milo/Desktop/BDD_EDR/Strate%CC%81gie%20d'investissement%202026%20%20UK.pptx).

## Project In One Page

- Sponsor context: this work is for Raphaël Bellaiche, Head of Product Management at EdRAM.
- Target geography: France, Germany, Switzerland, Italy, Spain.
- Competitor scope rule: managers active in at least one target market and above EUR 10bn AUM.
- Phase 1 deliverables:
  - D1 dashboard comparing competitor outlooks
  - D2 exactly 10 strategic insights versus EdRAM
- Phase 2 deliverables:
  - D3 country-by-country sales recommendations with KPIs
  - D4 AI log

## Current State Of The Work

- The source collection step is largely done for Phase 1.
- There are 21 outlook source files in [outlooks](/Users/milo/Desktop/BDD_EDR/outlooks): EdRAM plus 20 competitors.
- The text extraction pass completed successfully for all 21 files, as recorded in [outlooks_txt/manifest.json](/Users/milo/Desktop/BDD_EDR/outlooks_txt/manifest.json).
- [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md) already encodes the main comparison logic needed for D1 and D2:
  - EdRAM benchmark view
  - macro dashboard
  - asset allocation dashboard
  - theme, risk, and contrarian signal dashboard
  - source citations and disclosure-quality markers such as `Q`, `Ql`, and `ND`
- The dashboard itself is still conceptual. [dashboard/README.md](/Users/milo/Desktop/BDD_EDR/dashboard/README.md) is a design brief, not a shipped product.
- The sales-prioritization phase is not yet assembled into a finished report, but the Excel extract provides a strong input for market/fund/client segmentation work.

## Main Analytical Content Already Captured

- EdRAM is positioned as selective rather than broadly bullish.
- Recurrent EdRAM themes across the local materials:
  - AI is important, but crowded U.S. mega-cap AI exposure should be treated cautiously.
  - Europe may surprise positively through Germany, fiscal support, and capital-markets integration.
  - Dollar weakness is a key axis.
  - Gold remains important.
  - Healthcare, resilience, sovereignty/defense, and selective China or EM exposure matter.
- The competitor comparison file already groups firms into direct peers, market giants, and regional or institutional players.
- The comparison is intentionally strict about missing disclosures: if a source does not publish a clean number, the matrix keeps it qualitative or marks it not disclosed rather than inferring precision.

## Data Inventory

### Outlook Corpus

- Folder: [outlooks](/Users/milo/Desktop/BDD_EDR/outlooks)
- Contents: 21 original competitor and benchmark outlook files in PDF or DOCX format.
- Includes: EdRAM, Amundi, AllianzGI, Anima, BNP Paribas AM, Berenberg, BlackRock, Candriam, Carmignac, DWS, EFG, Generali AM, Goldman Sachs AM, JP Morgan AM, Lazard, Lombard Odier, M&G, Oddo BHF AM, Pictet, Santander AM, UBS.

### Text Mirror For Agents

- Folder: [outlooks_txt](/Users/milo/Desktop/BDD_EDR/outlooks_txt)
- Purpose: plain-text mirrors of every file in `outlooks/` so agents can search and cite local text instead of repeatedly parsing PDFs.
- Generation status: 21 successes, 0 failures.
- Extraction methods:
  - PDF: `pypdf` layout extraction
  - DOCX: `pandoc`
- Best starting point for source-backed work: [outlooks_txt/manifest.json](/Users/milo/Desktop/BDD_EDR/outlooks_txt/manifest.json), then the specific `.txt` files.

### Fund Distribution / Commercial Extract

- File: [Extraction Albert School 20251231.xlsx](/Users/milo/Desktop/BDD_EDR/Extraction%20Albert%20School%2020251231.xlsx)
- Structure: one worksheet named `31 12 2025`.
- Main columns observed:
  - `Business Relationship`
  - `Fund`
  - `Share`
  - `ISIN`
  - `Date`
  - `AUM (€)`
  - `BR Segmentation`
  - `Business Country`
- High-level size:
  - 9,567 rows
  - 35 distinct funds
  - 38 business countries
- Most represented countries in the extract:
  - France: 4,140 rows
  - Switzerland: 1,824
  - Spain: 827
  - Luxembourg: 792
  - Italy: 405
  - Germany: 270
- Most frequent segment labels:
  - `Bank / EdR Private Banking`
  - `Bank / Private Banking`
  - `Bank / Retail`
  - `Insurance Company / Unit Link`
- This file is likely most useful for Deliverable 3, especially country prioritization, client targeting, and KPI hypotheses.

### EdRAM House View Decks

- Files:
  - [Stratégie d'investissement 2026 FR.pptx](/Users/milo/Desktop/BDD_EDR/Strate%CC%81gie%20d'investissement%202026%20FR.pptx)
  - [Stratégie d'investissement 2026  UK.pptx](/Users/milo/Desktop/BDD_EDR/Strate%CC%81gie%20d'investissement%202026%20%20UK.pptx)
- Each deck has 14 slides.
- They appear to be French and English versions of the same EdRAM investment-strategy storyline.
- Main slide topics include:
  - AI as a macro factor
  - 2026 as a fiscal year
  - risk of political pressure on the Fed
  - capital markets union
  - China-U.S. rivalry
  - skepticism on private credit
  - low risk premiums
  - equity stance
  - weaker dollar
  - gold
  - conclusions

## Important Caveats

- [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md) is the key Phase 1 comparison artifact even though its filename suggests only a selection step.
- [deliverable_2.md](/Users/milo/Desktop/BDD_EDR/deliverable_2.md) and [deliverable_3.md](/Users/milo/Desktop/BDD_EDR/deliverable_3.md) are assignment/rubric files, not completed submissions.
- If the brief and the deliverable instruction files conflict, treat [business_case_brief.md](/Users/milo/Desktop/BDD_EDR/business_case_brief.md) as the canonical source for overall scope and deliverable framing, and treat [deliverable_2.md](/Users/milo/Desktop/BDD_EDR/deliverable_2.md) and [deliverable_3.md](/Users/milo/Desktop/BDD_EDR/deliverable_3.md) mainly as scoring rubrics.
- [dashboard/README.md](/Users/milo/Desktop/BDD_EDR/dashboard/README.md) is a product note only. There is no implemented dashboard code in the repo right now.
- [2025_12_houseview_fr_7f0b604b28.pdf](/Users/milo/Desktop/BDD_EDR/2025_12_houseview_fr_7f0b604b28.pdf) is byte-identical to [outlooks/EDRAM - Outlook 2026.pdf](/Users/milo/Desktop/BDD_EDR/outlooks/EDRAM%20-%20Outlook%202026.pdf). Treat it as a duplicate copy of the EdRAM benchmark source.
- Some extracted outlook text files note empty pages or low text density. Use the original source files when exact formatting or page interpretation matters.

## Recommended Reading Order For Agents

- Start with this file.
- Read [foundation/README.md](/Users/milo/Desktop/BDD_EDR/foundation/README.md) next if the task is to build, clean, or extend the Step 2 macro dataset.
- Read [business_case_brief.md](/Users/milo/Desktop/BDD_EDR/business_case_brief.md) if you need the official assignment framing and deliverable definitions.
- Read [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md) if you need the actual analytical substance already produced.
- Read [dashboard/README.md](/Users/milo/Desktop/BDD_EDR/dashboard/README.md) only if the task is to build or refine Deliverable 1.
- Use [Extraction Albert School 20251231.xlsx](/Users/milo/Desktop/BDD_EDR/Extraction%20Albert%20School%2020251231.xlsx) for Deliverable 3, especially country, channel, and fund-prioritization work.
- Use [outlooks_txt](/Users/milo/Desktop/BDD_EDR/outlooks_txt) only when you need source-level validation, quotes, or additional datapoints that are not already summarized.

## Practical Next Steps

- For D1 work: turn the comparison tables from [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md) into a structured data model and then into the dashboard spec from [dashboard/README.md](/Users/milo/Desktop/BDD_EDR/dashboard/README.md).
- For D2 work: distill exactly 10 commercially relevant insights from the consensus and divergence patterns already captured in [competitor_selection.md](/Users/milo/Desktop/BDD_EDR/competitor_selection.md).
- For D3 work: combine the macro views with the fund-distribution evidence in [Extraction Albert School 20251231.xlsx](/Users/milo/Desktop/BDD_EDR/Extraction%20Albert%20School%2020251231.xlsx) to prioritize funds and client types by country.
