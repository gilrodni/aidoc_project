"""NumPy array serializer."""

from io import BytesIO
from typing import Any

import numpy as np

from .base import Serializer


class NumpySerializer(Serializer):
    """
    Serializer for NumPy arrays using the native .npy format.
    
    This serializer converts NumPy arrays to/from bytes in the standard
    .npy format, which preserves the array's dtype, shape, and data exactly.
    """

    @property
    def format(self) -> str:
        return "npy"

    def serialize(self, value: Any) -> bytes:
        """
        Serialize a NumPy array to bytes in .npy format.
        
        Args:
            value: The NumPy array to serialize.
        
        Returns:
            The .npy formatted bytes.
        """
        buffer = BytesIO()
        np.save(buffer, value)
        return buffer.getvalue()

    def deserialize(self, data: bytes) -> np.ndarray:
        """
        Deserialize bytes to a NumPy array.
        
        Args:
            data: The .npy formatted bytes.
        
        Returns:
            The deserialized NumPy array.
        """
        buffer = BytesIO(data)
        return np.load(buffer)


