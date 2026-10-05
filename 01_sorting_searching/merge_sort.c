#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "algo_utils.h"

void merge(int *arr, int p, int q, int r, OpMetrics *metrics) {
    int n1 = q - p + 1;
    int n2 = r - q;
    
    int L[n1];
    int R[n2];
    
    // Copy into temp buffers
    for (int i = 0; i < n1; i++) {
        L[i] = arr[p + i];
        metrics->shifts++;
    }
    for (int j = 0; j < n2; j++) {
        R[j] = arr[q + 1 + j];
        metrics->shifts++;
    }
    
    int i = 0;
    int j = 0;
    int k = p;
    
    // Main comparison loop
    while (i < n1 && j < n2) {
        metrics->comparisons++;
        if (L[i] <= R[j]) { 
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        metrics->shifts++;
        k++;
    }
    
    // Cleanup leftovers
    while (i < n1) {
        arr[k] = L[i];
        metrics->shifts++;
        i++;
        k++;
    }
    
    while (j < n2) {
        arr[k] = R[j];
        metrics->shifts++;
        j++;
        k++;
    }
}

void merge_sort(int *arr, int p, int r, OpMetrics *metrics) {
    if (p < r) {
        // Safe against integer overflow: p + (r - p) / 2
        int q = p + (r - p) / 2;
        merge_sort(arr, p, q, metrics);
        merge_sort(arr, q + 1, r, metrics);
        merge(arr, p, q, r, metrics);
    }
}

int main(void) {
    srand(time(NULL));
    int size = 100;
    int *array = generate_random_array(size, 100);
    printf("Original: ");
    print_array(array, size);
    
    OpMetrics metrics = {0, 0};
    merge_sort(array, 0, size - 1, &metrics);
    
    printf("Sorted:   ");
    print_array(array, size);
    printf("Comparisons: %llu | Data Moves: %llu\n", metrics.comparisons, metrics.shifts);
    
    free(array);
    return 0;
}
