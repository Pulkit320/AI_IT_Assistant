"""
Structured JSON Logger Setup.
Provides production-quality formatted JSON logs for cloud and local environments.
"""

import json
import logging
import sys
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom logging formatter that converts record metadata into JSON format."""

    @staticmethod
    def mask_pii(text: str) -> str:
        """Masks sensitive PII patterns in log messages."""
        if not isinstance(text, str):
            return text
        import re
        # Mask password_hash or secret answers if present
        text = re.sub(r'("password_hash":\s*")[^"]+"', r'\1[REDACTED]"', text)
        text = re.sub(r'("security_answer":\s*")[^"]+"', r'\1[REDACTED]"', text)
        return text

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": self.mask_pii(record.getMessage()),
            "module": record.module,
            "filename": record.filename,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configures root logger to use stdout stream handler with JSON formatting."""
    logger = logging.getLogger("helpdesk")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicate log entries
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    return logger


logger = setup_logging()
