import hashlib
import logging

logger = logging.getLogger(__name__)


class SessionStitcher:
    """Utility for creating deterministic visitor IDs from fingerprints."""

    @staticmethod
    def stitch(fingerprint: str) -> str:
        vid = hashlib.sha256(fingerprint.encode()).hexdigest()
        logger.info(f"Stitched visitor id {vid} from fingerprint")
        return vid
