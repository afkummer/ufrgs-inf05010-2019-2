#!/bin/bash

# Remove resquícios de uma rodada anterior.
rm -f batch-grasp.txt

# Cria o arquivo com todas as execuções da entrada do GRASP.
for inst in `ls -1 -Sr ../instancias/*`; do
   for alpha in 0.0 0.2 0.4 0.6 0.8 1.0; do
      for seed in `seq 1 10`; do
         echo "./grasp-pfsp.py $inst $seed $alpha 1000000000 1000000000" >> batch-grasp.txt
      done
   done
done
