"""Local file system storage implementation."""

from pathlib import Path
from typing import Any

from .base import Storage
from .serializers.registry import SerializerRegistry
from .serializers.numpy_serializer import NumpySerializer
from .serializers.json_serializer import JsonSerializer


class LocalFileStorage(Storage):
    """
    Storage implementation using the local file system.
    
    Objects are stored as files where the filename is the key plus file extension.
    User must specify the format when saving and retrieving.
    
    Example:
        storage = LocalFileStorage("./my_storage")
        storage.save("my_array", np.array([1, 2, 3]), "npy")
        storage.save("my_data", {"key": "value"}, "json")
        
        print(storage.count())  # 2
        print(storage.exists("my_array", "npy"))  # True
        
        arr = storage.get("my_array", "npy")  # Returns numpy array
    """

    # Mapping from format name to file extension
    FORMAT_TO_EXTENSION: dict[str, str] = {
        "json": ".json",
        "npy": ".npy",
    }

    def __init__(self, base_path: str | Path = "./storage") -> None:
        """
        Initialize the local file storage.
        
        Args:
            base_path: The directory path where objects will be stored.
                      Will be created if it doesn't exist.
        """
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize serializer registry
        self._registry = SerializerRegistry()
        self._registry.register(NumpySerializer())
        self._registry.register(JsonSerializer())

    @property
    def base_path(self) -> Path:
        """Get the base storage directory path."""
        return self._base_path

    def _get_extension(self, format: str) -> str:
        """
        Get the file extension for a format.
        
        Args:
            format: The format name.
        
        Returns:
            The file extension (including the dot).
        
        Raises:
            KeyError: If format is not supported.
        """
        if format not in self.FORMAT_TO_EXTENSION:
            raise KeyError(f"Unknown format: {format}")
        return self.FORMAT_TO_EXTENSION[format]

    def _build_path(self, key: str, format: str) -> Path:
        """
        Build the file path for a key and format.
        
        Args:
            key: The storage key.
            format: The format name.
        
        Returns:
            The full file path.
        """
        extension = self._get_extension(format)
        return self._base_path / f"{key}{extension}"

    def save(self, key: str, value: Any, format: str) -> None:
        """
        Save an object to the local file system.
        
        Args:
            key: Unique string identifier for the object.
            value: The object to save.
            format: The format name (e.g., "json", "npy").
        
        Raises:
            KeyError: If the format is not supported.
        """
        serializer = self._registry.get(format)
        file_path = self._build_path(key, format)
        data = serializer.serialize(value)
        file_path.write_bytes(data)

    def get(self, key: str, format: str) -> Any:
        """
        Retrieve an object from storage.
        
        Args:
            key: The unique identifier of the object.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            The deserialized object.
        
        Raises:
            KeyError: If the key does not exist or format not supported.
        """
        serializer = self._registry.get(format)
        file_path = self._build_path(key, format)
        
        if not file_path.exists():
            raise KeyError(f"Key not found: {key}")
        
        data = file_path.read_bytes()
        return serializer.deserialize(data)

    def exists(self, key: str, format: str) -> bool:
        """
        Check if a key exists in storage.
        
        Args:
            key: The key to check.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            True if the key exists, False otherwise.
        """
        file_path = self._build_path(key, format)
        return file_path.exists()

    def count(self) -> int:
        """
        Get the number of stored objects.
        
        Returns:
            The count of objects in storage.
        """
        supported = set(self.FORMAT_TO_EXTENSION.values())
        return sum(1 for f in self._base_path.iterdir() if f.is_file() and f.suffix in supported)

    def delete(self, key: str, format: str) -> bool:
        """
        Delete an object from storage.
        
        Args:
            key: The key of the object to delete.
            format: The format name (e.g., "json", "npy").
        
        Returns:
            True if deleted, False if key didn't exist.
        """
        file_path = self._build_path(key, format)
        if not file_path.exists():
            return False
        
        file_path.unlink()
        return True
