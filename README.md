
# INF05010 - Otimização combinatória

Esse repositório contém o material complementar utilizado na edição de 2019/2 da disciplina INF05010. A apresentação dos problemas propostos pode ser encontrada [aqui](trab-opt-apresentacao.pdf).
Uma especificação mais detalhada do projeto final da disciplina está disponível [aqui](trab-opt.pdf). Outras informações podem ser encontradas na [Plataforma Moodle Inf](https://moodle.inf.ufrgs.br/course/view.php?id=255).

## Trabalho de otimização

### Mirrored Traveling Tournament Problem (mTTP)

As instâncias do mTTP são matrizes quadrada com as distâncias entre todos os pares de cidades do problema. O nome das instâncias inclui algum contexto de onde elas foram retiradas, bem como o número de equipes consideradas no problema. Os melhores valores de solução conhecidos (BKS) foram extraídos de [Santos e Carvalho (2018)](https://proceedings.science/sbpo/papers/algoritmo-genetico-aplicado-a-otimizacao-do-planejamento-de-torneios-esportivos) e uma formulação matemática do problema pode ser encontrada em [Carvalho e Lorena (2012)](https://www.sciencedirect.com/science/article/abs/pii/S0360835212001726).

| Instância | BKS    |
|-----------|-------:|
|[NL4](instancias/mttp/N4.txt)             | 8276   |
|[NL6](instancias/mttp/N6.txt)             | 26588  |
|[NL8](instancias/mttp/N8.txt)             | 41928  |
|[NL10](instancias/mttp/N10.txt)           | 63832  |
|[NL12](instancias/mttp/N12.txt)           | 119608 |
|[NL14](instancias/mttp/N14.txt)           | 199363 |
|[circ6](instancias/mttp/circ6.txt)        | 72     |
|[circ8](instancias/mttp/circ8.txt)        | 140    |
|[circ10](instancias/mttp/circ10.txt)      | 272    |
|[circ12](instancias/mttp/circ12.txt)      | 432    |

__Nota :__ As instâncias foram espelhadas da biblioteca [Challenge Traveling Tournament Instances](https://mat.gsia.cmu.edu/TOURN/).


### Maximally Diverse Grouping Problem (MDGP)

As instâncias do MDGP tem seu formato descrito [neste arquivo](instancias/mdgp/instance_format.txt), e são nomeadas conforme a convenção: `RanInt_n010_ss_10.txt`, `RanInt` indica o procedimento utilizado na geração dos pesos, `n010` indica o número de "individuos" do problema, `ss` indica que os grupos devem ter o mesmo número de indivíduos, e `10` indica _id_ da instância dentro da família de casos de teste. Os melhores valores de solução conhecidos (BKS) foram extraídos de [Araujo e Figueiredo. (2018)](https://proceedings.science/sbpo/papers/o-problema-da-diversidade-maxima-de-grupos%3A-uma-abordagem-de-programacao-linear-inteira). Esse mesmo trabalho apresenta uma formulação matemática para o problema.

| Instância | _n_ | Tamanho das equipes | BKS |
|-----------|----:|:-------------------:|----:|
|[RanInt_07](instancias/mdgp/RanInt_n010_ds_07.txt)   | 10  | ≠   | 1221.00     |
|[RanReal_10](instancias/mdgp/RanReal_n010_ss_10.txt)  | 10  | =   | 1195.92    |
|[RanInt_03](instancias/mdgp/RanInt_n012_ss_03.txt)   | 12  | =   | 993.00      |
|[Geo_10](instancias/mdgp/Geo_n010_ss_10.txt)      | 10  | =   | 3752.03        |
|[RanInt_10](instancias/mdgp/RanInt_n010_ss_10.txt)   | 10  | =   | 1112.00    |
|[RanInt_03](instancias/mdgp/RanInt_n060_ds_03.txt)   | 60  | ≠   | 17041      |
|[RanReal_04](instancias/mdgp/RanReal_n060_ss_04.txt)  | 60  | =   | 18050.80   |
|[RanInt_05](instancias/mdgp/RanInt_n030_ss_05.txt)   | 30  | =   | 5496.00    |
|[Geo_04](instancias/mdgp/Geo_n060_ss_04.txt)      | 60  | =   | 45971.80   |
|[Geo_08](instancias/mdgp/Geo_n030_ds_08.txt)      | 30  | ≠   |  13282.00  |


__Nota :__ Instâncias foram espelhadas da [MDGPLIB](http://grafo.etsii.urjc.es/index.php/category/maximally-diverse-grouping/).


### Home Health Care Routing and Scheduling Problem (HHCRSP)

O formato das instâncias está descrito [aqui](http://wcms.itz.uni-halle.de/download.php?down=38056&elem=2882667), e são nomeadas conforme a convenção: em `InstanzCPLEX_HCSRP_50_2.txt`, `50` indica o número de pacientes considerados no problema, e `2` indica o _id_ da instância dentro da família. Os limitantes superiores das instâncias de teste foram extraídos de [Neto et al. (2019)](neto-2019.pdf). Uma formulação matemática para o problema está disponível em [Mankowska et al. (2014)](https://link.springer.com/article/10.1007%2Fs10729-013-9243-1). __Atenção__: as restrições de sincronização das rotas (11) e (12) devem ser _desconsideradas_ no trabalho da disciplina!

| Instância | Limitante superior |
|-----------|-------------------:|
|[A3](instancias/hhcrsp/InstanzCPLEX_HCSRP_10_3.txt)  |   305.90   |
|[B3](instancias/hhcrsp/InstanzCPLEX_HCSRP_25_3.txt)  |   399.20   |
|[B9](instancias/hhcrsp/InstanzCPLEX_HCSRP_25_9.txt)  |   403.80   |
|[C1](instancias/hhcrsp/InstanzCPLEX_HCSRP_50_1.txt)  |  1006.72   |
|[C2](instancias/hhcrsp/InstanzCPLEX_HCSRP_50_2.txt)  |   597.06   |
|[C6](instancias/hhcrsp/InstanzCPLEX_HCSRP_50_6.txt)  |   852.04   |
|[D10](instancias/hhcrsp/InstanzCPLEX_HCSRP_75_10.txt) |  1306.60   |
|[E8](instancias/hhcrsp/InstanzVNS_HCSRP_100_8.txt)  |   832.73   |
|[F1](instancias/hhcrsp/InstanzVNS_HCSRP_200_1.txt)  |  1721.40   |
|[G9](instancias/hhcrsp/InstanzVNS_HCSRP_300_9.txt)  |  2415.50   |


__Nota :__ As instâncias foram espelhadas de [Benchmark instances for the home health care routing and scheduling problem](https://prodlog.wiwi.uni-halle.de/forschung/research_data/hhcrsp/). Adicionalmente, o formato das instâncias foi normalizado para o padrão utilizado em `InstanzCPLEX`. Caso se opte por usar as instâncias originais da Dorota Mankowska, atente que as `InstanzVNS` tem formato diferente!
