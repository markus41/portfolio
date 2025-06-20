import React, { useState } from 'react';
import ReactFlow, { Background, Controls, addEdge } from 'reactflow';
import 'reactflow/dist/style.css';
import { getApiKey } from './config';
import SettingsPage from './SettingsPage';

export default function App() {
  if (window.location.pathname.includes('settings')) {
    return <SettingsPage />;
  }
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const save = async () => {
    const workflow = {
      name: 'workflow',
      nodes: nodes.map((n) => ({
        id: n.id,
        type: n.type || 'agent',
        label: n.data?.label || n.id,
      })),
      edges: edges.map((e) => ({
        source: e.source,
        target: e.target,
        label: e.label,
      })),
    };

    const headers = { 'Content-Type': 'application/json' };
    const apiKey = getApiKey();
    if (apiKey) headers['X-API-Key'] = apiKey;

    await fetch('/workflows', {
      method: 'POST',
      headers,
      body: JSON.stringify(workflow),
    });
  };

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <button onClick={save}>Save</button>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={setNodes} onEdgesChange={setEdges} onConnect={onConnect}>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
