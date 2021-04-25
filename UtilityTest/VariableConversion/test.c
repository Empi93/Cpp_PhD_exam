/* libreria di test per CFFI
 */
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <float.h>

#include "test.h"

double * FloatArrayManaging (int VecLen, float *Array)
{
    double *x;                  // Gamma ray energy
    int i=0;
     
    x = (double*)malloc(sizeof(double)*VecLen);
    if (x == NULL){
        printf("Allocation failed test 1");
        fflush(stdout);
        exit(1);
    } 

    for (i=0;i<VecLen;i++){
        x[i]=0.;
    }

    x[1] = 1.;

    printf("DURING test function excecution\nInputArray: ");
    for (i=0; i<VecLen; i++){
        printf("%.2f ", Array[i]);
    }
    printf("\n\n");

    Array[1] = 3.;
    
    return x; 
}

double ** FloatMatrixManaging (int dim1, int dim2, float **Matrix)
{
    double **x;                  // Gamma ray energy
    int i=0, j=0;
     
    x = (double**)malloc(sizeof(double*)*dim1);
    for (i=0; i<dim2; i++){
        x[i] = (double*)malloc(sizeof(double)*dim2);
    }
    if (x == NULL){
        printf("Allocation failed test 1");
        fflush(stdout);
        exit(1);
    } 

    for (i=0;i<dim1;i++){
        for (j=0;j<dim2;j++){
            x[i][j]=0.;
        }
    }

    x[1][1] = 1.;

    printf("DURING test function excecution\nInputArray: ");
    for (i=0;i<dim1;i++){
        for (j=0;j<dim2;j++){
            printf("%.2f ", Matrix[i][j]);
        }
    }
    printf("\n\n");

    Array[1] = 3.;
    
    return x; 
}


