#!/bin/bash
cd  `dirname "$0"`
cd ..
for var in 1 2 3 4 5 6 7 8 9 10
    do
#        echo "ahoj" > ./logs/ahoj.log
        stdbuf -oL python test_runner.py > ./logs/test_result${var}.log 2>./logs/test_result${var}.err
    done
