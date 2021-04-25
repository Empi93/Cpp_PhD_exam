#ifndef _CPP_BSURFACE_H_
#define _CPP_BSURFACE_H_
#include <vector>
#include "pixel.h"
#include "image.h"

class CPPbsurface : public image
{
public:
    // default ctor
    CPPbsurface ();
    // ctors not implemented
    /*
    CPPbsurface   (float* Rb, float* zb, float Rm, float RM, const float& zm, 
                const int& lenB, const float& zM, const int& dimR, const int& dimz) {;}
    CPPbsurface    (float* Rb, float* zb, float* Rp, float* zp, const float& Rm, 
                const float& RM, const float& zm, const float& zM, 
                const int& lenB, const int& dimR, const int& dimz) {;}
    CPPbsurface   (float* Rb, float* zb, float** coordinates, const float& Rm, 
                const float& RM, const float& zm, const float& zM, 
                const int& lenB, const int& dimR, const int& dimz) {;}
    */
    // ctor implemented
    CPPbsurface   (float* Rb, float* zb, float* m, float* q, float* Case, 
                //float*** coordinates, const float& Rm, const float& RM, 
                float coordinates[][4][2], const float& Rm, const float& RM, 
                const float& zm, const float& zM, const int& lenB, 
                const int& dimR, const int& dimz);
    // dtor
    ~CPPbsurface();

    // Methods for ctors
    void MakeBorderMask();
    void MakeInnerMask(){;}

    // Getters
    int* GetBorderMask();
    int* GetInsideMask();


private:
    int lenB_p;
    std::vector<float>  R_p, z_p, m_p, q_p;       // line coordinates
    std::vector<int>  Case_p;       // line coordinates
    int* BorderMask_p; 
    int* InsideMask_p;        // mask for smoothing
};

#endif // _CPP_BSURFACE_H_