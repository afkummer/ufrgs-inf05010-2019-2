#!/bin/bash

if [ $# -ne 1 ]; then
   echo "Preciso do caminho de uma instância para continuar."
   exit 1
fi

# Parâmetros de execução do GLPK
inst=$1
tmlim=3600
extraArgs='--presol --bestp --mir'

# Mensagem de boas vindas
echo "== PFSP solver com GLPSOL =="
echo "-- Instância:" $inst
echo "-- Tempo limite:" $tmlim "segundos"
echo "-- Argumentos extra:" $extraArgs

# Converte a instância
printf "\nConvertendo instância para formato do GLPK... "
./criaInstGlpk.py $inst 2>&1 > /dev/null
if [ $? -ne 0 ]; then
   echo "Falhou!"
   echo "Abortando execução do script."
   exit 1
fi
echo "Ok!"

echo "Iniciando GLPSOL."
echo $inst > glpk.log
glpsol -m pfsp.mod -d pfsp.dat --tmlim $tmlim $extraArgs -o pfsp.sol | tee -a glpk.log

if [ $? -ne 0 ]; then
   echo "GLPSOL falhou!"
   echo "Abortando execução do script."
   rm -f pfsp.dat
   exit 1
fi

printf "\nScript finalizado.\nSolução escrita em pfsp.sol.\n"
rm -f pfsp.dat

