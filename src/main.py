"""Example usage of the generic storage API."""

import numpy as np
from storage import LocalFileStorage


class SomeClass:
    """Example class to demonstrate storage of custom objects."""
    
    def __init__(self, text: str, number: float):
        self.txt = text
        self.number = number


def main():
    # Create a local file storage instance
    storage = LocalFileStorage("./my_storage")
    
    # Save 5 instances of SomeClass as JSON
    for i in range(5):
        storage.save(str(i), SomeClass(chr(65 + i), i), "json")
    
    # Print metadata
    print(f"Count: {storage.count()}")  # Output: 5
    print(f"Exists('4'): {storage.exists('4', 'json')}")  # Output: True
    print(f"Exists('5'): {storage.exists('5', 'json')}")  # Output: False
    
    # Load and use a saved object
    obj = storage.get("2", "json")
    print(f"get('2')['number'] + 1 = {obj['number'] + 1}")  # Output: 3
    
    # Save and load a NumPy array
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    storage.save("matrix", arr, "npy")
    
    loaded_arr = storage.get("matrix", "npy")
    print(f"Loaded NumPy array:\n{loaded_arr}")
    
    # Delete an object
    storage.delete("0", "json")
    print(f"Count after delete: {storage.count()}")


if __name__ == "__main__":
    main()
