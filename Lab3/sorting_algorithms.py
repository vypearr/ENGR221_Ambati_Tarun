""" TODO
Author: Tarun Ambati
Last updated: 2026-07-05
Description: Comparing selection sort, insertion sort, and bubble sort 
"""

import random
import time

from preferences import Preferences


class SortingAlgorithms:
    """Stores the array and generator-based sorting algorithms for the visualizer."""

    def __init__(self):
        """Initialize the array, highlighted indices, and current algorithm state."""
        # The algorithm to sort
        self.array = []

        # Any indices to highlight
        self.inner_idx = -1
        self.outer_idx = -1

        # A string representing the current sorting algorithm
        self.current_alg = None

        # Store the method of the sorting algorithm being run
        self.alg_method = None

    def create_new_array(self, length=Preferences.NUM_ELEMENTS) -> list:
        """Create and return a new random array with the requested length."""
        return [random.randint(0, Preferences.MAX_VAL) for _ in range(length)]

    def get_next_step(self) -> None:
        """Advance the current sorting generator by one step.

        Each sorting method yields two indices. Those indices tell the display
        which bars should be highlighted at the current step.
        """
        try:
            # Treats the current sorting algorithm as an iterator and gets the
            # next pair of indices that should be highlighted.
            self.outer_idx, self.inner_idx = next(self.alg_method)
        except StopIteration:
            # When the sort finishes, clear the highlighted indices.
            self.outer_idx, self.inner_idx = -1, -1

    def restart(self, new_alg, length=Preferences.NUM_ELEMENTS) -> None:
        """Restart the sorting process with a new algorithm and random array."""
        self.current_alg = new_alg
        self.alg_method = {
            "selection": self.selection_sort,
            "insertion": self.insertion_sort,
            "bubble": self.bubble_sort,
        }[self.current_alg]()
        self.array = self.create_new_array(length)
        self.outer_idx, self.inner_idx = -1, -1

    def selection_sort(self):
        """Sort self.array using selection sort.

        Selection sort repeatedly selects the smallest value from the unsorted
        part of the array and swaps it into the next sorted position. This is a
        generator so the GUI can show each step with yield.
        """
        n = len(self.array)

        # Move the boundary between the sorted and unsorted sections.
        for i in range(n):
            # Start by assuming the current index contains the smallest value.
            yield -1, i
            min_idx = i

            # Search the remaining unsorted portion for a smaller value.
            for j in range(i + 1, n):
                # Highlight the current minimum and the value being checked.
                yield min_idx, j

                if self.array[j] < self.array[min_idx]:
                    min_idx = j

            # Put the smallest value found into its final sorted position.
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            yield i, min_idx

    def insertion_sort(self):
        """Sort self.array using insertion sort.

        Insertion sort builds a sorted left side of the array. Each new item is
        inserted into the correct place by swapping it left until it is no
        longer smaller than the item before it. This modifies the original list
        in place and yields highlighted indices for the visualizer.
        """
        n = len(self.array)

        for i in range(n):
            # The item at i is the next item we are inserting into the sorted side.
            j = i
            yield i, j

            # Shift the current item left until the left side is sorted again.
            while j > 0 and self.array[j - 1] > self.array[j]:
                yield j - 1, j
                self.array[j], self.array[j - 1] = self.array[j - 1], self.array[j]
                j -= 1
                yield j, i

    def bubble_sort(self):
        """Sort self.array using bubble sort.

        Bubble sort repeatedly compares neighboring values and swaps them when
        they are out of order. After each full pass, the largest remaining value
        has bubbled to the end of the unsorted section. This modifies the list
        in place and yields highlighted indices for the visualizer.
        """
        n = len(self.array)

        for i in range(n - 1):
            # The final i elements are already in their correct positions.
            for j in range(n - 1 - i):
                yield i, j

                # Swap adjacent values if they are out of order.
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]

                yield i, j + 1

    def get_runtime(self) -> float:
        """Return how many seconds the current algorithm takes to finish."""
        # Get the time before running.
        start_time = time.time()

        # Run through every yielded step until the generator is finished.
        for _ in self.alg_method:
            pass

        # Get the time after running.
        end_time = time.time()

        # Return the elapsed time.
        return end_time - start_time


if __name__ == "__main__":
    s = SortingAlgorithms()
    s.restart("bubble", 10000)
    print(s.get_runtime())
