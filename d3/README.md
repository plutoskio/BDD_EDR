# Deliverable 3 Workspace

This folder is the working area for Deliverable 3: country-by-country sales recommendations for EdRAM.

The target is not a generic macro note. The target is a sales-ready recommendation pack that links:

- country narrative
- EdRAM fund selection
- client/channel targeting
- KPI logic

## Working Principle

We win this case if the final output looks like a product manager brief for the Director of Sales, not like a student report.

That means:

- each country must have a genuinely different commercial story
- every recommended fund must have a clear macro reason and a clear sales reason
- KPIs must be explicit and decision-useful
- we should show both existing strengths and expansion opportunities

## Folder Structure

- `build_crm_summaries.py`
  - reproducible CRM parser using only the Python standard library
- `data/`
  - country, fund, and segment summaries extracted from `CRM_2025.xlsx`
- `notes/`
  - scoring framework, peer-set logic, and cross-country observations
- `country_workpads/`
  - one folder per target country for recommendation drafting

## Recommended Workflow

1. Establish the local macro lens for each country.
2. Map those narratives to the EdRAM fund range.
3. Check commercial reality in CRM:
   - existing traction
   - channel concentration
   - fund concentration
4. Rank `Scale Now`, `Strategic Bet`, and `Challenger` ideas.
5. Turn the analysis into a sales brief with KPIs and messaging.
