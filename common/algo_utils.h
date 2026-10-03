#ifndef ALGO_UTILS_H
#define ALGO_UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    unsigned long long comparisons;
    unsigned long long shifts;
} OpMetrics;

static inline void print_array(const int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

static inline int* generate_random_array(int size, int max_val) {
    int *arr = malloc(size * sizeof(int));
    if (!arr) {
        perror("malloc failed");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % max_val;
    }
    return arr;
}

#endif // ALGO_UTILS_H
