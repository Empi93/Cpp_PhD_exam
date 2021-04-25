g++ -c -fPIC -o ./bin/pixel.o ./src/CPPYY/pixel.cc
gcc -shared -o ./bin/pixel.so ./bin/pixel.o