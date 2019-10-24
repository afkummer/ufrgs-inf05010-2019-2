#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pprint
import time

pp = pprint.PrettyPrinter(3)

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


def randomPoolInitialSolution(inst: PfspInstance, alpha: float = 0.1):
   from math import floor
   tmp = []
   complSlots = [[0 for j in range(inst.numJobs)] for r in range(inst.numMachines)]
   
   for cand in range(300):
      s = [i for i in range(inst.numJobs)]
      random.shuffle(s)
      cmax = fullEval(inst, s, complSlots)
      tmp.append((s, cmax))
   
   sorted(tmp, key=lambda x: x[1])
   pos = random.randint(0, floor(len(tmp)*alpha))
   fullEval(inst, tmp[pos][0], complSlots)

   return tmp[pos][0], complSlots


if __name__ == '__main__':
   from sys import argv
   from math import ceil
   if len(argv) != 9:
      print('Wrong number of args: %d' % len(argv))
      pp.pprint(argv)
      print('Usage: %s <instance file> <seed> <alpha> <first ls> <second ls> <third ls> <max iter w/o impr> <RCL strategy>' % argv[0])
      exit(1)

   pp.pprint(argv)
   print('Executable:', argv[0])
   print('Instance:', argv[1])
   print('Seed:', argv[2])
   print('Alpha:', argv[3])
   print('LS1:', argv[4])
   print('LS2:', argv[5])
   print('LS3:', argv[6])
   print('Max iter w/o improvement:', argv[7])
   print('RCL strategy:', argv[8])

   random.seed(int(argv[2]))
   inst = PfspInstance(argv[1])

   alpha = float(argv[3])
   idLs1 = int(argv[4])
   idLs2 = int(argv[5])
   idLs3 = int(argv[6])
   maxIterWoImpr = int(argv[7])
   rclStrat = int(argv[8])

   lsNames = ['numJobs', 'numIter', 'numRand', 'none']
   print('Order of evaluation of local search procedures: [ ', end='')
   print(lsNames[idLs1], lsNames[idLs2], lsNames[idLs3], ']')

   print('Initial solution strategy: ', end='')
   if rclStrat == 0:
      print('greedyRandom')
      jobSeq, complSlots = greedyRandom(inst, alpha)
   elif rclStrat == 1:
      print('randomPoolInitialSolution')
      jobSeq, complSlots = randomPoolInitialSolution(inst, alpha)
   else:
      print('Unknown strategy to select initial solution: %d' % rclStrat)
      exit(1)

   bestObj = float('inf') # Current best obj
   iterLastImpr = 0       # Iterations w/o improvement
   iterCnt = 0            # Iteration counter

   
   time0 = time.time()
   while iterCnt - iterLastImpr < maxIterWoImpr and iterCnt <= 2450:
      doPrint = iterCnt % 50 == 0

      def apply2swap(times):
         global inst, jobSeq, complSlots, iterLastImpr, bestObj
         for i in range(times):
            # Choose two random jobs
            j1 = random.randint(0, inst.numJobs-1)
            j2 = random.randint(0, inst.numJobs-1)
            while j1 == j2:
               j2 = random.randint(0, inst.numJobs-1)

            # Apply the movement and check the cost of new solution
            jobSeq[j1], jobSeq[j2] = jobSeq[j2], jobSeq[j1]
            obj = fullEval(inst, jobSeq, complSlots)

            if obj < bestObj:
               # If the solution improved, update best obj value
               # and refresh iterator of last impr iter
               bestObj = obj
               iterLastImpr = iterCnt
               doPrint = True
               return True
            else:
               # Otherwise, revert the swap
               jobSeq[j1], jobSeq[j2] = jobSeq[j2], jobSeq[j1]
               obj = fullEval(inst, jobSeq, complSlots)
               return False
         
      def applyLs(lsId):
         if lsId == 0:
            # Repeated 2RandomSwap according the number of tasks
            jobsSwapCrit = ceil(inst.numJobs/100)
            apply2swap(jobsSwapCrit)
         elif lsId == 1:
            # Repeated 2RandomSwap according iteration criteria
            iterSwapCrit = ceil(inst.numJobs/1000)
            apply2swap(iterSwapCrit)
         elif lsId == 2:
            # Pure random criteria
            rndSwapCrit = random.randint(0, inst.numJobs-1)
            apply2swap(rndSwapCrit)
         elif lsId == -1:
            # Skip this pass of local search procedure
            pass
         else:
            print('Invalid local search identifier: %d' % lsId)
            exit(1)

      applyLs(idLs1)
      applyLs(idLs2)
      applyLs(idLs3)

      if doPrint:
         print('Iteration: %d   Last improvement: %d   Best obj: %f' % (iterCnt, iterLastImpr, bestObj))

      iterCnt += 1

   time1 = time.time()
   elapsed = time1 - time0

   print('Best solution found with cost: %f' % bestObj)
   print(bestObj)
   ## print('Job sequence: ')
   ## pp.pprint(jobSeq)
   #print('Success movements based on swap criteria: ')
   #pp.pprint(critSuccessCnt)

   from sys import stdout
   fid = stdout
   print()
   if True:
   # with open('results.csv', 'a+') as fid:
      # if fid.tell() == 0:
      #    fid.write('instance,')
      #    fid.write('rep,')
      #    fid.write('alpha,')
      #    fid.write('time,')
      #    fid.write('bestObj\n')
      fid.write('%s,' % argv[1])
      fid.write('%s,' % argv[2])
      fid.write('%f,' % alpha)
      fid.write('%f,' % elapsed)
      fid.write('%f,' % bestObj)
      fid.write('\n')
