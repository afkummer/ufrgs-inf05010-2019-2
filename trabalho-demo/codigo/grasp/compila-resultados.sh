#!/bin/bash

# Dá as boas-vindas.
echo "compila-resultados.sh: Consolida resultados da metaheurística"

# Testa se o script sabe onde estão os resultados individuais.
if [ $# -eq 0 ]; then
   echo "Preciso saber o diretório de resultados da metaheurística." 
   exit 1
fi

# Extrai comandos da linha de comandos.
TDIR=$1

if [ ! -d $TDIR ]; then
   echo "Diretório de experimentos $TDIR não existe."
   exit 1
fi

# Prepara o arquivo de saída geral.
echo "instancia,seed,alpha,tempo,obj.grasp,obj.best" > resultados.csv

# Faz o loop sobre os dados de saída.
for f in `ls -1 $TDIR/*`; do
   tail -n1 $f >> resultados.csv
done

# Dá mensagem de saída.
echo "Resultados reunidos em resultados.csv."


