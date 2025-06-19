import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Polls ``/teams/{team}/status`` on a fixed interval and displays the result.
 * If the API supported Server-Sent Events or websockets, this component could
 * subscribe instead of polling.
 */
function StatusViewer({ team, apiKey, interval = 5000 }) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!team) return undefined;
    let active = true;

    const fetchStatus = async () => {
      try {
        const res = await fetch(`/teams/${team}/status`, {
          headers: { 'X-API-Key': apiKey },
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (active) {
          setStatus(data.status);
          setError(null);
        }
      } catch (err) {
        if (active) setError(err.message);
      }
    };

    fetchStatus();
    const id = setInterval(fetchStatus, interval);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, [team, apiKey, interval]);

  if (!team) return null;
  return (
    <div className="mt-4" data-testid="status-viewer">
      <h5>Current Status</h5>
      {error ? (
        <p className="text-danger" data-testid="status-error">{error}</p>
      ) : (
        <p data-testid="status-text">{status || 'Loading...'}</p>
      )}
    </div>
  );
}

StatusViewer.propTypes = {
  team: PropTypes.string,
  apiKey: PropTypes.string,
  interval: PropTypes.number,
};

export default StatusViewer;
