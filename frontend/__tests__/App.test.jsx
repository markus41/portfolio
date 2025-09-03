import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import App from '../src/App';

vi.stubGlobal('fetch', vi.fn());
vi.stubGlobal('EventSource', class {
  constructor() {}
  addEventListener() {}
  close() {}
});
vi.stubGlobal('ResizeObserver', class {
  observe() {}
  unobserve() {}
  disconnect() {}
});

vi.stubEnv('VITE_API_KEY', 'test-key');

describe('App', () => {
  afterEach(() => {
    fetch.mockClear();
  });

  it('sends API key from environment when saving', async () => {
    render(<App />);
    fireEvent.click(screen.getByText(/save/i));
    await waitFor(() => expect(fetch).toHaveBeenCalled());
    const options = fetch.mock.calls[0][1];
    expect(options.headers['X-API-Key']).toBe('test-key');
  });

  it('adds a node via drag-and-drop from the toolbox', () => {
    render(<App />);
    const item = screen.getByText('Agent');
    const canvas = screen.getByTestId('rf-wrapper');
    const dataTransfer = {
      data: {},
      setData(key, val) {
        this.data[key] = val;
      },
      getData(key) {
        return this.data[key];
      },
      effectAllowed: 'move',
      dropEffect: 'move',
    };
    fireEvent.dragStart(item, { dataTransfer });
    fireEvent.drop(canvas, { dataTransfer, clientX: 10, clientY: 10 });
    expect(screen.getByText('New Agent')).toBeInTheDocument();
  });

  it('edits a node label via context menu', async () => {
    render(<App />);
    const item = screen.getByText('Agent');
    const canvas = screen.getByTestId('rf-wrapper');
    const dataTransfer = {
      data: {},
      setData(key, val) {
        this.data[key] = val;
      },
      getData(key) {
        return this.data[key];
      },
      effectAllowed: 'move',
      dropEffect: 'move',
    };
    fireEvent.dragStart(item, { dataTransfer });
    fireEvent.drop(canvas, { dataTransfer, clientX: 10, clientY: 10 });
    const node = screen.getByText('New Agent');
    fireEvent.contextMenu(node);
    fireEvent.click(screen.getByRole('menuitem', { name: /edit/i }));
    const input = screen.getByLabelText('label');
    fireEvent.change(input, { target: { value: 'Updated' } });
    fireEvent.click(screen.getByText('Save'));
    await screen.findByText('Updated');
  });
});
