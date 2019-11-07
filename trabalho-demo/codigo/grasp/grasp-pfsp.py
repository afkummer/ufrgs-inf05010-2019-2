#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pprint
import time

pp = pprint.PrettyPrinter(3)

# Objeto que representa um caso de teste do problema.
class PfspInstance:
   def __init__(self, fname):
      from os import path
      self.name = path.splitext(path.basename(fname))[0]
      with open(fname, 'r') as fid:
         header = [int(i) for i in fid.readline().split()]
         self.numJobs = header[0]
         self.numMachines = header[1]
         self.procTimes = [] # Indexed as: [job id][machine id]
         for l in fid:
            tks = [int(i) for i in l.split()]
            row = []
            for i in range(len(tks)):
               if i % 2 != 0:
                  row.append(tks[i])
            self.procTimes.append(row)


# Faz a avaliação completa de uma solução do problema.
# Não utiliza cálculo incremental da função objetivo.
def fullEval(inst: PfspInstance, jobSeq, complSlots):
   complSlots[0][0] = inst.procTimes[jobSeq[0]][0]

   for j in range(1, inst.numJobs):
      complSlots[0][j] = complSlots[0][j-1] + inst.procTimes[jobSeq[j]][0]

   for r in range(1, inst.numMachines):
      complSlots[r][0] = complSlots[r-1][0] + inst.procTimes[jobSeq[0]][r]

   for j in range(1, inst.numJobs):
      job = jobSeq[j]
      for r in range(1, inst.numMachines):
         top = complSlots[r-1][j]
         left = complSlots[r][j-1]
         complSlots[r][j] = max(top, left) + inst.procTimes[jobSeq[j]][r]

   return complSlots[-1][len(jobSeq)-1]


# Implementa um método construtivo guloso randomizado (GRASP).
def greedyRandom(inst: PfspInstance, alpha: float = 0.1):
   from math import floor, ceil
   jobSeq = []
   complSlots = [] # Indexed as [machine id][slot id]
   for i in range(inst.numMachines):
      complSlots.append([0] * inst.numJobs)
   lastUsed = -1

   def computeCmax(jobId):
      curr = lastUsed + 1
      complSlots[0][curr] = inst.procTimes[jobId][0]
      if curr > 0:
         complSlots[0][curr] += complSlots[0][lastUsed]

      for r in range(1, inst.numMachines):
         top = complSlots[r-1][curr]
         left = 0
         if curr > 0:
            left = complSlots[r][lastUsed]
         complSlots[r][curr] = max(top, left) + inst.procTimes[jobId][r]

      return complSlots[-1][curr]

   pending = [i for i in range(inst.numJobs)]
   while len(pending) != 0:
      rcl = []
      for j in pending:
         rcl.append((j, computeCmax(j)))

      sorted(rcl, key=lambda x: x[1])
      chosen = rcl[random.randint(0, floor((len(rcl)-1) * alpha))][0]

      pending.remove(chosen)
      jobSeq.append(chosen)
      computeCmax(chosen)
      lastUsed += 1

   return jobSeq, complSlots


# Ponto de entrada da aplicação.
# Argumentos: 
# - Caminho da instância
# - Semente de aleatoriedade
# - Valor de alpha
# - Número máximo de iterações sem melhora
# - Máximo de iterações global (-1 = infinito)
if __name__ == '__main__':
   from sys import argv
   from math import ceil
   print(' '.join(argv))
   if len(argv) != 6:
      print('Utilização: %s <caminho instância> <semente> <alpha> <max iter sem melhora> <max iter>' % argv[0])
      exit(1)

   # Separa os comandos de invocação do programa.
   instPath = argv[1]
   seed = int(argv[2])
   alpha = float(argv[3])
   maxIterWoImpr = int(argv[4])
   maxIter = int(argv[5])

   # Prepara os dados iniciais da aplicação.
   random.seed(seed)
   inst = PfspInstance(instPath)

   # Cria a solução inicial com GRASP.
   jobSeq, complSlots = greedyRandom(inst, alpha)
   bestObj = fullEval(inst, jobSeq, complSlots)
   graspObj = bestObj
   
   # Variáveis de controle do critério de parada
   iterLastImpr = 0  # Iterações sem melhora 
   iterCnt = 0       # Total de iterações

   # Registra o tempo de início do solver.
   time0 = time.time()

   # Loop principal.
   while iterCnt - iterLastImpr < maxIterWoImpr and iterCnt <= maxIter:
      doPrint = False

      # Função auxiliar que testa se o swap das tarefas de dois slots
      # leva a uma solução de melhor valor de f.o. A função seleciona
      # tarefas aleatoriamente, e faz sucessivas tentativas de troca
      # em busca de soluções melhores.
      def apply2swap(times):
         global inst, jobSeq, complSlots, iterLastImpr, bestObj, doPrint
         for i in range(times):
            # Escolhe duas tarefas aleatórias distintas.
            j1 = random.randint(0, inst.numJobs-1)
            j2 = random.randint(0, inst.numJobs-1)
            while j1 == j2:
               j2 = random.randint(0, inst.numJobs-1)

            # Faz a troca e avalia se a mudança vale a pena.
            jobSeq[j1], jobSeq[j2] = jobSeq[j2], jobSeq[j1]
            obj = fullEval(inst, jobSeq, complSlots)

            if obj < bestObj:
               # Aceita uma solução melhorada.
               bestObj = obj
               iterLastImpr = iterCnt
               doPrint = True
               return True
            else:
               # Não aceita piora, então reverte a troca e atualiza a
               # solução novamente.
               jobSeq[j1], jobSeq[j2] = jobSeq[j2], jobSeq[j1]
               obj = fullEval(inst, jobSeq, complSlots)
               return False
         
      # Troca 2RandomSwap repetida de acordo com o número de tarefas.
      jobsSwapCrit = ceil(inst.numJobs/100)
      apply2swap(jobsSwapCrit)
      
      # Troca 2RandomSwap repetida de acordo com o número de iterações.
      iterSwapCrit = ceil(inst.numJobs/1000)
      apply2swap(iterSwapCrit)

      # Troca 2RandomSwap repetida por um número aleatório de vezes.
      rndSwapCrit = random.randint(0, inst.numJobs-1)
      apply2swap(rndSwapCrit)

      # Imprime mensagem de progresso a cada 50 iterações, ou quando faz melhora.
      doPrint = doPrint or iterCnt % 50 == 0
      if doPrint:
         print('Iteração: %d   Iter. última melhora: %d   Valor obj: %f   Tempo: %f s.' % (iterCnt, iterLastImpr, bestObj, time.time() - time0))

      iterCnt += 1

   # Calcula o tempo total de execução da busca.
   time1 = time.time()
   elapsed = time1 - time0

   # Faz um último print, para o output ser preciso com o trabalho 
   # feito pela heurística. De outra forma, é possível que pelo menos
   # 50 iterações finais não sejam reportadas!
   print('Iteração: %d   Iter. última melhora: %d   Valor obj: %f   Tempo: %f s.' % (iterCnt, iterLastImpr, bestObj, time.time() - time0))

   # Escreve o resultado da execução no stdout.
   print(bestObj)
   print('%s,%d,%f,%f,%d,%d' % (instPath, seed, alpha, elapsed, graspObj, bestObj))

