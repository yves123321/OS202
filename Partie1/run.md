//第一问
g++ TestProductMatrix TestProductMatrix.cpp ProdMatMat.cpp Matrix.cpp -o TestProductMatrix
//第二至七问
g++ TestProductMatrix TestProductMatrix.cpp ProdMatTest2.cpp Matrix.cpp -o TestProductMatrix2
...
//第八问
g++ ProdMatMat.cpp Matrix.cpp test_product_matrice_blas.cpp -o TestProductMatrix8 -lblas