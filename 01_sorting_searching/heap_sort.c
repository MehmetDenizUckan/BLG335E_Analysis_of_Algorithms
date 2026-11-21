#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "algo_utils.h"

static inline void swap(int *a, int *b, OpMetrics *m) {
    int t = *a;
    *a = *b;
    *b = t;
    if (m) m->shifts += 3; // 1 swap = 3 element assignments/moves
}

void max_heapify(int *A, int heap_size, int i, OpMetrics *m) {
    while (1) {
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        int largest = i;

        if (l < heap_size) {
            if (m) m->comparisons++;
            if (A[l] > A[largest]) {
                largest = l;
            }
        }

        if (r < heap_size) {
            if (m) m->comparisons++;
            if (A[r] > A[largest]) {
                largest = r;
            }
        }

        if (largest == i) {
            break; // heap property satisfied
        }

        swap(&A[i], &A[largest], m);
        i = largest;
    }
}

void build_max_heap(int *A, int size, OpMetrics *m) {
    for (int i = size / 2 - 1; i >= 0; i--) {
        max_heapify(A, size, i, m);
    }
}

void heap_sort(int *A, int size, OpMetrics *m) {
    build_max_heap(A, size, m);
    for (int i = size - 1; i > 0; i--) {
        swap(&A[0], &A[i], m);
        max_heapify(A, i, 0, m);
    }
}

int main(void) {
    srand((unsigned int)time(NULL));
    const int size = 100;
    const int max_val = 100;

    int *arr = generate_random_array(size, max_val);
    OpMetrics metrics = {0, 0};

    printf("Original array:\n");
    print_array(arr, size);

    heap_sort(arr, size, &metrics);

    printf("\nSorted array:\n");
    print_array(arr, size);
    printf("\nComparisons: %llu | Shifts (moves): %llu\n",
           metrics.comparisons, metrics.shifts);

    free(arr);
    return 0;
}
