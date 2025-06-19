import React, { useState } from 'react';
import EventForm from './components/EventForm';
import StatusViewer from './components/StatusViewer';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  const [team, setTeam] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [result, setResult] = useState(null);

  return (
    <div className="container py-4">
      <h1 className="mb-4">Team Dashboard</h1>
      <EventForm
        team={team}
        setTeam={setTeam}
        apiKey={apiKey}
        setApiKey={setApiKey}
        onResult={(data) => setResult(JSON.stringify(data, null, 2))}
      />
      <StatusViewer team={team} apiKey={apiKey} />
      {result && (
        <div className="mt-4">
          <h5>Result</h5>
          <pre data-testid="result">{result}</pre>
        </div>
      )}
    </div>
  );
}
