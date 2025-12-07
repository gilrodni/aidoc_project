"""Abstract base class for serializers."""

from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):
    """
    Abstract base class for object serializers.
    
    Serializers handle the conversion of Python objects to/from bytes.
    They are decoupled from storage - the storage layer handles persistence.
    """

    @property
    @abstractmethod
    def format(self) -> str:
        """
        The format identifier for this serializer (e.g., 'json', 'npy').
        
        Returns:
            The format name without any dot prefix.
        """
        pass

    @abstractmethod
    def serialize(self, value: Any) -> bytes:
        """
        Serialize an object to bytes.
        
        Args:
            value: The object to serialize.
        
        Returns:
            The serialized bytes representation.
        """
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> bytes:
        """
        Deserialize bytes back to bytes.
        
        Args:
            data: The bytes to deserialize.
        
        Returns:
            The deserialized bytes.
        """
        pass


