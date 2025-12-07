"""JSON serializer for general Python objects."""

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .base import Serializer


class JsonSerializer(Serializer):
    """
    Serializer for general Python objects using JSON format.
    
    This serializer handles:
    - Dictionaries
    - Lists and tuples
    - Primitive types (str, int, float, bool, None)
    - Dataclasses
    - Objects with __dict__ attribute (converted to dict)
    
    Objects are converted to standard JSON format bytes.
    """

    @property
    def format(self) -> str:
        return "json"

    def serialize(self, value: Any) -> bytes:
        """
        Serialize an object to JSON bytes.
        
        Args:
            value: The object to serialize.
        
        Returns:
            UTF-8 encoded JSON bytes.
        """
        json_data = self._to_json_compatible(value)
        return json.dumps(json_data, indent=2, ensure_ascii=False).encode("utf-8")

    def deserialize(self, data: bytes) -> Any:
        """
        Deserialize JSON bytes to a Python object.
        
        Args:
            data: The JSON bytes to deserialize.
        
        Returns:
            The deserialized Python object (dict, list, or primitive).
        """
        return json.loads(data.decode("utf-8"))

    def _to_json_compatible(self, value: Any) -> Any:
        """
        Convert a Python object to a JSON-compatible structure.
        
        Args:
            value: The object to convert.
        
        Returns:
            A JSON-compatible representation of the object.
        """
        # Handle None and primitives
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        
        # Handle dataclasses
        if is_dataclass(value) and not isinstance(value, type):
            return asdict(value)
        
        # Handle dictionaries
        if isinstance(value, dict):
            return {str(k): self._to_json_compatible(v) for k, v in value.items()}
        
        # Handle lists and tuples
        if isinstance(value, (list, tuple)):
            return [self._to_json_compatible(item) for item in value]
        
        # Handle objects with __dict__
        if hasattr(value, "__dict__"):
            return {k: self._to_json_compatible(v) for k, v in value.__dict__.items()}
        
        # Last resort: convert to string
        return str(value)

