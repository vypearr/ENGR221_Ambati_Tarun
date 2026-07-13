"""
Author: Tarun Ambati
Last updated: July 12, 2026
Description: Defines custom Queue and Stack data structures used by the
Duck Collector search algorithms. Queue is FIFO behavior for BFS, and
Stack is FILO behavior for DFS.
"""

class Queue():
    def __init__(self):
        self.items = []

    def add(self, item) -> None:
        """ "Enqueue" the item to the end of the queue """
        self.items.append(item)

    def remove(self):
        """ Dequeue" the item from the queue and return it """
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self) -> bool:
        """ Returns whether or not the queue is empty """
        return len(self.items) == 0
    

class Stack():
    def __init__(self):
        self.items = []

    def add(self, item) -> None:
        """ Push an item to the top of the stack """
        self.items.append(item)

    def remove(self):
        """ Pop an item from the stack and return it """
        if self.is_empty():
            return None
        return self.items.pop()
    
    def is_empty(self) -> bool:
        """ Returns whether or not the stack is empty """
        return len(self.items) == 0