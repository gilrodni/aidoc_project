"""Generic storage API with pluggable backends and serializers."""

from .base import Storage
from .local_file_storage import LocalFileStorage
from .serializers import (
    Serializer,
    SerializerRegistry,
    JsonSerializer,
    NumpySerializer,
)

__all__ = [
    # Storage interfaces and implementations
    "Storage",
    "LocalFileStorage",
    # Serializers
    "Serializer",
    "SerializerRegistry",
    "JsonSerializer",
    "NumpySerializer",
]

