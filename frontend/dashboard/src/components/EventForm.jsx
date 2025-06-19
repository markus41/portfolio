import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Form, Button, Alert } from 'react-bootstrap';

/**
 * Form for submitting events to a team via the backend API.
 * The parent component must hold the ``team`` and ``apiKey`` state so that
 * ``StatusViewer`` can poll the same team.
 */
function EventForm({ team, setTeam, apiKey, setApiKey, onResult }) {
  const [eventType, setEventType] = useState('');
  const [payload, setPayload] = useState('{}');
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/teams/${team}/event`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({ type: eventType, payload: JSON.parse(payload) }),
      });
      const data = await response.json();
      onResult(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Form onSubmit={submit} data-testid="event-form">
      {error && (
        <Alert variant="danger" data-testid="error">
          {error}
        </Alert>
      )}
      <Form.Group className="mb-3">
        <Form.Label>Team Name</Form.Label>
        <Form.Control
          value={team}
          onChange={(e) => setTeam(e.target.value)}
          required
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>API Key</Form.Label>
        <Form.Control
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Event Type</Form.Label>
        <Form.Control
          value={eventType}
          onChange={(e) => setEventType(e.target.value)}
          required
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Payload (JSON)</Form.Label>
        <Form.Control
          as="textarea"
          rows={3}
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
        />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
}

EventForm.propTypes = {
  team: PropTypes.string.isRequired,
  setTeam: PropTypes.func.isRequired,
  apiKey: PropTypes.string,
  setApiKey: PropTypes.func.isRequired,
  onResult: PropTypes.func.isRequired,
};

export default EventForm;
