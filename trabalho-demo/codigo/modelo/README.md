## Modelagem do PFSP com GLPK

Esse diretório contém o modelo matemático do problema FlowShop Permutacional
em linguagem MathProg. O modelo está descrito no arquivo [pfsp.mod](pfsp.mod),
enquanto o script [criaInstGlpk.py](criaInstGlpk.py) deve ser utilizado para 
converter as instâncias de teste para um formato que o GLPK entende. 

O script [roda-glpk.sh](roda-glpk.sh) pode ser utilizado para facilitar a 
interação com o solver. Esse script toma os seguintes passos:

- Chama o `criaInstGlpk.py` e converte a instância para um formato compatível
com o MathProg

- Chama o `glpsol`, informando os arquivos de modelo e de dados de entrada

O script `roda-glpk.sh` também define alguns parâmetros de execução do 
`glpsol`, a saber:

- `--tmlim 3600`: Limita o tempo de execução em 1 hora

- `--presol`: Ativa o preprocessamento do modelo

- `--mir`: Ativa as heurísticas de arredondamento para problemas inteiros

- `--bestp`: Utiliza a heurística de projeção para selecionar a próxima
variável que o _branch_ deve ser feito

Para uma descrição mais completa das opções aceitas pelo `glpsol`, consulte
a documentação do _solver_.

