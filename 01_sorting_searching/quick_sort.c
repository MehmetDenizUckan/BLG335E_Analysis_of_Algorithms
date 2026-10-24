#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "algo_utils.h"

static inline void swap_tracked(int *a, int *b, OpMetrics *metrics) {
    int t = *a;
    *a = *b;
    *b = t;
    if (metrics) {
        metrics->shifts += 3;
    }
}

int partition(int *arr, int p, int r, OpMetrics *metrics) {
    int pivot_idx = rand() % (r - p + 1) + p;
    swap_tracked(&arr[pivot_idx], &arr[r], metrics);
    int pivot = arr[r];
    int i = p - 1;
    for (int j = p; j < r; j++) {
        if (metrics) {
            metrics->comparisons++;
        }
        if (arr[j] <= pivot) {
            i++;
            swap_tracked(&arr[i], &arr[j], metrics);
        }
    }
    swap_tracked(&arr[i + 1], &arr[r], metrics);
    return i + 1;
}

void quick_sort(int *arr, int p, int r, OpMetrics *metrics) {
    if (p < r) {
        int q = partition(arr, p, r, metrics);
        quick_sort(arr, p, q - 1, metrics);
        quick_sort(arr, q + 1, r, metrics);
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
    quick_sort(arr, 0, size - 1, &metrics);
    printf("\nSorted array:\n");
    print_array(arr, size);
    printf("\n--- Metrics ---\n");
    printf("Comparisons : %llu\n", metrics.comparisons);
    printf("Data Moves  : %llu\n", metrics.shifts);
    free(arr);
    return 0;
}
