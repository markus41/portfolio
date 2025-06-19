import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Subscribe to the `/teams/{team}/stream` SSE endpoint and display messages.
 */
function StreamViewer({ team, apiKey }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!team) return undefined;
    const url = `/teams/${team}/stream?api_key=${encodeURIComponent(apiKey || '')}`;
    const source = new EventSource(url);
    const handleStatus = (e) => setMessages((m) => [...m, `status: ${e.data}`]);
    const handleActivity = (e) => setMessages((m) => [...m, `activity: ${e.data}`]);
    source.addEventListener('status', handleStatus);
    source.addEventListener('activity', handleActivity);
    return () => source.close();
  }, [team, apiKey]);

  if (!team) return null;
  return (
    <div className="mt-4" data-testid="stream-viewer">
      <h5>Live Stream</h5>
      <pre data-testid="stream-data">{messages.join('\n')}</pre>
    </div>
  );
}

StreamViewer.propTypes = {
  team: PropTypes.string,
  apiKey: PropTypes.string,
};

export default StreamViewer;
