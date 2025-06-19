import { render, screen, waitFor } from '@testing-library/react';
import StatusViewer from '../src/components/StatusViewer';
import { vi } from 'vitest';

vi.stubGlobal('fetch', vi.fn());

describe('StatusViewer', () => {
  afterEach(() => {
    fetch.mockClear();
  });

  it('polls status endpoint periodically', async () => {
    vi.useFakeTimers();
    fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ status: 'done' }) });
    render(<StatusViewer team="sales" apiKey="secret" interval={1000} />);
    await vi.advanceTimersByTimeAsync(1000);
    await waitFor(() => expect(fetch).toHaveBeenCalled());
    expect(fetch.mock.calls[0][0]).toBe('/teams/sales/status');
    vi.useRealTimers();
  });
});
