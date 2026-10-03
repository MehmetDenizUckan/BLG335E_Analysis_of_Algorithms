#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "algo_utils.h"

void insertion_sort(int *arr, int size, OpMetrics *metrics) {
    for (int j = 1; j < size; j++) {
        int key = arr[j];
        int i = j - 1;
        while (i >= 0) {
            metrics->comparisons++;
            if (arr[i] > key) {
                arr[i + 1] = arr[i];
                metrics->shifts++;
                i--;
            } else {
                break;
            }
        }
        arr[i + 1] = key;
    }
}

int main(void) {
    srand(time(NULL));
    int size = 100;
    int *array = generate_random_array(size, 100);

    printf("Original: ");
    print_array(array, size);

    OpMetrics metrics = {0, 0};
    insertion_sort(array, size, &metrics);

    printf("Sorted:   ");
    print_array(array, size);
    printf("Comparisons: %llu | Shifts: %llu\n", metrics.comparisons, metrics.shifts);

    free(array);
    return 0;
}
