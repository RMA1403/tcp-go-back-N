class DynamicArray:
    def __init__(self):
        self.array = []  # Initialize an empty array

    def resize_array(self, new_size):
        current_size = len(self.array)
        if new_size > current_size:
            self.array.extend([None] * (new_size - current_size))

    def insert(self, position, value):
        if position < 0:
            raise ValueError("Position cannot be negative.")
        
        if position >= len(self.array):
            self.resize_array(position + 1)
        
        self.array[position] = value

    def get_value(self, position):
        if position < 0 or position >= len(self.array):
            raise IndexError("Position out of bounds.")
        
        return self.array[position]
    
    def get_size(self):
        return len(self.array)

    def delete_at(self, position):
        if position < 0 or position >= len(self.array):
            raise IndexError("Position out of bounds.")
        
        self.array[position] = None

    def has_value(self):
        return any(item is not None for item in self.array)

    def __str__(self) -> str:
        return str(self.array)