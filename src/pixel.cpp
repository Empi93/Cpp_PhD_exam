#include <iostream>
#include <cmath>
#include <vector>
#include "../include/pixel.h"
#include "../include/preprocessor_directives.h"

/**********    CTORS    **********/
pixel::pixel()
{
    coordinates_p[0][0] = 0.;
    coordinates_p[0][1] = 0.;
    coordinates_p[1][0] = 1.;
    coordinates_p[1][1] = 0.;
    coordinates_p[2][0] = 1.;
    coordinates_p[2][1] = 1.;
    coordinates_p[3][0] = 0.;
    coordinates_p[3][1] = 1.;

    RM_p=1.;
    Rm_p=0.;
    zM_p=1.;
    zm_p=0.;
}

pixel::pixel(float* R, float* z)
{
    for (int i=0; i<N_VERTICES; ++i){
        coordinates_p[i][0] = R[i];
        coordinates_p[i][1] = z[i];
    }
    FindMaxMinCoordinates();
}

pixel::pixel(float coordinates[4][2])
{
    for (int i=0; i<N_VERTICES; ++i){
        for (int j=0; j<N_COORDINATES; j++){
            std::cout << coordinates[i][j] << ' ';
            coordinates_p[i][j] = coordinates[i][j];
        }
        std::cout << std::endl;
    }
    FindMaxMinCoordinates();
}


/**********    DTOR    **********/
pixel::~pixel(){}  


/**********    OPERATOR    **********/
bool pixel::operator == (const pixel& PixelToCompare){
    if (    (Rm_p==PixelToCompare.Rm_p)
        &&  (RM_p==PixelToCompare.RM_p)
        &&  (zm_p==PixelToCompare.zm_p)
        &&  (zM_p==PixelToCompare.zM_p)
        )
        return true;
    else
        return false;
}


/**********    METHODS FOR CTORS    **********/
void pixel::FindMaxMinCoordinates(){
    // set value at choice
    RM_p = coordinates_p[0][0];     
    Rm_p = coordinates_p[0][0];     
    zM_p = coordinates_p[0][1];     
    zm_p = coordinates_p[0][1];			

    for (int i=0; i<N_VERTICES; i++){	
        if ( RM_p < coordinates_p[i][0] )     { RM_p = coordinates_p[i][0]; }
        if ( coordinates_p[i][0] < Rm_p )     { Rm_p = coordinates_p[i][0]; }

        if ( zM_p < coordinates_p[i][1] )     { zM_p = coordinates_p[i][1]; }
        if ( coordinates_p[i][1] < zm_p )     { zm_p = coordinates_p[i][1]; }	
    }
} 


/**********    SETTERS    **********/
void pixel::SetCoordinates(float coordinates[4][2]){
    for (int i=0; i<N_VERTICES; ++i){
        for (int j=0; j<N_COORDINATES; j++){
            coordinates_p[i][j] = coordinates[i][j];
        }
    }
    FindMaxMinCoordinates();
}


/**********    GETTERS    **********/
float pixel::GetRM() const{
    return RM_p;
}
float pixel::GetRm() const{
    return Rm_p;
}
float pixel::GetzM() const{
    return zM_p;
}
float pixel::Getzm() const{
    return zm_p;
}


/**********    PRINTERS    **********/
void pixel::Print() const
{
    PRINT_VERTEX(coordinates_p[3],coordinates_p[2])
    PRINT_VERTEX(coordinates_p[0],coordinates_p[1])
}

void pixel::PrintAll() const
{
    std::cout << "Coordinates:" << std::endl;
    PRINT_VERTEX(coordinates_p[3],coordinates_p[2])
    PRINT_VERTEX(coordinates_p[0],coordinates_p[1])
    std::cout << "R min: " << Rm_p << std::endl;
    std::cout << "R Max: " << RM_p << std::endl; 
    std::cout << "z min: " << zm_p << std::endl; 
    std::cout << "z Max: " << zM_p << std::endl;
}