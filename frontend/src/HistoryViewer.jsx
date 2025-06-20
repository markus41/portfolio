import React, { useEffect, useState } from 'react';
import { getApiKey } from './config';

export default function HistoryViewer() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const headers = {};
      const apiKey = getApiKey();
      if (apiKey) headers['X-API-Key'] = apiKey;
      const resp = await fetch('/history?limit=20', { headers });
      if (resp.ok) {
        const data = await resp.json();
        setItems(data.history || []);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
      <h3>History</h3>
      <ul>
        {items.map((h) => (
          <li key={h.id}>
            <strong>{h.team}</strong> {h.event_type} =&gt;{' '}
            {JSON.stringify(h.result)}
          </li>
        ))}
      </ul>
    </div>
  );
}
