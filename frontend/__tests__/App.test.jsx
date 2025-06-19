import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import App from '../src/App';

vi.stubGlobal('fetch', vi.fn());

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
});
