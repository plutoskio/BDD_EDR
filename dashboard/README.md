# Edmond de Rothschild Competitive Dashboard

This repository contains the interactive Phase 1 macroeconomic and investment competitive analysis dashboard built specifically for **Edmond de Rothschild (EdRAM)**.

## Live Deployment
The application is pre-built and live here: **[https://plutoskio.github.io/BDD_EDR_DASHBOARD](https://plutoskio.github.io/BDD_EDR_DASHBOARD)**

## Features
- **Asset Manager Comparison**: Directly compare EdRAM's outlooks side-by-side with individual leading competitors.
- **Market Consensus**: A fully qualitative and quantitative breakdown highlighting EdRAM's key differentiators, strong alignments, and market blindspots.
- **Evidence Drawer**: Double-click traceability for every metric linking to the original analyst rationale and source text.

## Running Locally

Because this project uses the Vite + React toolchain, it is extremely robust and has **no complex system dependencies**. 

To run it locally on your own machine, simply clone this repository and execute the following in your terminal:

```bash
# 1. Install Node.js dependencies
npm install

# 2. Start the local development server
npm run dev
```

Navigate to `http://localhost:5173/` in your browser.

## Tech Stack
- **Framework**: React.js + Vite
- **Styling**: Pure CSS architecture tailored precisely to Edmond de Rothschild Corporate Branding (Prussian Blue, Gold, and Ebony elements).
- **Data Parser**: Natively reads data from statically hosted `csv` and `json` files.
