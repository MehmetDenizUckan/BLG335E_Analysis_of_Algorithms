"""
CEN335E - Analysis of Algorithms I - Project 1 (Fall 2026)
Sorting Under the Microscope: Counting, Randomness and Adversaries

Student name : ____________________
Student ID   : ____________________

Read Project1.pdf first. Section 3 of Project1.pdf is the SPECIFICATION of every function below.
The autograder counts element comparisons, so follow the pseudocode in Project1.pdf exactly:
the same comparisons, in the same order, with the same operators.

Rules
  * Do not change any function name or signature.
  * Do not use sorted(), list.sort(), heapq, bisect, min()/max() on elements, or any library sort
    inside the functions you implement. You MAY use sorted() in your own tests as an oracle.
  * Only the Python standard library. Plotting in your report may use matplotlib (optional).
  * Compare elements only with <, <=, > and >=. Never compare elements with ==.
"""

import math
import random
import time

STUDENT_ID = "820210338"          # <-- write your student number here; it seeds all your experimen ffts
RESEARCH_TRACK = "R2"     # <-- choose exactly one: "R1", "R2" or "R3" (Project1.pdf, Section 4)


# =====================================================================================
# PART A - Lecture algorithms (Weeks 1-4)                                   [A1-A6]     
# =====================================================================================
def insertion_sort(A, p=0, r=None):
    """Sort A[p..r] (inclusive, 0-based) in place. Returns None."""
    if r is None:
        r = len(A) - 1
    
    for j in range(p + 1, r + 1):
        key = A[j]
        i = j - 1
      
        while i >= p and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key

def merge(A, p, q, r):
    """Merge sorted A[p..q] and A[q+1..r] in place, stably, WITHOUT sentinels."""
    n1 = q - p + 1
    n2 = r - q

    L = A[p : q + 1]
    R = A[q + 1 : r + 1]

    i = 0
    j = 0
    k = p

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1
        k += 1
    
    if i < len(L):
        A[k : r + 1] = L[i:]
    elif j < len(R):
        A[k : r + 1] = R[j:]

def merge_sort(A, p=0, r=None):
    """Top-down merge sort of A[p..r] in place with q = (p + r) // 2. Returns None."""
    if r is None:
        r = len(A) - 1

    if r > p:
        q = (p + r) // 2  
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


def partition(A, p, r):
    """Lomuto PARTITION of A[p..r] around x = A[r]. Returns the pivot's final index."""
    # TODO A3
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


def choose_pivot(A, p, r, pivot, rng):
    """Move the pivot chosen by rule 'last', 'random' or 'median3' into A[r]."""
    # TODO A3
    if pivot == "last":
        return
    elif pivot == "random":
        k = rng.randint(p, r)
        A[k], A[r] = A[r], A[k]
    elif pivot == "median3" and r - p + 1 >= 3:
            m = (p + r) // 2
            # Strict comparison order from Section 3:
            if A[m] < A[p]:
                A[m], A[p] = A[p], A[m]
            if A[r] < A[p]:
                A[r], A[p] = A[p], A[r]
            if A[r] < A[m]:
                A[r], A[m] = A[m], A[r]
            A[m], A[r] = A[r], A[m]



def quicksort(A, pivot="last", rng=None, cutoff=2):
    """In-place quicksort with smaller-side recursion and an insertion-sort cutoff. Returns None."""
    if len(A) <= 1:
        return
    if pivot == "random" and rng is None:
        rng = random.Random()
    # TODO A3 + A4 (you may add a helper function) 

    S = max(cutoff, 2)

    def QS(p, r):
        while r - p + 1 >= S:
            choose_pivot(A, p, r, pivot, rng)
            q = partition(A, p, r)
            if q - p < r - q:
                # Left side is strictly smaller -> recurse left, loop right
                QS(p, q - 1)
                p = q + 1
            else:
                # Right side is smaller or equal -> recurse right, loop left
                QS(q + 1, r)
                r = q - 1
        if p < r:
            insertion_sort(A, p, r)

    QS(0, len(A) - 1)


def quickselect(A, k, rng):
    """Return the k-th smallest element of A (k is 1-based). A may be rearranged."""
    # TODO A5
    p = 0 
    r = len(A) - 1
    while True:
        if p == r:
            return A[p]
        idx = rng.randint(p, r)
        A[idx], A[r] = A[r], A[idx]
        q = partition(A, p, r)
        rank = q - p + 1
        if k == rank:
            return A[q]
        elif k < rank:
            r = q - 1
        else:
            k = k - rank
            p = q + 1


def count_inversions(A):
    """Return the number of pairs i < j with A[i] > A[j], in O(n lg n) time, without changing A."""
    arr = list(A)
    
    def merge_and_count(p, q, r):
        L = arr[p : q + 1]
        R = arr[q + 1 : r + 1]
        
        i = 0
        j = 0
        k = p
        len_L = len(L)
        len_R = len(R)
        inv_count = 0
        
        while i < len_L and j < len_R:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                inv_count += len_L - i
                j += 1
            k += 1
            
        while i < len_L:
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len_R:
            arr[k] = R[j]
            j += 1
            k += 1
            
        return inv_count

    def sort_and_count(p, r):
        if p >= r:
            return 0
        q = (p + r) // 2
        left_inv = sort_and_count(p, q)
        right_inv = sort_and_count(q + 1, r)
        split_inv = merge_and_count(p, q, r)
        return left_inv + right_inv + split_inv

    if len(arr) <= 1:
        return 0

    return sort_and_count(0, len(arr) - 1)  




# =====================================================================================
# PART B - The adversary                                                    [A7]        
# =====================================================================================

def quadratic_input(n):
    """Return a list of n integers on which quicksort(A, pivot='median3') makes at least n*n/8
    element comparisons."""
    # TODO A7
    raise NotImplementedError


# =====================================================================================
# PART C - Research track: implement ONLY the track named in RESEARCH_TRACK  [Section 4]
# =====================================================================================

# ---- R1: Powersort merge policy --------------------------------------------------------
def node_power(s1, n1, n2, n):
    # TODO R1
    raise NotImplementedError


def powersort(A):
    # TODO R1
    raise NotImplementedError


# ---- R2: Skip-merge mergesort -------------------------------------------------------------
def skip_merge_sort(A, p=0, r=None):
    # TODO R2
    raise NotImplementedError


# ---- R3: Two-stage approximate top-K ------------------------------------------------------
def exact_topk(A, K, rng):
    # TODO R3
    raise NotImplementedError


def two_stage_topk(A, K, B, Kp):
    # TODO R3
    raise NotImplementedError


def recall_at_k(approx, exact):
    # TODO R3
    raise NotImplementedError


# =====================================================================================
# PROVIDED HELPERS - do not modify
# =====================================================================================

class Counted:
    """Wraps a value every <, <=, >, >=, == between Counted objects adds 1 to Counted.count.
    The autograder uses exactly this class to count your comparisons."""
    count = 0
    __slots__ = ("v", "tag")

    def __init__(self, v, tag=None):
        self.v = v
        self.tag = tag            # e.g. the original position, to test stability

    def __lt__(self, o):
        Counted.count += 1
        return self.v < o.v

    def __le__(self, o):
        Counted.count += 1
        return self.v <= o.v

    def __gt__(self, o):
        Counted.count += 1
        return self.v > o.v

    def __ge__(self, o):
        Counted.count += 1
        return self.v >= o.v

    def __eq__(self, o):
        Counted.count += 1
        return self.v == o.v

    __hash__ = None

    def __repr__(self):
        return f"Counted({self.v})"


def count_comparisons(sort_call, data):
    """Run sort_call on a wrapped copy of data. Returns (number of comparisons, resulting values).

    Example:  c, out = count_comparisons(lambda W: quicksort(W, "median3"), [5, 2, 4, 6, 1, 3])
    """
    W = [Counted(x) for x in data]
    Counted.count = 0
    sort_call(W)
    return Counted.count, [w.v for w in W]


def harmonic(n):
    """H_n = 1 + 1/2 + ... + 1/n."""
    return sum(1.0 / k for k in range(1, n + 1))


def make_data(kind, n, seed):
    """Reproducible test inputs. kind is one of
       'random'   : a random permutation of 0..n-1 (all distinct)
       'dups'     : n random values from {0, ..., 9}
       'sorted'   : 0, 1, ..., n-1
       'reverse'  : n-1, ..., 1, 0
       'nearly'   : sorted, then n // 100 random adjacent swaps
       'runs8'    : 8 sorted runs of (almost) equal length, values interleaved at random
    """
    rng = random.Random(f"{seed}-{kind}-{n}")
    if kind == "random":
        A = list(range(n))
        rng.shuffle(A)
        return A
    if kind == "dups":
        return [rng.randrange(10) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n - 1, -1, -1))
    if kind == "nearly":
        A = list(range(n))
        for _ in range(n // 100):
            i = rng.randrange(max(n - 1, 1))
            if i + 1 < n:
                A[i], A[i + 1] = A[i + 1], A[i]
        return A
    if kind == "runs8":
        vals = list(range(n))
        rng.shuffle(vals)
        A = []
        for b in range(8):
            chunk = vals[b * n // 8:(b + 1) * n // 8]
            chunk.sort()                      # provided helper: building the input may use sort
            A.extend(chunk)
        return A
    raise ValueError(kind)


def seed():
    """Your personal seed. Use it for every experiment in your report."""
    return int(STUDENT_ID)


def median_time(sort_call, data, repeats=5):
    """Median wall-clock time (seconds) of sort_call on fresh copies of data."""
    times = []
    for _ in range(repeats):
        A = list(data)
        t0 = time.perf_counter()
        sort_call(A)
        times.append(time.perf_counter() - t0)
    times.sort()                              # provided helper: sorting timing results is allowed
    return times[len(times) // 2]


# =====================================================================================
# YOUR EXPERIMENTS - write the code that produces the tables and plots of your report
# =====================================================================================

def run_experiments():
    s = seed()
    # Example: comparisons of randomized quicksort vs. the exact expectation 2(n+1)H_n - 4n
    n = 1000
    c, _ = count_comparisons(lambda W: quicksort(W, "random", random.Random(s)), make_data("random", n, s))
    print("randomized quicksort, n =", n, "comparisons =", c,
          "expected =", round(2 * (n + 1) * harmonic(n) - 4 * n, 1))
    # TODO: your experiments (Project1.pdf, Section 5)


if __name__ == "__main__":
    run_experiments()
