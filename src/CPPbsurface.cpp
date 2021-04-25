#include <iostream>
#include <vector>
#include "../include/pixel.h"
#include "../include/image.h"
#include "../include/preprocessor_directives.h"
#include "../include/CPPbsurface.h"

/**********    CTORS    **********/
CPPbsurface::CPPbsurface ():
    image(),
    lenB_p(0)
{

}

CPPbsurface::CPPbsurface (float* Rb, float* zb, float* m, float* q, float* Case, 
                    float coordinates[][4][2], const float& Rm, const float& RM, 
                    const float& zm, const float& zM, const int& lenB, 
                    const int& dimR, const int& dimz):
    image(coordinates, Rm, RM, zm, zM, dimR, dimz)
{
    // Fill the coordinates vectors
    int j=0;
    for (int i=0; i<lenB-1; ++i){
        if ((Rb[i]!=Rb[i+1])||(zb[i]!=zb[i+1])){
            ++j;
            R_p.push_back(Rb[i]);
            z_p.push_back(zb[i]);
            m_p.push_back(m[i]);
            q_p.push_back(q[i]);
            Case_p.push_back(Case[i]);
        }
    }
    R_p.push_back(Rb[lenB-1]);
    z_p.push_back(zb[lenB-1]);
    lenB_p = j+1;
    
    // Generate masks
    BorderMask_p = new int[dimR*dimz];
    InsideMask_p = new int[dimR*dimz];
    for (int i=0; i<dimR*dimz; ++i){
        BorderMask_p[i] = InsideMask_p[i] = 0;
    }   
    MakeBorderMask(); 
}


/**********    DTOR    **********/
CPPbsurface::~CPPbsurface(){
    R_p.~vector(); 
    z_p.~vector();
    m_p.~vector(); 
    q_p.~vector();
    Case_p.~vector();
    delete[] BorderMask_p; 
    delete[] InsideMask_p;
    pixels.~vector();
}


/**********    METHODS FOR CTORS    **********/
void CPPbsurface::MakeBorderMask(){
    float sRM, sRm, szM, szm;	    // segment R and z, Max and min
    float pRm, pRM, pzm, pzM;       // pixel R and z, Max and min

    // Cycle over image pixels
    for (int i=0; i < dimR_p*dimz_p; i++) {
        // get pixel max-min
        pRm = pixels[i].GetRm();
        pRM = pixels[i].GetRM();
        pzm = pixels[i].Getzm();
        pzM = pixels[i].GetzM();

        // Cycle over surface segments 
        for	(int j=0; j < lenB_p-1; j++) {
            // Sort segment vertices
            if (R_p[j] < R_p[j+1]){
                sRm = R_p[j];
                sRM = R_p[j+1];
            }
            else{
                sRm = R_p[j+1];
                sRM = R_p[j];
            }	
                            
            if (z_p[j]<z_p[j+1]){
                szm = z_p[j];
                szM = z_p[j+1];
            }
            else{
                szm = z_p[j+1];
                szM = z_p[j];
            }
            
            // one vertex of segment inside pixel
            for (int k=0; k<2 ; k++){
                if (   ( pRm <= R_p[j+k] ) && ( R_p[j+k] <= pRM )
                    && ( pzm <= z_p[j+k] ) && ( z_p[j+k] <= pzM )){
                    BorderMask_p[i] = 1 ;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, k+1)
                    #endif
                }
            }
            if (BorderMask_p[i]==1){
                break;
            }
            // m_p != 0 & infty
            if(Case_p[j] == 2){
                if (   ( pzm <= m_p[j]*pRm + q_p[j]) && ( m_p[j]*pRm + q_p[j] <=  pzM )
                    && ( sRm <= pRm ) && ( pRm <= sRM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 3)
                    #endif
                    
                    break;
                }
                else if (( pzm <= m_p[j]*pRM + q_p[j] ) && ( m_p[j]*pRM + q_p[j] <= pzM)
                        && ( sRm <= pRM ) && ( pRM <= sRM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 4)
                    #endif
                    
                    break;
                }
                else if ((pRM >= pzM/m_p[j]-q_p[j]/m_p[j])&&(pRm <= pzM/m_p[j]-q_p[j]/m_p[j])
                       && ( szm <= pzM ) && ( pzM <= szM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 5)
                    #endif

                    break;
                }
                else if ((pRM >= pzm/m_p[j]-q_p[j]/m_p[j])&&(pRm <= pzm/m_p[j]-q_p[j]/m_p[j])
                       && ( szm <= pzm ) && ( pzm <= szM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 6)
                    #endif

                    break;
                }
            }
            // m_p = infty
            if(Case_p[j] == 0){
                if (   ( szm <= pzm  ) && ( pzM <= szM  )
                    && ( pRm <= R_p[j] ) && ( R_p[j] <= pRM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 7)
                    #endif

                    break;
                }
            }
            // m_p = 0
            if(Case_p[j] == 1){
                if (   ( sRm < pRm   ) && ( pRM <= sRM  )
                    && ( pzm <= z_p[j] ) && ( z_p[j] <= pzM )){
                    BorderMask_p[i] = 1;

                    #ifdef _DBG_ON
                        PRINT_DEBUG(i, j, 8)
                    #endif

                    break;
                }
            }
        }
    }


}


/**********    GETTERS    **********/
int* CPPbsurface::GetBorderMask(){
    return BorderMask_p;
}
int* CPPbsurface::GetInsideMask(){
    return InsideMask_p;
}

