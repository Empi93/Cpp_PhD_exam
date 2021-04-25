import cppyy
import numpy as np
from array import array

# Load the library
cppyy.include('../include/pixel.h')
cppyy.load_library('../bin/pixel.so')
# The library lives in cppyy.gbl

###########################    FROM PYTHON TO C    ############################
##########    1D ARRAY    ##########
## python list - must use vector 
print("\n1D    python list")                                          
cppyy.cppdef("""
    void test_1D(const std::vector<int>& array) {
        for (int i=0; i<array.size(); i++) {
                std::cout << array[i] << " ";
        }
        std::cout << std::endl;
    }
""")

var = np.array([1, 2, 3, 4]).tolist()
cppyy.gbl.test_1D(var)

## array.array()
print("\n1D    array.array()")
R = array('f',[1., 3., 5., 8.])
z = array('f',[2., 3., 5., 7.])
o1 = cppyy.gbl.pixel(R,z)
o1.Print()

## np.array()
## dtype must be explicitly defined to match C types
print("\n1D    np.array()")
R = np.array([1., 3., 5., 8.], dtype=np.float32)    # float64 not suported
z = np.array([2., 3., 5., 7.], dtype=np.float32)
o2 = cppyy.gbl.pixel(R,z)
o2.Print()

##########    2D ARRAY    ##########

## np.array()                                                   [DOES NOT WORK]
#print("2D    np.array()")
### The C module access only first sub-array correctly
#R = np.array([[1.,2.], [3.,3.], [5.,5.], [8.,7.]], dtype=np.float32, order='C')
#o4 = cppyy.gbl.pixel(R)
#o4.Print()

## python list - must use vector 
print("\n2D   python list with vector on C side")                                                
cppyy.cppdef("""
    void test_2D(const std::vector<std::vector<double>>& array) {
        for (int i=0; i<array.size(); i++) {
            for (int j=0; j<array[i].size(); j++) {
                std::cout << array[i][j] << " ";
            }
            std::cout << std::endl;
        }
    }
""")

#var = np.array([[1, 2], [3, 4]]).tolist()          # np.array not accepted
#cppyy.gbl.test_2D(var)

# it works only if C expects a vector of double and python uses np.float32
var = np.array([[1., 2.], [3., 4.]], dtype=np.float32).tolist() 
cppyy.gbl.test_2D(var)
#cppyy.gbl.test(var)


###########################    FROM C TO PYTHON    ############################
##########    1D ARRAY    ##########
# it works with dynamically declared arrays only!!!
print("\n\nHow to return variables to Python")
cppyy.cppdef("""
float* create_float_array(int sz) {
    //float* pf = (float*)malloc(sizeof(float)*sz);
    float* pf = new float[sz];
    for (int i = 0; i < sz; ++i) pf[i] = 2*i;
    return pf;
}""")
NDATA = 8
arr = cppyy.gbl.create_float_array(NDATA)
print(arr)
arr.reshape((NDATA,))   # adjust the llv's size
v = np.frombuffer(arr, dtype=np.float32, count=NDATA)  # cast to float
# frombuffer supports only 1D array
print(len(v))
print(v)



