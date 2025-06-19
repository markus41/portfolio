"""Backward compatible import for the default REST memory service."""

from .memory_service.rest import RestMemoryService

# Maintain historical name
MemoryService = RestMemoryService

__all__ = ["MemoryService", "RestMemoryService"]
