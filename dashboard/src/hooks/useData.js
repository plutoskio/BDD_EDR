import { useState, useEffect } from 'react';
import Papa from 'papaparse';
import csvUrl from '../data/asset_manager_master.csv?url';

export function useData() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Papa.parse(csvUrl, {
      download: true,
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        // Clean the keys and parse if necessary
        setData(results.data);
        setLoading(false);
      },
      error: (err) => {
        console.error('PapaParse error:', err);
        setError(err);
        setLoading(false);
      }
    });
  }, []);

  return { data, loading, error };
}
