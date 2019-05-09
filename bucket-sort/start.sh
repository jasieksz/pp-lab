#!/bin/bash

mkdir results

size=10000000

echo "CPU,Bucket_CPU,Data_Gen,Init,Split,Sort,Merge,Total" >> results/alg2_e7

for proc in {1..4}
do
    for bucket in 1 2 4 6 8 12 15 20 25 30 35 45 60 80 100 150 200 500 1000 2500
    do
        ./prog2 $size $proc $bucket >> results/alg2_e7
    done
done

echo "CPU,Bucket_CPU,Data_Gen,Init,Split,Sort,Merge,Total" >> results/alg1_e7

for proc in {1..4}
do
    for bucket in 1 2 4 6 8 12 15 20 25 30 35 45 60 80 100 150 200 500 1000 2500
    do
      	./prog1 $size $proc $bucket >> results/alg1_e7
    done
done

