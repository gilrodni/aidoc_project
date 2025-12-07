"""Abstract base class for storage implementations."""

from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    """
    Abstract base class defining the generic storage API.
    
    All storage implementations (local file system, S3, etc.) should inherit
    from this class and implement all abstract methods.
    """

    @abstractmethod
    def save(self, key: str, value: Any, format: str) -> None:
        """
        Save an object to storage.
        
        Args:
            key: Unique identifier for the object.
            value: The object to save.
            format: The format name (e.g., "json", "npy").
        
        Raises:
            KeyError: If the format is not supported.
        """
        pass

    @abstractmethod
    def get(self, key: str, format: str) -> Any:
        """
        Retrieve an object from storage.
        
        Args:
            key: The unique identifier of the object to retrieve.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            The deserialized object.
        
        Raises:
            KeyError: If the key does not exist in storage.
        """
        pass

    @abstractmethod
    def exists(self, key: str, format: str) -> bool:
        """
        Check if an object exists in storage.
        
        Args:
            key: The unique identifier to check.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            True if the key exists, False otherwise.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get the number of objects currently stored.
        
        Returns:
            The total count of stored objects.
        """
        pass

    @abstractmethod
    def delete(self, key: str, format: str) -> bool:
        """
        Delete an object from storage.
        
        Args:
            key: The unique identifier of the object to delete.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            True if the object was deleted, False if it didn't exist.
        """
        pass
