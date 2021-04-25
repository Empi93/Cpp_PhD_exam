#!/bin/bash
#chmod +rx tester.sh

gcc -o testC.out main.c test.c -lm
./testC.out 
