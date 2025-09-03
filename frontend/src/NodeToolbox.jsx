import React from 'react';

// Definitions of draggable node types. Each entry describes the ReactFlow
// `type` and the default label assigned when dropped on the canvas.
const NODE_TYPES = [
  { type: 'agent', label: 'Agent' },
  { type: 'task', label: 'Task' },
];

/**
 * Sidebar palette listing available node types.
 *
 * Users can drag an item from this toolbox onto the ReactFlow canvas to create
 * a new node of the corresponding type. The component is intentionally
 * stateless and purely presentational so that consumers can customize node
 * creation logic within the editor.
 */
export default function NodeToolbox() {
  /**
   * Attach node type information to the drag event so the drop handler inside
   * the ReactFlow canvas can read it via `event.dataTransfer.getData`.
   */
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside
      aria-label="Node toolbox"
      role="listbox"
      style={styles.container}
    >
      {NODE_TYPES.map((node) => (
      <div
        key={node.type}
        style={styles.item}
        draggable
        onDragStart={(event) => onDragStart(event, node.type)}
        role="option"
        aria-grabbed="false"
      >
        {node.label}
      </div>
      ))}
    </aside>
  );
}

const styles = {
  container: {
    padding: 10,
    borderRight: '1px solid #ccc',
    width: 150,
    boxSizing: 'border-box',
  },
  item: {
    padding: '4px 8px',
    border: '1px solid #999',
    borderRadius: 4,
    marginBottom: 4,
    cursor: 'grab',
    background: '#fff',
  },
};

