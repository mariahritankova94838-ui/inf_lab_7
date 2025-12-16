#pragma once

#ifdef _WIN32
#ifdef DISTANCE_EXPORTS
#define DISTANCE_API __declspec(dllexport)
#else
#define DISTANCE_API __declspec(dllimport)
#endif
#else
#define DISTANCE_API
#endif

extern "C" {
    DISTANCE_API double vector_distance(const double* vec1, const double* vec2, int size);
    DISTANCE_API double vector_distance_n_times(const double* vec1, const double* vec2, int size, int iterations);
}