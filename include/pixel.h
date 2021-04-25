#ifndef _PIXEL_H_
#define _PIXEL_H_

//#include <iostream>
//#include <cmath>
//#include <vector>
#include "preprocessor_directives.h"

#define N_VERTICES 4
#define N_COORDINATES 2

class pixel
{
public:
    // default ctor
    pixel();
    // ctors
    pixel(float* R, float* z);
    pixel(float coordinates[4][2]);
    // dtor
    ~pixel();

    // operator
    bool operator == (const pixel& PixelToCompare);

    // methods for ctors
    void FindMaxMinCoordinates();

    // Setters
    void SetCoordinates(float coordinates[4][2]);

    // Getters
    float GetRM() const;
    float GetRm() const;
    float GetzM() const;
    float Getzm() const;

    // Printer
    void Print() const;
    void PrintAll() const;

    private:
        float coordinates_p[N_VERTICES][N_COORDINATES];
        float RM_p, Rm_p;
        float zM_p, zm_p;
};

#endif // _PIXEL_H_
