# Deliverable 3 — The Competitive Edge Playbook

## How Asset Management Sales Actually Work

Before reading the strategy, it helps to understand who EdRAM's Sales team actually sells to and how. This is not retail brokerage. EdRAM does not call individual investors.

### The clients are intermediaries

EdRAM sells to **organizations** that distribute funds to their own end clients:

| Client Type | What They Are | How the Sale Works |
|---|---|---|
| **Private Banks** | Wealth managers serving high-net-worth clients | EdRAM pitches the bank's fund selector or CIO to get on their **recommended list** |
| **Insurance Companies** | Firms packaging funds into unit-linked life insurance products | EdRAM must convince them to **include** the fund in their menu. Very sticky once listed. |
| **Fund of Funds** | Asset managers who build portfolios of other managers' funds | They evaluate EdRAM on performance, risk, fees, and thesis. Analytical buyers. |
| **Retail Platforms** | Banks listing funds for retail clients to buy | EdRAM needs to be on the **approved product shelf** and stay visible. |
| **EdR Private Banking** | Edmond de Rothschild's own wealth management arm | Internal — coordinating with their own bankers to push specific funds to HNW clients. |

### How a typical sales cycle works

1. **Quarterly or annual review meeting** — The salesperson meets the client (e.g., a private bank's fund selector) to present EdRAM's market outlook and recommend specific funds. **This is exactly the meeting our tool prepares them for.**
2. **The pitch** is always: *"Given the macro environment, here's why our fund is better positioned than what you currently hold"* — often a competitor's product. This is why competitive displacement matters.
3. **If the client agrees** → they allocate a portion of their portfolio (or their clients' portfolios) to the EdRAM fund. Typical ticket: €5M–€500M+ depending on the client type.
4. **Duration** — No fixed lock-in for most UCITS funds. Money can leave at any time. In practice, allocations are **sticky for 1–3 years** unless something changes — which is why periodic reviews matter.
5. **The real risk** — A competitor's salesperson shows up with a better pitch and the client moves money out. Knowing what competitors are saying is the best defense.

### Existing clients vs. new prospecting

Roughly **70% of effort is growing and protecting existing relationships**, 30% is prospecting new ones. The CRM data covers the existing base — so our triggers focus on defending, cross-selling, and identifying white space within relationships that already exist.

---

## What We're Building

A **standalone interactive sales tool** — a deployed web app — that gives each country sales head a live, meeting-ready playbook combining CRM intelligence, competitive displacement angles, and revenue KPIs.

This is **separate from the D1 dashboard**. D1 is analytical intelligence for product management. D3 is **a sales action tool for the field**.

> The brief says: *"The format should be directly usable by a Sales manager preparing a client meeting or a country briefing."*
>
> Other groups will submit a PDF. We submit **a live tool they can open on their laptop before walking into the meeting**.

---

## The Solution: An Interactive Sales Playbook

### What it does

A Sales manager opens the tool, selects their country, and gets:

1. **Local macro narrative** — 3 bullets on what the local competitive consensus says and where EdRAM diverges. Not a global macro recap — the angle that matters for *this market's* conversations.

2. **Three ranked fund recommendations** — Scale Now / Strategic Bet / Challenger — each with:
   - One-sentence macro rationale
   - The **named competitor product** it's designed to displace
   - A one-sentence client pitch ready to use verbatim
   - KPIs: installed AUM, target accounts, estimated fee revenue

3. **CRM client triggers** — quantified segments to prioritize calling:
   - Accounts with negative outlook mismatch
   - Concentrated positions ripe for cross-sell
   - White-space accounts with zero exposure to the recommended product

4. **Meeting prep view** — a clean, printable one-page brief per country

### What makes it stand out

| vs. other groups | Our approach |
|---|---|
| They submit a report | We submit a live, deployed tool |
| They say "recommend Fund X" | We say "pitch Fund X **against Competitor Y's product**, here's the one-liner" |
| They say "addressable AUM = €500M" | We say "estimated fee uplift = €2.1M/year at 15% conversion" |
| They say "target institutional clients" | We say "147 PB accounts with >70% concentration in one fund — call them first" |
| Same recommendations in every country | Different triggers, competitors, pitches, and "what NOT to push" per market |

---

## Three-Layer Intelligence Architecture

```
CRM client data  ×  Phase 1 competitor views  ×  EdRAM fund range
       ↓                     ↓                         ↓
  WHO to call         WHAT to say against          WITH which product
                      named competitors
```

### Layer 1 — Client Action Triggers (from CRM)

We parse `CRM_2025.xlsx` to identify specific, quantified client segments:

- **Negative Outlook Mismatch**: clients holding products where the 2026 consensus has turned cautious
- **Concentration Risk**: clients with >70% in a single fund family → cross-sell opportunity
- **White Space**: existing relationships with zero exposure to a product category where EdRAM has macro alignment

Each trigger produces: account count, AUM at risk/opportunity, and the specific fund to pitch.

### Layer 2 — Competitive Displacement (from Phase 1)

Because we built the Phase 1 dashboard, we know exactly what each competitor tells clients in each market. Each fund recommendation comes with:

- Which competitor's positioning it beats
- Why EdRAM's angle is differentiated (consensus divergence or superior execution)
- A ready-made one-sentence pitch for the client conversation

| Country | Competitor logic | EdRAM's edge | Product |
|---|---|---|---|
| France | Amundi / BNP cautious on AI concentration | Big Data is the *smarter* AI play — users, not mega-caps | Big Data |
| Germany | DWS calls "Goldilocks" — complacent on duration | Carry over duration discipline | Financial Bonds |
| Switzerland | UBS / LO pushing broad EM income | More targeted hybrid and EM credit story | Corporate Hybrid Bonds |
| Italy | Anima favors cyclicals and growth tilt | Credit sophistication over generic growth | Short Duration Credit |
| Spain | Santander / JPAM broadly constructive | Defined-maturity packaging that globals lack | Millesima 2030 |

### Layer 3 — Revenue-Impact KPIs

Every recommendation is quantified in the language a Director of Sales thinks in:

```
Fee uplift = Addressable AUM × Conversion rate × Management fee rate
```

Additional KPIs per pick:
- Current installed AUM (the "defend" baseline)
- Reachable accounts in target segment
- Cross-sell penetration rate (% with zero exposure to this product)
- Revenue uplift estimate (annual management fee from incremental conversion)

---

## Tech Stack

| Component | Technology |
|---|---|
| CRM parser | Python → JSON data files |
| Interactive app | React + Vite (separate from D1 dashboard) |
| Styling | Vanilla CSS with EdRAM corporate branding |
| Deployment | GitHub Pages (separate repository/deployment) |
| Data | Static JSON files generated from CRM + competitor analysis |

### Data Pipeline

```
CRM_2025.xlsx ──→ Python parser ──→ crm_triggers.json
                                          ↓
competitor_selection.md ──→ structured ──→ competitive_angles.json
                                          ↓
                                    React app ──→ GitHub Pages
```

---

## Country Deliverable Structure

Each country in the app shows:

### 1. Macro Headline
3 bullets: local consensus + EdRAM's divergence angle

### 2. Fund Recommendations

| Tier | Purpose |
|---|---|
| **Scale Now** | Strongest macro fit + existing traction → defend and grow |
| **Strategic Bet** | Biggest competitive divergence → unique EdRAM opening |
| **Challenger** | Unexpected pick that shows commercial depth |

### 3. Client Action Triggers
CRM segments to call, with numbers

### 4. What NOT to Push
Products that are defaulted to in this market but are *not* the right 2026 play. Shows conviction.

### 5. Meeting Prep
Printable one-page view

---

## The Jury Pitch (one sentence)

> **We didn't just tell Sales which funds to recommend — we built them a tool that shows which clients to call first, what the competitor across the table is saying, and how much fee revenue is at stake.**

---

## Folder Structure

```
D3/
├── README.md                    ← this file (strategy & methodology)
├── scripts/
│   └── parse_crm.py            ← CRM data parser
├── data/
│   ├── crm_triggers.json       ← parsed client triggers by country
│   └── competitive_angles.json ← structured displacement data
├── app/                        ← Vite + React sales playbook app
│   ├── src/
│   ├── public/
│   └── package.json
├── france.md                    ← written country brief (backup/print)
├── germany.md
├── switzerland.md
├── italy.md
└── spain.md
```

## Rubric Alignment

| Criterion | Weight | How we score |
|---|---|---|
| **Macro-to-fund linkage** | /30 | Every pick tied to a named competitor divergence |
| **KPI quality** | /25 | Revenue-based, computed on explicit hypotheses |
| **Country differentiation** | /20 | Different triggers, competitors, pitches per market |
| **Client targeting precision** | /15 | CRM-quantified segments with account counts |
| **Actionability** | /10 | Live interactive tool, not a document |
