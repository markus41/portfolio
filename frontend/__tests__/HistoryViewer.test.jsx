import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import HistoryViewer from '../src/HistoryViewer.jsx';

let lastInstance;
class MockEventSource {
  constructor(url) {
    this.url = url;
    this.listeners = {};
    lastInstance = this;
  }
  addEventListener(type, cb) {
    this.listeners[type] = cb;
  }
  close() {
    this.closed = true;
  }
  emit(type, data) {
    if (this.listeners[type]) this.listeners[type]({ data });
  }
}

vi.stubGlobal('EventSource', MockEventSource);
vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ history: [] }) })));
vi.stubEnv('VITE_API_KEY', 'secret');

describe('HistoryViewer', () => {
  afterEach(() => {
    fetch.mockClear();
  });

  it('subscribes to stream and updates list on activity', () => {
    render(<HistoryViewer team="demo" />);
    expect(lastInstance.url).toBe('/teams/demo/stream?api_key=secret');
    lastInstance.emit('activity', JSON.stringify({ event: { type: 'lead' }, result: { ok: true } }));
    expect(screen.getByText(/lead/)).toBeInTheDocument();
    expect(screen.getByText(/"ok": true/)).toBeInTheDocument();
  });
});
