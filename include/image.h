#ifndef _IMAGE_H_
#define _IMAGE_H_
#include "preprocessor_directives.h"
#include "pixel.h"
#include <vector>

class image
{
public:
    // default ctor
    image();
    // ctors
    image  (float Rm, float RM, float zm, float zM, int dimR, int dimz) {;}
    image  (float* R, float* z, float Rm, float RM, 
            float zm, float zM, int dimR, int dimz) {;}
    image  (float** coordinates, float Rm, float RM, 
            float zm, float zM, int dimR, int dimz) {;}
    image  (float coordinates[][4][2], float Rm, float RM, 
            float zm, float zM, int dimR, int dimz);
    // dtor
    virtual ~image();

    // Getters
    virtual float GetPixelRM(int i) const;
    virtual float GetPixelRm(int i) const;
    virtual float GetPixelzM(int i) const;
    virtual float GetPixelzm(int i) const;

    // Printer
    virtual void Print() const{;}

    protected:
        std::vector<pixel> pixels;
        int     dimR_p, dimz_p;

    private:
        float   RM_p, Rm_p, zM_p, zm_p;
};

#endif // _IMAGE_H_