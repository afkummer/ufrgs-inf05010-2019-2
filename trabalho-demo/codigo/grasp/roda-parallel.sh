#!/bin/bash

# Dá as boas-vindas.
echo "roda-parallel.sh: Wrapper da metaheurística GRASP para o FlowShow"

# Testa se o parallel está instalado e disponível.
command -v parallel 2>&1 > /dev/null
if [ $? -ne 0 ]; then
   echo "O programa GNU parallel não está instalado neste computador."
   echo "O script precisa deste programa para continuar."
   exit 1
fi

# Script que roda os casos de teste do GRASP para o PFSP.
# O script é responsável, ele tenta verificar a consistência
# do ambiente de testes antes de continuar.
if [ $# -eq 0 ]; then
   echo "Preciso saber quantas threads estão disponíveis para teste."
   exit 1
fi

# Extrai comandos da linha de comandos.
THREADS=$1
INFILE="batch-grasp.txt"

# Testa se o arquivo de testes existe, e encerra o script em caso negativo.
if [ ! -f $INFILE ]; then
   echo "Arquivo batch '$INFILE' de experimentos não existe."
   echo "Para criar um, execute o script gera-batch.sh."
   exit 1
fi

# Dá algumas informações úteis sobre o experimento.
echo "Experimentos em paralelo: $THREADS experimentos"
TDIR="$(mktemp -d -p .)"
echo "Armazenando logs dos experimentos em $TDIR."
printf "Iniciando experimentos com GNU parallel...\n\n"

parallel -j $THREADS --shuf --eta --tmpdir=$TDIR --files < $INFILE

