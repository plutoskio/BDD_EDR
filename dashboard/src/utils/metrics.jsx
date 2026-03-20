export const METRICS = [
  { section: 'Macro Forecasts', 
    isMacro: true,
    items: [
      { key: 'global_growth_2026', label: 'Global Growth (%)' },
      { key: 'us_gdp_2026', label: 'US GDP (%)' },
      { key: 'eurozone_gdp_2026', label: 'Eurozone GDP (%)' },
      { key: 'china_gdp_2026', label: 'China GDP (%)' },
      { key: 'em_growth_2026', label: 'EM Growth (%)' },
      { key: 'global_inflation_2026', label: 'Global Inflation (%)' },
      { key: 'us_inflation_2026', label: 'US Inflation (%)' },
      { key: 'eurozone_inflation_2026', label: 'Eurozone Inflation (%)' },
      { key: 'fed_year_end_rate_2026', label: 'Fed Policy Rate (%)' },
      { key: 'ecb_deposit_rate_year_end_2026', label: 'ECB Deposit Rate (%)' },
      { key: 'eur_usd_2026', label: 'EUR/USD' },
    ]
  },
  { section: 'Equities', 
    isMacro: false,
    items: [
      { key: 'equities_overall', label: 'Overall Equities' },
      { key: 'equities_geography_us', label: 'US Equities' },
      { key: 'equities_geography_europe', label: 'European Equities' },
      { key: 'equities_geography_japan', label: 'Japanese Equities' },
      { key: 'equities_geography_em', label: 'Emerging Markets' },
      { key: 'equities_geography_china', label: 'Chinese Equities' },
      { key: 'equities_size_large_cap', label: 'Large Caps' },
      { key: 'equities_size_small_cap', label: 'Small Caps' },
    ]
  },
  { section: 'Fixed Income',
    isMacro: false,
    items: [
      { key: 'fixed_income_overall', label: 'Overall Fixed Income' },
      { key: 'fixed_income_credit_quality_investment_grade', label: 'Investment Grade' },
      { key: 'fixed_income_credit_quality_high_yield', label: 'High Yield' },
      { key: 'fixed_income_segment_government_bonds', label: 'Government Bonds' },
      { key: 'fixed_income_segment_corporate_bonds', label: 'Corporate Bonds' },
      { key: 'fixed_income_segment_em_debt', label: 'EM Debt' },
    ]
  },
  { section: 'Currencies & Commodities',
    isMacro: false,
    items: [
      { key: 'currencies_usd', label: 'USD' },
      { key: 'currencies_eur', label: 'EUR' },
      { key: 'currencies_em_fx', label: 'EM FX' },
      { key: 'commodities_gold', label: 'Gold' },
      { key: 'commodities_oil', label: 'Oil' },
    ]
  },
  { section: 'Thematic Convictions',
    isMacro: false,
    items: [
      { key: 'themes_ai', label: 'Artificial Intelligence' },
      { key: 'themes_healthcare', label: 'Healthcare' },
      { key: 'themes_energy_transition', label: 'Energy Transition' },
      { key: 'themes_defense_sovereignty', label: 'Defense / Sovereignty' },
    ]
  }
];

export function extractData(row, key, isMacro) {
  if (!row) return null;
  const statusKey = isMacro ? `${key}_status` : `${key}_view`;
  let valKey = isMacro ? `${key}_value` : null;
  
  return {
    status: row[statusKey] || 'ND',
    value: isMacro ? row[valKey] : '',
    why: row[`${key}_why`] || '',
    page: row[`${key}_page`] || '',
    wording: row[`${key}_raw_wording`] || '',
    source_file: row.source_file
  };
}

export function getStatusColor(status) {
  if (!status) return 'var(--status-nd-text)';
  const s = status.toLowerCase().trim();
  if (['positive', 'long', 'overweight', 'constructive', 'attractive'].includes(s)) return 'var(--status-pos-text)';
  if (['negative', 'short', 'underweight', 'unattractive', 'cautious'].includes(s)) return 'var(--status-neg-text)';
  if (['neutral', 'mixed'].includes(s)) return 'var(--status-neu-text)';
  if (s === 'qualitative' || s === 'quantitative') return 'var(--text-highlight)';
  return 'var(--status-nd-text)';
}

export function formatValueDisplay(data) {
  if (data.status === 'ND' || data.status === 'nd' || !data.status) {
    return <span style={{color: 'var(--status-nd-text)', fontStyle: 'italic', fontSize: '13px'}}>ND</span>;
  }
  
  if (data.value && data.value.trim() !== '') {
    return <span style={{fontWeight: 600, color: 'var(--text-primary)'}}>{data.value}</span>;
  }
  
  return <span style={{color: getStatusColor(data.status), textTransform: 'capitalize', fontWeight: 500}}>{data.status}</span>;
}
