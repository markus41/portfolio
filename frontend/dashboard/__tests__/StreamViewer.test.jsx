import { render, screen } from '@testing-library/react';
import StreamViewer from '../src/components/StreamViewer';
import { vi } from 'vitest';

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

describe('StreamViewer', () => {
  it('connects to SSE endpoint and renders messages', () => {
    render(<StreamViewer team="sales" apiKey="secret" />);
    expect(lastInstance.url).toBe('/teams/sales/stream?api_key=secret');
    lastInstance.emit('status', 'running');
    expect(screen.getByTestId('stream-data').textContent).toMatch('running');
  });
});
