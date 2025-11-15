"""
Sorting Algorithms: Understanding Algorithm Design from First Principles

This module implements various sorting algorithms with performance analysis.
Work through GUIDE.md to understand each algorithm deeply.
"""

from typing import List, Callable, Tuple
from dataclasses import dataclass
import time
import random


@dataclass
class SortMetrics:
    """Metrics collected during sorting."""
    comparisons: int = 0
    swaps: int = 0
    time_seconds: float = 0.0
    algorithm_name: str = ""


# =============================================================================
# Part 1: Simple Sorts (O(n²))
# =============================================================================

def bubble_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Bubble Sort: Repeatedly swap adjacent elements if out of order.

    Challenge: Implement with early stopping optimization
    """
    # TODO: Implement
    # Remember: larger elements "bubble up" to the end
    # Optimization: stop if no swaps made in a pass
    pass


def insertion_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Insertion Sort: Build sorted array one element at a time.

    Challenge: Implement the "card sorting" approach
    """
    # TODO: Implement
    # Remember: maintain a sorted portion, insert each new element
    pass


def selection_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Selection Sort: Repeatedly select minimum and place at beginning.

    Challenge: Why is this always O(n²), even for sorted input?
    """
    # TODO: Implement
    pass


# =============================================================================
# Part 2: Divide and Conquer - Merge Sort
# =============================================================================

def merge(left: List[int], right: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Merge two sorted arrays into one sorted array.

    Challenge: Implement two-pointer technique
    """
    # TODO: Implement
    # Remember: compare front elements, take smaller
    pass


def merge_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Merge Sort: Divide array in half, sort recursively, merge results.

    Time: O(n log n)
    Space: O(n)

    Challenge: Implement divide-and-conquer recursion
    """
    # TODO: Implement
    # Base case: array of size 0 or 1
    # Recursive case: split, sort halves, merge
    pass


# =============================================================================
# Part 3: Quick Sort
# =============================================================================

def partition(arr: List[int], low: int, high: int,
              pivot_strategy: str = "last", metrics: SortMetrics = None) -> int:
    """
    Partition array around pivot.

    Args:
        arr: Array to partition
        low: Start index
        high: End index
        pivot_strategy: "first", "last", "random", or "median3"

    Returns:
        Final position of pivot

    Challenge: Implement in-place partitioning
    """
    # TODO: Implement
    # 1. Choose pivot based on strategy
    # 2. Partition elements around pivot
    # 3. Return pivot's final position
    pass


def quicksort(arr: List[int], low: int = 0, high: int = None,
              pivot_strategy: str = "last", metrics: SortMetrics = None) -> List[int]:
    """
    Quick Sort: Partition around pivot, sort recursively.

    Average: O(n log n)
    Worst: O(n²)
    Space: O(log n) for recursion

    Challenge: Implement with different pivot strategies
    """
    if high is None:
        high = len(arr) - 1

    # TODO: Implement
    # Base case: low >= high
    # Recursive case: partition, sort left and right
    pass


def median_of_three(arr: List[int], low: int, high: int) -> int:
    """
    Find median of first, middle, and last elements.

    Challenge: Why does this improve quicksort?
    """
    # TODO: Implement
    pass


# =============================================================================
# Part 4: Heap Sort
# =============================================================================

def heapify(arr: List[int], n: int, i: int, metrics: SortMetrics = None):
    """
    Maintain max heap property for subtree rooted at index i.

    Challenge: Implement without recursion (bonus: both versions)
    """
    # TODO: Implement
    # Remember: parent at i, children at 2i+1 and 2i+2
    pass


def build_heap(arr: List[int], metrics: SortMetrics = None):
    """
    Build max heap from unsorted array.

    Challenge: Why is this O(n) and not O(n log n)?
    """
    # TODO: Implement
    # Start from last non-leaf node, heapify backwards
    pass


def heap_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Heap Sort: Build max heap, repeatedly extract maximum.

    Time: O(n log n)
    Space: O(1)

    Challenge: Implement in-place
    """
    # TODO: Implement
    # 1. Build max heap
    # 2. Swap root with last element
    # 3. Reduce heap size, re-heapify
    # 4. Repeat
    pass


# =============================================================================
# Part 5: Non-Comparison Sorts
# =============================================================================

def counting_sort(arr: List[int], max_val: int = None,
                 metrics: SortMetrics = None) -> List[int]:
    """
    Counting Sort: Count occurrences, place in order.

    Time: O(n + k) where k is range of values
    Space: O(k)

    Challenge: Implement for integers in known range
    """
    # TODO: Implement
    # 1. Count occurrences
    # 2. Calculate cumulative counts
    # 3. Place elements in output array
    pass


def radix_sort(arr: List[int], metrics: SortMetrics = None) -> List[int]:
    """
    Radix Sort: Sort digit by digit using stable sort.

    Time: O(d × (n + k)) where d is number of digits
    Space: O(n + k)

    Challenge: Implement using counting sort for each digit
    """
    # TODO: Implement
    # 1. Find maximum to determine number of digits
    # 2. Sort by each digit (least to most significant)
    # 3. Use stable sort (counting sort) for each pass
    pass


def bucket_sort(arr: List[float], num_buckets: int = 10,
                metrics: SortMetrics = None) -> List[float]:
    """
    Bucket Sort: Distribute into buckets, sort each, concatenate.

    Average: O(n + k)
    Worst: O(n²)

    Challenge: Implement for floating-point values in [0, 1)
    """
    # TODO: Implement
    # 1. Create buckets
    # 2. Distribute elements
    # 3. Sort each bucket
    # 4. Concatenate results
    pass


# =============================================================================
# Part 6: Analysis and Utilities
# =============================================================================

def is_sorted(arr: List[int]) -> bool:
    """Check if array is sorted."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def generate_test_data(size: int, pattern: str = "random") -> List[int]:
    """
    Generate test data with specific patterns.

    Args:
        size: Size of array
        pattern: "random", "sorted", "reverse", "nearly_sorted", "duplicates"

    Challenge: What patterns stress-test different algorithms?
    """
    # TODO: Implement different patterns
    pass


def benchmark_sort(sort_func: Callable, arr: List[int],
                  name: str = "") -> SortMetrics:
    """
    Benchmark a sorting algorithm.

    Returns:
        Metrics including time, comparisons, swaps
    """
    metrics = SortMetrics(algorithm_name=name)
    arr_copy = arr.copy()

    start_time = time.time()
    result = sort_func(arr_copy, metrics)
    metrics.time_seconds = time.time() - start_time

    assert is_sorted(result), f"{name} did not sort correctly!"
    return metrics


def compare_algorithms(size: int = 1000, pattern: str = "random"):
    """
    Compare all sorting algorithms on same data.

    Challenge: Create informative comparison table
    """
    data = generate_test_data(size, pattern)

    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (insertion_sort, "Insertion Sort"),
        (selection_sort, "Selection Sort"),
        (merge_sort, "Merge Sort"),
        (quicksort, "Quick Sort"),
        (heap_sort, "Heap Sort"),
        (counting_sort, "Counting Sort"),
        (radix_sort, "Radix Sort"),
    ]

    print(f"\nComparing algorithms on {pattern} data (n={size})")
    print("=" * 80)

    # TODO: Benchmark each algorithm and display results
    pass


class SortingVisualizer:
    """
    Visualize sorting algorithms step by step.

    Challenge: Create clear ASCII or graphical visualizations
    """

    def __init__(self, arr: List[int]):
        self.original = arr.copy()
        self.current = arr.copy()
        self.steps = []

    def visualize_step(self, description: str = ""):
        """Capture and display current state."""
        # TODO: Implement visualization
        pass

    def show_all_steps(self):
        """Show all captured steps."""
        # TODO: Implement
        pass


def smart_sort(arr: List[int]) -> Tuple[List[int], str]:
    """
    Intelligently choose sorting algorithm based on data characteristics.

    Challenge: Analyze data and select best algorithm

    Returns:
        Sorted array and explanation of choice
    """
    # TODO: Implement analysis
    # Consider:
    # - Array size
    # - Is it nearly sorted?
    # - Range of values (for counting/radix sort)
    # - Memory constraints

    explanation = "Choosing algorithm based on..."
    # TODO: Choose and apply algorithm

    return arr, explanation


# =============================================================================
# Testing
# =============================================================================

def test_all_sorts():
    """Test all sorting algorithms for correctness."""
    test_cases = [
        [],
        [1],
        [2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [1, 1, 1, 1, 1],
        list(range(100, 0, -1)),
    ]

    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (insertion_sort, "Insertion Sort"),
        (selection_sort, "Selection Sort"),
        (merge_sort, "Merge Sort"),
        (quicksort, "Quick Sort"),
        (heap_sort, "Heap Sort"),
    ]

    print("Testing all sorting algorithms...")
    for sort_func, name in algorithms:
        for test in test_cases:
            result = sort_func(test.copy())
            assert is_sorted(result), f"{name} failed on {test}"
    print("All tests passed!")


if __name__ == "__main__":
    print("Sorting Algorithms: First Principles Implementation")
    print("=" * 80)
    print("\nWork through GUIDE.md to implement each algorithm.")
    print("Run this file to test your implementations.\n")

    # TODO: Uncomment as you implement
    # test_all_sorts()
    # compare_algorithms(size=1000, pattern="random")
    # compare_algorithms(size=1000, pattern="nearly_sorted")
