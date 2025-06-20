import React, { useState } from 'react';
import { getApiKey } from './config';

export default function SettingsPage() {
  const [organization, setOrg] = useState('');
  const [openaiKey, setOpenaiKey] = useState('');
  const [crmUrl, setCrmUrl] = useState('');
  const [crmKey, setCrmKey] = useState('');
  const [emailKey, setEmailKey] = useState('');
  const [disabledTeams, setDisabled] = useState('');

  const save = async () => {
    const payload = {
      organization,
      openai_api_key: openaiKey || undefined,
      crm_api_url: crmUrl || undefined,
      crm_api_key: crmKey || undefined,
      email_service_api_key: emailKey || undefined,
      disabled_teams: disabledTeams
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean),
    };

    const headers = { 'Content-Type': 'application/json' };
    const apiKey = getApiKey();
    if (apiKey) headers['X-API-Key'] = apiKey;

    await fetch('/settings', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
  };

  return (
    <div className="container mt-4">
      <h1>User Settings</h1>
      <div className="mb-3">
        <label className="form-label">Organization</label>
        <input className="form-control" value={organization} onChange={(e) => setOrg(e.target.value)} />
      </div>
      <div className="mb-3">
        <label className="form-label">OpenAI API Key</label>
        <input className="form-control" value={openaiKey} onChange={(e) => setOpenaiKey(e.target.value)} />
      </div>
      <div className="mb-3">
        <label className="form-label">CRM API URL</label>
        <input className="form-control" value={crmUrl} onChange={(e) => setCrmUrl(e.target.value)} />
      </div>
      <div className="mb-3">
        <label className="form-label">CRM API Key</label>
        <input className="form-control" value={crmKey} onChange={(e) => setCrmKey(e.target.value)} />
      </div>
      <div className="mb-3">
        <label className="form-label">Email Service API Key</label>
        <input className="form-control" value={emailKey} onChange={(e) => setEmailKey(e.target.value)} />
      </div>
      <div className="mb-3">
        <label className="form-label">Disabled Teams (comma separated)</label>
        <input className="form-control" value={disabledTeams} onChange={(e) => setDisabled(e.target.value)} />
      </div>
      <button className="btn btn-primary" onClick={save}>Save</button>
    </div>
  );
}
