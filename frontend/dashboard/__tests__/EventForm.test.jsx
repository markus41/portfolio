import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import EventForm from '../src/components/EventForm';
import { vi } from 'vitest';

vi.stubGlobal('fetch', vi.fn());

describe('EventForm', () => {
  afterEach(() => {
    fetch.mockClear();
  });

  it('posts event to the backend', async () => {
    fetch.mockResolvedValue({ json: () => Promise.resolve({ result: 'ok' }) });
    const onResult = vi.fn();
    render(
      <EventForm
        team="sales"
        setTeam={() => {}}
        apiKey="secret"
        setApiKey={() => {}}
        onResult={onResult}
      />
    );
    fireEvent.change(screen.getByLabelText(/Event Type/i), { target: { value: 'lead' } });
    fireEvent.change(screen.getByLabelText(/Payload/i), { target: { value: '{}' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    await waitFor(() => expect(fetch).toHaveBeenCalled());
    expect(fetch.mock.calls[0][0]).toBe('/teams/sales/event');
    expect(onResult).toHaveBeenCalled();
  });
});
