const fs = require('fs');
const papa = require('papaparse');

const content = fs.readFileSync('../foundation/asset_manager_master.csv', 'utf8');
const { data } = papa.parse(content, { header: true, skipEmptyLines: true });

const competitors = data.filter(r => r.manager !== 'EdRAM' && r.manager !== 'Benchmark');

const metrics = [
  'global_growth_2026', 'us_gdp_2026', 'eurozone_gdp_2026', 'china_gdp_2026', 'em_growth_2026',
  'global_inflation_2026', 'us_inflation_2026', 'eurozone_inflation_2026',
  'fed_year_end_rate_2026', 'ecb_deposit_rate_year_end_2026', 'eur_usd_2026',
  'equities_overall', 'equities_geography_us', 'equities_geography_europe', 'equities_geography_japan', 'equities_geography_em', 'equities_geography_china', 'equities_size_large_cap', 'equities_size_small_cap',
  'fixed_income_overall', 'fixed_income_credit_quality_investment_grade', 'fixed_income_credit_quality_high_yield', 'fixed_income_segment_government_bonds', 'fixed_income_segment_corporate_bonds', 'fixed_income_segment_em_debt',
  'currencies_usd', 'currencies_eur', 'currencies_em_fx', 'commodities_gold', 'commodities_oil',
  'themes_ai', 'themes_healthcare', 'themes_energy_transition', 'themes_defense_sovereignty'
];

let promptData = {};
metrics.forEach(m => {
  promptData[m] = [];
  competitors.forEach(c => {
    let status = c[`${m}_status`] || c[`${m}_view`];
    let val = c[`${m}_value`];
    let why = c[`${m}_why`] || c[`${m}_raw_wording`];
    if (status && status.toLowerCase() !== 'nd') {
       promptData[m].push(`${c.manager}: [${status}] ${val ? val : ''} - ${why || ''}`);
    }
  });
});

fs.writeFileSync('prompt_data.json', JSON.stringify(promptData, null, 2));
console.log('prompt_data.json created');
