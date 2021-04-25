# Intro
The present folder shows two ways of using a C++ library in Python. 

The example presented here is a module of a Python library designed for performin tomography and unfolding of gamma-rays spectroscopic measurements in tokomaks. The C++ module is responsible for the generation of a pixel mask from a geometric description of a B-field line. 

The reason for developing a C/C++ module comes from the fact that the first Python implementation was extremely slow and a C module helped improving speed by 2 order of magnitudes on some computers. A more precise comparison between various impelemntation (Python, C, C++ and NumPy vectorization) will be presented during the exam. 

In the present folder the original C module has been expanded in object oriented C++, which has been binded to a Python script using CPPYY or CFFI.  

## CPPYY
This is a wrapper designed at CERN that allows to bind C++ code into Python. ./UtilityTest contains some examples of argument passing between Python and C++ as well as the correct way to return an array from C++ to Python. 

In principle this is all we need to implement a Python wrapper for C++ using CPPYY. However the difficulties encountered in variable conversion from Python/NumPy to C++ suggested to use CFFI for the final implementation.

The utility test is here included for reference. 

## CFFI
CFFI offers an easier variables conversion API. For this reason the C++ class has been wrapped in a C library that is binded in the Python script using CFFI. 

The class has been implemented in src: wrapper.cpp wrapps the class implemented in CPPbsurface.cpp. This latter is derived from image.cpp, which contains a vector of pixel.cpp. 

The headers are in include/, togheter with a header containing all the precompiler directive necessary to compile the code correctly.

The source code is compiled in the library: bin/libBsurface.so and is called in the python script in function PixelsCpp contained in:
UtilityTest/Application/surface.py 

UtilityTest/ finally contains also some varibale conversion tests.

## Run the project
* Follow the following guides to install CFFI and CPPYY:
    https://cppyy.readthedocs.io/en/latest/installation.html
    https://cffi.readthedocs.io/en/latest/installation.html
  I used the conda install.

* To use the class, compile it using the bash script:
    CFFI_installer.sh

  Then move to UtilityTest/Application and run CFFI_test_case.py

* To test the variable conversion go to UtilityTest/VariableConversion and run:
    cffi_variables_conversion_ut.py
    cppyy_variables_conversion_ut.py