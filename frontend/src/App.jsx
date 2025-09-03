import React, {
  useCallback,
  useRef,
  useState
} from 'react';
import ReactFlow, {
  Background,
  Controls,
  ReactFlowProvider,
  addEdge,
  useEdgesState,
  useNodesState,
  useReactFlow
} from 'reactflow';
import 'reactflow/dist/style.css';
import { getApiKey } from './config';
import HistoryViewer from './HistoryViewer.jsx';
import NodeEditor from './NodeEditor.jsx';
import NodeToolbox from './NodeToolbox.jsx';

// ---------------------------------------------------------------------------
// App wrapper
// ---------------------------------------------------------------------------

/**
 * Wrap the workflow editor with ReactFlowProvider so hooks such as
 * `useReactFlow` can access the internal instance. All editor logic lives in the
 * nested `Editor` component.
 */
export default function App() {
  return (
    <ReactFlowProvider>
      <Editor />
    </ReactFlowProvider>
  );
}

// ---------------------------------------------------------------------------
// Editor component
// ---------------------------------------------------------------------------
function Editor() {
  // Manage nodes and edges using ReactFlow's helper hooks to automatically
  // produce `onNodesChange`/`onEdgesChange` handlers.
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // State for context menu and the currently edited item.
  const [contextMenu, setContextMenu] = useState(null);
  const [editingItem, setEditingItem] = useState(null);

  // Ref to the ReactFlow wrapper div so we can calculate drop coordinates.
  const wrapperRef = useRef(null);
  const { project } = useReactFlow();

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  // --------------------------- Drag and drop -------------------------------
  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const type = event.dataTransfer.getData('application/reactflow');
      if (!type) return;

      const bounds = wrapperRef.current.getBoundingClientRect();
      const position = project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });
      const label = `New ${type.charAt(0).toUpperCase() + type.slice(1)}`;
      const newNode = {
        id: crypto.randomUUID(),
        type,
        position,
        data: { label },
      };
      setNodes((nds) => nds.concat(newNode));
    },
    [project, setNodes],
  );

  // --------------------------- Context menu -------------------------------
  const openContextMenu = useCallback((type, id, event) => {
    event.preventDefault();
    setContextMenu({ type, id, position: { x: event.clientX, y: event.clientY } });
  }, []);

  const deleteItem = useCallback(() => {
    if (!contextMenu) return;
    if (contextMenu.type === 'node') {
      setNodes((nds) => nds.filter((n) => n.id !== contextMenu.id));
    } else {
      setEdges((eds) => eds.filter((e) => e.id !== contextMenu.id));
    }
    setContextMenu(null);
  }, [contextMenu, setEdges, setNodes]);

  const duplicateNode = useCallback(() => {
    if (!contextMenu) return;
    setNodes((nds) => {
      const node = nds.find((n) => n.id === contextMenu.id);
      if (!node) return nds;
      const copy = {
        ...node,
        id: crypto.randomUUID(),
        position: { x: node.position.x + 25, y: node.position.y + 25 },
      };
      return nds.concat(copy);
    });
    setContextMenu(null);
  }, [contextMenu, setNodes]);

  const editItem = useCallback(() => {
    if (!contextMenu) return;
    if (contextMenu.type === 'node') {
      const node = nodes.find((n) => n.id === contextMenu.id);
      if (node) setEditingItem(node);
    } else {
      const edge = edges.find((e) => e.id === contextMenu.id);
      if (edge) setEditingItem(edge);
    }
    setContextMenu(null);
  }, [contextMenu, edges, nodes]);

  const saveEdit = useCallback(
    (label) => {
      if (!editingItem) return;
      if ('source' in editingItem) {
        setEdges((eds) =>
          eds.map((e) => (e.id === editingItem.id ? { ...e, label } : e)),
        );
      } else {
        setNodes((nds) =>
          nds.map((n) =>
            n.id === editingItem.id ? { ...n, data: { ...n.data, label } } : n,
          ),
        );
      }
      setEditingItem(null);
    },
    [editingItem, setEdges, setNodes],
  );

  // --------------------------- Persistence --------------------------------
  const saveWorkflow = async () => {
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
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <NodeToolbox />
      <div
        ref={wrapperRef}
        style={{ flex: 1 }}
        onDrop={onDrop}
        onDragOver={onDragOver}
        data-testid="rf-wrapper"
      >
        <button onClick={saveWorkflow}>Save</button>
        <HistoryViewer />
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeContextMenu={(event, node) =>
            openContextMenu('node', node.id, event)
          }
          onEdgeContextMenu={(event, edge) =>
            openContextMenu('edge', edge.id, event)
          }
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      {contextMenu && (
        <ContextMenu
          position={contextMenu.position}
          type={contextMenu.type}
          onEdit={editItem}
          onDuplicate={duplicateNode}
          onDelete={deleteItem}
        />
      )}
      {editingItem && (
        <NodeEditor
          item={editingItem}
          onSave={saveEdit}
          onClose={() => setEditingItem(null)}
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Context menu helper component
// ---------------------------------------------------------------------------
function ContextMenu({ position, type, onEdit, onDuplicate, onDelete }) {
  return (
    <div
      role="menu"
      style={{
        position: 'absolute',
        top: position.y,
        left: position.x,
        background: '#fff',
        border: '1px solid #ccc',
        padding: 4,
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <button onClick={onEdit} role="menuitem">
        Edit
      </button>
      {type === 'node' && (
        <button onClick={onDuplicate} role="menuitem">
          Duplicate
        </button>
      )}
      <button onClick={onDelete} role="menuitem">
        Delete
      </button>
    </div>
  );
}

