#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"

namespace {

 // 包含OpenMP头文件


const int szBlock = 1024; // 设定块大小

void prodSubBlocks(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                   const Matrix& A, const Matrix& B, Matrix& C) {
    for (int i = iRowBlkA; i < std::min(A.nbRows, iRowBlkA + szBlock); ++i) {
        for (int k = iColBlkA; k < std::min(A.nbCols, iColBlkA + szBlock); ++k) {
            for (int j = iColBlkB; j < std::min(B.nbCols, iColBlkB + szBlock); ++j) {
                C(i, j) += A(i, k) * B(k, j);
            }
        }
    }
}
}

Matrix operator*(const Matrix& A, const Matrix& B) {
    Matrix C(A.nbRows, B.nbCols, 0.0);

    // 进行块分解计算
    for (int iRowBlkA = 0; iRowBlkA < A.nbRows; iRowBlkA += szBlock) {
        for (int iColBlkB = 0; iColBlkB < B.nbCols; iColBlkB += szBlock) {
            for (int iColBlkA = 0; iColBlkA < A.nbCols; iColBlkA += szBlock) {
                prodSubBlocks(iRowBlkA, iColBlkB, iColBlkA, szBlock, A, B, C);
            }
        }
    }
    return C;
}

