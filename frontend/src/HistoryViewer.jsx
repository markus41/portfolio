import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { getApiKey } from './config';

// Default team used for streaming history updates. This mirrors the
// example team in the repository documentation.
const DEFAULT_TEAM = 'sales';
export default function HistoryViewer({ team = DEFAULT_TEAM }) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const apiKey = getApiKey();
    const headers = {};
    if (apiKey) headers['X-API-Key'] = apiKey;

    // Load the latest history snapshot on mount.
    const fetchHistory = async () => {
      const resp = await fetch('/history?limit=20', { headers });
      if (resp.ok) {
        const data = await resp.json();
        setItems(data.history || []);
      }
    };
    fetchHistory();

    // Subscribe to live updates from the team-specific SSE endpoint.
    const qs = apiKey ? `?api_key=${encodeURIComponent(apiKey)}` : '';
    const src = new EventSource(`/teams/${team}/stream${qs}`);
    const handleActivity = (e) => {
      try {
        const msg = JSON.parse(e.data);
        const item = {
          id: Date.now(),
          team,
          event_type: msg.event?.type || 'unknown',
          result: msg.result,
        };
        setItems((prev) => [item, ...prev].slice(0, 20));
      } catch {
        // ignore malformed payloads
      }
    };
    src.addEventListener('activity', handleActivity);
    return () => src.close();
  }, [team]);

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

HistoryViewer.propTypes = {
  // Name of the team to subscribe to for live history updates.
  team: PropTypes.string,
};
