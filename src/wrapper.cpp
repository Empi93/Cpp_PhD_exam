#include <stdlib.h>
#include <stdio.h>
#include "../include/pixel.h"
#include "../include/image.h"
#include "../include/CPPbsurface.h"
#include "../include/preprocessor_directives.h"
#include "../include/wrapper.h"

struct bsurface {
	void *obj;
};

bsurface_t * bsurface_create(float* Rb, float* zb, float* m, float* q, 
                             float* Case, float coordinates[][4][2], 
                             const float Rm, const float RM, const float zm,
                             const float zM, const int lenB, const int dimR, 
                             const int dimz)
{
	bsurface_t *b;
	CPPbsurface *obj;

	b      = (typeof(b))malloc(sizeof(*b));
	printf("Fino a qui tutto bene, ora inizializzo l'oggetto\n");
	obj    = new CPPbsurface (Rb, zb, m, q, Case, coordinates, Rm, RM, zm, zM,
						   lenB, dimR, dimz);
	b->obj = obj;

	return b;
}

/*bsurface_t * test_types(float* Rb, float coordinates[][4][2], const int dimRb)   
{
	bsurface_t *b;
	CPPbsurface *obj;

	b      = (typeof(b))malloc(sizeof(*b));
	obj    = new CPPbsurface ();
	b->obj = obj;

	printf("%d\n", dimRb);
	for (int i=0; i<dimRb; ++i){
		printf("%f ", Rb[i]);
	}
	printf("\n");
	for (int i=0; i<dimRb; ++i){
		printf(" [ ");
		for (int j=0; j<4; ++j){
			printf(" [ ");
			for (int k=0; k<2; k++){
				printf("%f ", coordinates[i][j][k]);
			}
			printf("]\n");
		}
		printf("]\n");
	}

	return b;
}*/

void bsurface_destroy(bsurface_t *b)
{
	if (b == NULL)
		return;
	delete static_cast<CPPbsurface *>(b->obj);
	free(b);
}

int* GetBorderMask(bsurface_t *b)
{
	CPPbsurface *obj;

	if (b == NULL){
		int * error = new int[2];
		for (int i=0; i<2; ++i){
			error[i] = 0;
		}

		return error;
	}

	obj = static_cast<CPPbsurface *>(b->obj);
	return obj->GetBorderMask();
}
