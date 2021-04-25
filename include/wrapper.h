#ifndef __WRAPPER_H__
#define __WRAPPER_H__

#ifdef __cplusplus
extern "C" {
#endif

struct bsurface;
typedef struct bsurface bsurface_t;

bsurface_t * bsurface_create(float* Rb, float* zb, float* m, float* q, 
                             float* Case, float coordinates[][4][2], 
                             const float Rm, const float RM, const float zm,
                             const float zM, const int lenB, const int dimR, 
                             const int dimz);
//bsurface_t * test_types(float* Rb, float coordinates[][4][2], const int dimRb);                        
void bsurface_destroy(bsurface_t *m);

int* GetBorderMask(bsurface_t *b);

#ifdef __cplusplus
}
#endif

#endif /* __WRAPPER_H__ */
