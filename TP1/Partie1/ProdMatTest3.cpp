#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"

Matrix operator*(const Matrix& A, const Matrix& B) {
    assert(A.nbCols == B.nbRows);
    Matrix C(A.nbRows, B.nbCols, 0.0);

    #pragma omp parallel for
    for (int i = 0; i < A.nbRows; i++) {
        for (int k = 0; k < A.nbCols; k++) {
            for (int j = 0; j < B.nbCols; j++) {
                C(i, j) += A(i, k) * B(k, j);
            }
        }
    }
    return C;
}
