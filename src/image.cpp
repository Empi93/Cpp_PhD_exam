#include <iostream>
#include <vector>
#include "../include/pixel.h"
#include "../include/image.h"
#include "../include/preprocessor_directives.h"

/**********    CTORS    **********/
image::image () :
    RM_p    (0.),
    Rm_p    (0.),
    zM_p    (0.),
    zm_p    (0.),
    dimR_p  (0) ,
    dimz_p  (0) {}

image::image (  float coordinates[][4][2], float Rm, float RM, 
                float zm, float zM, int dimR, int dimz ) :
    RM_p    (RM)    ,
    Rm_p    (Rm)    ,
    zM_p    (zM)    ,
    zm_p    (zm)    ,
    dimR_p  (dimR)  ,
    dimz_p  (dimz)
    {
    int Npixels = dimR*dimz;
    pixel temp;
    bool unique = true;
    bool inside = true;
    for (int i=0; i<Npixels; ++i){
        for (int j=0; j<N_VERTICES; ++j){
            if   ((coordinates[i][j][0] < Rm)
               || (RM < coordinates[i][j][1])
               || (coordinates[i][j][1] < zm)
               || (zM < coordinates[i][j][1])){
                    inside = false;
                }
        }
        temp.SetCoordinates(coordinates[i]);
        for (int j=0; j<i; j++){
            if (pixels[j]==temp){
                unique = false;
            }
        }
        if (unique&&inside){
            pixels.push_back(temp);
        }
    }
}


/**********    DTOR    **********/
image::~image () {
    pixels.~vector();
}


/**********    GETTERS    **********/
float image::GetPixelRM (int i) const {
    return pixels[i].GetRM();
}
float image::GetPixelRm (int i) const {
    return pixels[i].GetRm();
}
float image::GetPixelzM (int i) const {
    return pixels[i].GetzM();
}
float image::GetPixelzm (int i) const {
    return pixels[i].Getzm();
}
