// Y-OS Universe — useCMS hook
// Fetches and caches the CMS data from /cms.json

import { useState, useEffect } from 'react';
import type { CMSData } from '../types/cms';

interface UseCMSResult {
  data: CMSData | null;
  loading: boolean;
  error: string | null;
}

export function useCMS(): UseCMSResult {
  const [data, setData] = useState<CMSData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/cms.json')
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((json: CMSData) => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { data, loading, error };
}
