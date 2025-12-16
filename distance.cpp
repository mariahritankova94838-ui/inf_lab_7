#include "distance.h"
#include <cmath>


DISTANCE_API double vector_distance(const double* vec1, const double* vec2, int size) {
    if (size <= 0 || vec1 == nullptr || vec2 == nullptr) {
        return 0.0;
    }

    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        double diff = vec1[i] - vec2[i];
        sum += diff * diff;
    }

    return sqrt(sum);
}


DISTANCE_API double vector_distance_n_times(const double* vec1, const double* vec2, int size, int iterations) {
    if (iterations <= 0) {
        return 0.0;
    }

    double total = 0.0;
    for (int i = 0; i < iterations; i++) {
        total += vector_distance(vec1, vec2, size);
    }

    return total;
}