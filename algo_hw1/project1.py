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
    # TODO A6
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
    """
    Return a list of n integers on which quicksort(A, pivot="median3")
    makes at least n^2 / 8 comparisons.
    """
    val = [None] * n      
    gas = n              
    candidate = None     
    class Element:
        __slots__ = ('idx',)
        def __init__(self, idx):
            self.idx = idx

        def _cmp(self, other):
            nonlocal gas, candidate
            x, y = self.idx, other.idx

          
            if val[x] is not None and val[y] is not None:
                return -1 if val[x] < val[y] else (1 if val[x] > val[y] else 0)

            
            if val[x] is None and val[y] is None:
                if x == candidate:
                   
                    val[y] = n - gas
                    gas -= 1
                    return 1  # x > y
                elif y == candidate:
                    val[x] = n - gas
                    gas -= 1
                    return -1  # x < y
                else:
                    candidate = x
                    val[y] = n - gas
                    gas -= 1
                    return 1  # x > y

            if val[x] is None:
                return 1   # x > y
            else:
                return -1  # x < y

        def __lt__(self, other):
            return self._cmp(other) < 0

        def __le__(self, other):
            return self._cmp(other) <= 0

        def __gt__(self, other):
            return self._cmp(other) > 0

        def __ge__(self, other):
            return self._cmp(other) >= 0

    adversary_arr = [Element(i) for i in range(n)]

    quicksort(adversary_arr, pivot="median3")

    for i in range(n):
        if val[i] is None:
            val[i] = n - gas
            gas -= 1

    return val

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
    if r is None:
        r = len(A)-1 

    if p < r:
        q = (p+r) // 2
        skip_merge_sort(A,p,q)
        skip_merge_sort(A,q+1,r)
        if A[q] <= A[q+1]:
            return
        merge(A,p,q,r)

        



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
    import statistics

    base_s = seed()
    print(f"=== Starting Experiments with Student Seed: {base_s} ===\n")

    # Helper: Harmonic number H_n = sum(1/i for i in 1..n)
    def H(n):
        return sum(1.0 / i for i in range(1, n + 1))

    # =========================================================================
    # EXPERIMENT Q1: Insertion Sort Theory vs Measurements
    # =========================================================================
    print("--- [Q1] Insertion Sort Verification ---")
    print(f"{'n':>6} | {'Mean Meas':>12} | {'Formula E[C]':>12} | {'Rel Error (%)':>14} | {'Exact Formula C == I+(n-1)-m'}")
    print("-" * 75)

    for n in [500, 1000, 2000]:
        measured_c = []
        formula_holds = True
        theoretical_expected = (n * (n - 1)) / 4.0 + n - H(n)

        for run in range(35):  # at least 30 permutations
            s_run = base_s + run * 10007 + n
            A = make_data("random", n, s_run)

            # Inversions I
            I = count_inversions(A)

            # Left-to-right minima count m (positions j >= 1 strictly smaller than all predecessors)
            m = 0
            curr_min = A[0]
            for j in range(1, n):
                if A[j] < curr_min:
                    m += 1
                    curr_min = A[j]

            # Measure actual comparisons in insertion_sort
            c, _ = count_comparisons(lambda W: insertion_sort(W), A)
            measured_c.append(c)

            # Verify exact relation: C = I + (n - 1) - m
            if c != I + (n - 1) - m:
                formula_holds = False

        mean_c = statistics.mean(measured_c)
        rel_err = abs(mean_c - theoretical_expected) / theoretical_expected * 100.0
        print(f"{n:>6} | {mean_c:>12.2f} | {theoretical_expected:>12.2f} | {rel_err:>13.4f}% | {str(formula_holds):>10}")

    print()

    # =========================================================================
    # EXPERIMENT Q2: Randomized Quicksort
    # =========================================================================
    print("--- [Q2] Randomized Quicksort ---")
    print("Part (a): Random Inputs (Mean & Std vs Theory)")
    print(f"{'n':>6} | {'Mean Meas':>12} | {'Std Dev':>10} | {'2(n+1)H_n - 4n':>15} | {'Rel Err (%)':>12}")
    print("-" * 65)

    for n in [100, 1000, 10000]:
        counts = []
        theory_q2 = 2.0 * (n + 1) * H(n) - 4.0 * n
        for run in range(35):
            s_run = base_s + run * 31337 + n
            rng = random.Random(s_run)
            c, _ = count_comparisons(lambda W: quicksort(W, pivot="random", rng=rng), make_data("random", n, s_run))
            counts.append(c)

        mean_val = statistics.mean(counts)
        std_val = statistics.stdev(counts)
        rel_err = abs(mean_val - theory_q2) / theory_q2 * 100.0
        print(f"{n:>6} | {mean_val:>12.2f} | {std_val:>10.2f} | {theory_q2:>15.2f} | {rel_err:>11.2f}%")

    print("\nPart (c): Duplicate Inputs (make_data('dups', n))")
    print(f"{'n':>6} | {'Comparisons':>14} | {'Comp / n^2':>12}")
    print("-" * 40)
    for n in [1000, 2000, 4000]:
        rng = random.Random(base_s + n)
        c, _ = count_comparisons(lambda W: quicksort(W, pivot="random", rng=rng), make_data("dups", n, base_s + n))
        print(f"{n:>6} | {c:>14} | {c / (n * n):>12.4f}")

    print()

    # =========================================================================
    # EXPERIMENT Q3: Cutoff S & Small-n Crossover
    # =========================================================================
    print("--- [Q3] Cutoff Optimization & Crossover ---")
    n_q3 = 100000
    cutoff_candidates = [2, 4, 8, 12, 16, 24, 32, 48, 64]
    print(f"Timing median3 quicksort (n={n_q3}) across cutoffs S (median of 5 runs):")

    best_S = 2
    best_time = float("inf")
    for S in cutoff_candidates:
        times = []
        for run in range(5):
            arr = make_data("random", n_q3, base_s + run * 7919)
            t0 = time.perf_counter()
            quicksort(arr, pivot="median3", cutoff=S)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)  # ms
        med_t = statistics.median(times)
        print(f"  S = {S:>2} -> {med_t:>8.2f} ms")
        if med_t < best_time:
            best_time = med_t
            best_S = S
    print(f"Optimal Cutoff found: S* = {best_S}\n")

    print("Insertion Sort vs. Merge Sort Crossover on Small n (median of 50 runs, in ms):")
    print(f"{'n':>6} | {'Insertion (ms)':>16} | {'MergeSort (ms)':>16} | {'Faster':>12}")
    print("-" * 55)
    for n_small in [4, 8, 16, 24, 32, 48, 64, 96, 128]:
        t_ins, t_mrg = [], []
        for run in range(50):
            seed_run = base_s + run * 997 + n_small
            a1 = make_data("random", n_small, seed_run)
            a2 = list(a1)

            t0 = time.perf_counter()
            insertion_sort(a1)
            t1 = time.perf_counter()
            t_ins.append((t1 - t0) * 1000.0)

            t0 = time.perf_counter()
            merge_sort(a2)
            t1 = time.perf_counter()
            t_mrg.append((t1 - t0) * 1000.0)

        med_ins = statistics.median(t_ins)
        med_mrg = statistics.median(t_mrg)
        winner = "Insertion" if med_ins < med_mrg else "MergeSort"
        print(f"{n_small:>6} | {med_ins:>16.4f} | {med_mrg:>16.4f} | {winner:>12}")

    print()

    # =========================================================================
    # EXPERIMENT Q4: Adversary & Pivot Failure Modes
    # =========================================================================
    print("--- [Q4] Adversary & Pivot Vulnerability ---")
    small_n = 8
    small_adv = quadratic_input(small_n)
    print(f"Adversary input generated for n={small_n}: {small_adv}")

    print("\nScaling quadratic_input on median3 vs. random quicksort:")
    print(f"{'n':>6} | {'Adv (Median3)':>15} | {'Adv / n^2':>11} | {'Adv (Random)':>15} | {'Rand Input (Med3)':>18}")
    print("-" * 75)
    for n in [500, 1000, 2000, 4000]:
        adv_input = quadratic_input(n)
        # 1. Median3 on adversary input
        c_adv_med, _ = count_comparisons(lambda W: quicksort(W, pivot="median3"), list(adv_input))
        # 2. Random pivot on adversary input
        rng = random.Random(base_s + n)
        c_adv_rand, _ = count_comparisons(lambda W: quicksort(W, pivot="random", rng=rng), list(adv_input))
        # 3. Median3 on uniform random input
        c_rand_med, _ = count_comparisons(lambda W: quicksort(W, pivot="median3"), make_data("random", n, base_s + n))

        print(f"{n:>6} | {c_adv_med:>15} | {c_adv_med / (n * n):>11.4f} | {c_adv_rand:>15} | {c_rand_med:>18}")

    print("\nVulnerability of pivot='last' on structured data:")
    for kind in ["nearly", "runs8"]:
        for n in [1000, 2000]:
            c, _ = count_comparisons(lambda W: quicksort(W, pivot="last"), make_data(kind, n, base_s + n))
            print(f"  kind={kind:<7} n={n:>5} -> comparisons={c:>10} (C / n^2 = {c / (n * n):.4f})")

    print()

    # =========================================================================
    # EXPERIMENT Q5: Wall-Clock Benchmarks & Asymptotics
    # =========================================================================
    print("--- [Q5] Wall-Clock Benchmark (ms) & Ratio Tests ---")
    print(f"{'Algorithm':<18} | {'n':>6} | {'Time (ms)':>10} | {'T / n^2 (e-6)':>14} | {'T / (n log n) (e-6)':>20}")
    print("-" * 75)

    q5_ns = [100, 1000, 5000, 20000, 100000]
    algorithms = [
        ("insertion_sort", lambda arr: insertion_sort(arr), [100, 1000, 5000]),
        ("merge_sort", lambda arr: merge_sort(arr), q5_ns),
        ("qs_random", lambda arr: quicksort(arr, pivot="random", rng=random.Random(base_s)), q5_ns),
        (f"qs_med3_S{best_S}", lambda arr: quicksort(arr, pivot="median3", cutoff=best_S), q5_ns),
        ("sorted_cpython", lambda arr: sorted(arr), q5_ns),
    ]

    for name, sort_fn, valid_ns in algorithms:
        for n in valid_ns:
            run_times = []
            for run in range(5):
                arr = make_data("random", n, base_s + run * 4001 + n)
                t0 = time.perf_counter()
                sort_fn(arr)
                t1 = time.perf_counter()
                run_times.append((t1 - t0) * 1000.0)
            med_t = statistics.median(run_times)

            # Ratio tests
            r_n2 = (med_t / (n * n)) * 1e6
            r_nlogn = (med_t / (n * math.log2(n))) * 1e6
            print(f"{name:<18} | {n:>6} | {med_t:>10.2f} | {r_n2:>14.4f} | {r_nlogn:>20.4f}")

    print()

    # =========================================================================
    # PART B: RESEARCH TRACK R2 EXPERIMENTS
    # =========================================================================
    print("--- [Part B: R2] Skip-Merge vs Standard Merge Sort ---")
    print(f"{'Input Kind':<10} | {'Standard Merge (C)':>20} | {'Skip Merge (C)':>16} | {'Difference':>12}")
    print("-" * 65)

    n_r2 = 10000
    for kind in ["random", "nearly", "runs8", "reverse"]:
        data_orig = make_data(kind, n_r2, base_s + 42)
        c_std, _ = count_comparisons(lambda W: merge_sort(W), list(data_orig))
        c_skip, _ = count_comparisons(lambda W: skip_merge_sort(W), list(data_orig))
        diff = c_skip - c_std
        print(f"{kind:<10} | {c_std:>20} | {c_skip:>16} | {diff:>+12}")

    print("\n=== All Experiments Completed Successfully ===")


if __name__ == "__main__":
    run_experiments()
