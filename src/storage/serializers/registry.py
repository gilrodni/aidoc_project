"""Registry for mapping formats to serializers."""

from .base import Serializer


class SerializerRegistry:
    """
    Registry that maps formats to serializers.
    """

    def __init__(self) -> None:
        self._format_map: dict[str, Serializer] = {}

    def register(self, serializer: Serializer) -> None:
        """
        Register a serializer with the registry.
        
        Args:
            serializer: The serializer instance to register.
        """
        self._format_map[serializer.format] = serializer

    def get(self, format: str) -> Serializer:
        """
        Get the serializer for a given format.
        
        Args:
            format: The format name (e.g., 'json', 'npy').
        
        Returns:
            The serializer registered for that format.
        
        Raises:
            KeyError: If no serializer is registered for the format.
        """
        if format not in self._format_map:
            raise KeyError(f"No serializer registered for format: {format}")
        return self._format_map[format]

    @property
    def supported_formats(self) -> list[str]:
        """Get a list of all supported formats."""
        return list(self._format_map.keys())
