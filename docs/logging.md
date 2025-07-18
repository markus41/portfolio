# Logging Configuration

The project emits all logs in JSON format to make it easy to ingest them into
log aggregation systems. Use ``src.utils.logging_config.setup_logging`` to
initialise the logger before running any code that writes log messages. It is
idempotent and safe to call multiple times.

```python
from src.utils.logging_config import setup_logging
import logging

setup_logging()  # configure root logger
logger = logging.getLogger(__name__)
logger.info("Started")
```

`setup_logging()` honours the ``LOG_LEVEL`` environment variable when a level is
not explicitly passed. Log entries contain a timestamp, level, logger name and
message:

```json
{"timestamp": "2024-01-01T00:00:00Z", "level": "INFO", "name": "demo", "message": "Started"}
```

Additional environment variables allow customising the output location and
format:

* ``LOG_FILE`` – path to a file where logs should be written. When set,
  ``setup_logging`` writes to this file instead of ``stdout``.
* ``LOG_PLAIN`` – when set to ``true`` or ``1`` the logger emits human readable
  text rather than JSON.

These can also be specified via parameters:

```python
setup_logging(file_path="/tmp/app.log", plain_text=True)
```
