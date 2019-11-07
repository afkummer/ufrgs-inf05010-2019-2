## Heurística GRASP com Busca Local para o PFSP

Esse diretório contém o código da implementação da heurística, bem como
alguns script auxiliares para execução dos testes sequencialmente, ou 
em paralelo. Descrição dos arquivos:

- `grasp-pfsp.py`: Implementa a heurística GRASP e a Busca Local

- `gera-batch.sh`: Gera um arquivo de textos (`batch-grasp.txt`) com as linhas
de execução da heurística para todas as instâncias de teste, considerando 
vários parâmetros de entrada distintos

- `roda-parallel.sh`: Roda várias instâncias simultâneas da heurística, 
considerando o arquivo `batch-grasp.txt`, utilizando o software GNU Parallel

- `compila-resultados.sh`: Consolida as saídas geradas com auxílio do GNU
Parallel em um arquivo CSV

- `faz-limpeza.sh`: Elimina arquivos temporários do diretório de trabalho

Os scripts estão relativamente bem comentados, sugiro a leitura do código 
fonte em caso de dúvidas. Informações sobre o experimento podem ser 
encontradas no [relatório do trabalho](../../../relatorio/).

