"""
Public tests for CEN335E Project 1.   Run:  python tests_public.py

These tests check correctness and a few exact comparison counts on small, fixed inputs.
The grading tests are different and stricter: other inputs, other seeds, exact counts for every
algorithm, stability, a recursion-depth limit and time limits. Passing these tests is necessary,
not sufficient.
"""
import random
import sys
import traceback

import project1 as P

results = []


def check(name, fn):
    try:
        fn()
        results.append((name, True, ""))
    except NotImplementedError:
        results.append((name, False, "not implemented"))
    except AssertionError as e:
        results.append((name, False, str(e)))
    except Exception as e:  # noqa: BLE001
        results.append((name, False, f"{type(e).__name__}: {e}"))
        traceback.print_exc()


def sorts_correctly(call, label, trials=200):
    rng = random.Random(2026)
    for _ in range(trials):
        n = rng.randint(0, 40)
        A = [rng.randint(-20, 20) for _ in range(n)]
        B = list(A)
        call(B)
        assert B == sorted(A), f"{label}: {A} -> {B}"


def count(call, data):
    c, out = P.count_comparisons(call, data)
    assert out == sorted(data), "wrong result"
    return c


# ---- Part A -------------------------------------------------------------------------------
def a1():
    sorts_correctly(P.insertion_sort, "insertion_sort")
    assert count(P.insertion_sort, [5, 2, 4, 6, 1, 3]) == 12, "insertion_sort [5,2,4,6,1,3] must make 12"
    assert count(P.insertion_sort, list(range(8, 0, -1))) == 28, "reverse n=8 must make 28"
    A = [9, 8, 7, 6, 5]
    P.insertion_sort(A, 1, 3)
    assert A == [9, 6, 7, 8, 5], "insertion_sort(A, p, r) must sort only A[p..r]"


def a2():
    sorts_correctly(P.merge_sort, "merge_sort")
    assert count(P.merge_sort, list(range(8))) == 12, "merge_sort on sorted n=8 must make 12"
    assert count(P.merge_sort, [5, 2, 4, 7, 1, 3, 2, 6]) == 17, "merge_sort CLRS Fig. 2.4 must make 17"


def a3():
    A = [2, 8, 7, 1, 3, 5, 6, 4]
    c, out = P.count_comparisons(lambda W: P.partition(W, 0, 7), A)
    assert out == [2, 1, 3, 4, 7, 5, 6, 8] and c == 7, f"partition CLRS Fig. 7.1 gave {out}, {c} comparisons"
    for rule in ("last", "random", "median3"):
        sorts_correctly(lambda B: P.quicksort(B, rule, random.Random(1)), f"quicksort {rule}")
    assert count(lambda W: P.quicksort(W, "last"), list(range(100))) == 4950, "last pivot, sorted n=100 must make 4950"
    assert count(lambda W: P.quicksort(W, "median3"), list(range(100))) == 588, "median3, sorted n=100 must make 588"
    c = count(lambda W: P.quicksort(W, "random", random.Random(7)), [5, 2, 4, 7, 1, 3, 2, 6, 9, 0])
    assert c == 21, f"random pivot with random.Random(7) on the 10-element example: {c}, expected 21"


def a4():
    sorts_correctly(lambda B: P.quicksort(B, "median3", None, 6), "quicksort cutoff 6")
    assert count(lambda W: P.quicksort(W, "last", None, 10), list(range(50))) == 1197, "last pivot, cutoff 10, sorted n=50 must make 1197"
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(120)
    try:
        A = list(range(1500))
        P.quicksort(A, "last")
    finally:
        sys.setrecursionlimit(old)
    assert A == list(range(1500))


def a5():
    rng = random.Random(5)
    for t in range(200):
        n = rng.randint(1, 30)
        A = [rng.randint(0, 9) for _ in range(n)]
        k = rng.randint(1, n)
        assert P.quickselect(list(A), k, random.Random(t)) == sorted(A)[k - 1], f"quickselect k={k} on {A}"


def a6():
    assert P.count_inversions([2, 3, 8, 6, 1]) == 5, "CLRS Problem 2-4: <2,3,8,6,1> has 5 inversions"
    assert P.count_inversions([5, 2, 4, 6, 1, 3]) == 9
    A = [3, 1, 2]
    P.count_inversions(A)
    assert A == [3, 1, 2], "count_inversions must not modify its input"


def a7():
    K = P.quadratic_input(200)
    assert isinstance(K, list) and len(K) == 200 and all(isinstance(x, int) for x in K), "200 ints"
    c = count(lambda W: P.quicksort(W, "median3"), K)
    assert c >= 200 * 200 / 8, f"only {c} comparisons on n=200; need at least 5000"


# ---- research tracks ----------------------------------------------------------------------
def r1():
    sorts_correctly(P.powersort, "powersort")
    assert P.node_power(0, 5, 3, 16) == 2 and P.node_power(0, 50, 50, 100) == 1, "node_power"
    assert count(P.powersort, list(range(100))) == 99, "sorted input: n-1 comparisons"
    assert count(P.powersort, list(range(100, 0, -1))) == 99, "decreasing input: n-1 comparisons"


def r2():
    sorts_correctly(P.skip_merge_sort, "skip_merge_sort")
    assert count(P.skip_merge_sort, list(range(100))) == 99, "sorted input: n-1 comparisons"


def r3():
    A = [5, 1, 9, 9, 3, 7, 2, 8]
    assert P.exact_topk(list(A), 3, random.Random(1)) == [9, 9, 8]
    assert P.exact_topk(list(A), 0, random.Random(1)) == []
    assert P.two_stage_topk(A, 3, 2, 3) == [9, 9, 8], "exact when Kp >= K"
    assert P.two_stage_topk(list(range(20)), 4, 4, 1) == [19, 14, 9, 4], "one per bucket"
    assert abs(P.recall_at_k([9, 8, 1], [9, 9, 8]) - 2 / 3) < 1e-9, "recall_at_k"


for name, fn in [("A1 insertion_sort", a1), ("A2 merge_sort", a2), ("A3 quicksort", a3),
                 ("A4 cutoff + stack", a4), ("A5 quickselect", a5), ("A6 inversions", a6),
                 ("A7 quadratic_input", a7)]:
    check(name, fn)
track = getattr(P, "RESEARCH_TRACK", "")
if track in ("R1", "R2", "R3"):
    check(f"{track} research track", {"R1": r1, "R2": r2, "R3": r3}[track])
else:
    results.append(("research track", False, "set RESEARCH_TRACK to 'R1', 'R2' or 'R3'"))

print()
for name, ok, msg in results:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:<22} {msg}")
print(f"\n  {sum(ok for _, ok, _ in results)} / {len(results)} public test groups passed.")
if str(getattr(P, "STUDENT_ID", "0")) in ("0", ""):
    print("  Reminder: set STUDENT_ID in project1.py.")
