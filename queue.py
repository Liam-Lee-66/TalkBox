class SimpleQueue:
    """
    A simple implementation of a queue with basic functionalities.

    Attributes:
        _items (list): Internal storage for the queue's items.
    """

    def __init__(self):
        """
        Initializes an empty queue.
        """
        self._items = []

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.

        Args:
            item: The item to be added to the queue.
        """
        self._items.append(item)

    def dequeue(self):
        """
        Removes and returns the item from the front of the queue.
        If the queue is empty, returns None.

        Returns:
            The item at the front of the queue or None if the queue is empty.
        """
        if not self.is_empty():
            return self._items.pop(0)
        return None

    def size(self):
        """
        Returns the number of items in the queue.

        Returns:
            The size of the queue.
        """
        return len(self._items)

    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return len(self._items) == 0

    def __str__(self):
        """
        Provides a string representation of the queue's contents.

        Returns:
            A string representation of the queue.
        """
        return str(self._items)

# Example usage
if __name__ == "__main__":
    q = SimpleQueue()
    q.enqueue("Hello")
    q.enqueue("World")
    print("Queue contents:", q)
    print("Queue size:", q.size())
    print("Dequeue:", q.dequeue())
    print("Queue contents after dequeue:", q)
    print("Dequeue:", q.dequeue())
    print("Queue is empty:", q.is_empty())
