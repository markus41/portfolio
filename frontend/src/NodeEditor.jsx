import React, { useState } from 'react';

/**
 * Simple modal dialog for editing the label of a node or edge. The component is
 * deliberately minimal but includes basic validation and accessibility
 * attributes so it can serve as a foundation for richer property editing in the
 * future.
 */
export default function NodeEditor({ item, onSave, onClose }) {
  const initial = item?.data?.label || item?.label || '';
  const [label, setLabel] = useState(initial);

  const save = () => {
    const trimmed = label.trim();
    if (!trimmed) return; // no empty labels
    onSave(trimmed);
  };

  return (
    <div style={overlay} role="dialog" aria-modal="true" aria-label="Edit label">
      <div style={modal}>
        <h2 style={{ marginTop: 0 }}>Edit</h2>
        <label style={{ display: 'block', marginBottom: 8 }}>
          Label
          <input
            aria-label="label"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            style={{ width: '100%' }}
          />
        </label>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
          <button onClick={onClose}>Cancel</button>
          <button onClick={save} disabled={!label.trim()}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

const overlay = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100vw',
  height: '100vh',
  background: 'rgba(0,0,0,0.3)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 100,
};

const modal = {
  background: '#fff',
  padding: 20,
  borderRadius: 4,
  minWidth: 300,
  boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
};

