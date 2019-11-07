#!/usr/bin/env python
#! -*- coding: utf-8 -*-

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


if __name__ == '__main__':
   # Testa os argumentos da linha de comando
   from sys import argv
   if len(argv) != 2:
      print('Utilização: %s <caminho até a instância>' % argv[0])
      exit(1)

   # Lê a instância
   instPath = argv[1]
   print('Processando instância "%s".' % instPath)
   inst = PfspInstance(instPath)

   # Grava o arquivo de instância para o GLPK
   with open('pfsp.dat', 'w') as fid:
      fid.write('#!/usr/bin/env glpsol\n\n')
      fid.write('# Instância original:\n')
      fid.write('# %s\n\n' % instPath)

      fid.write('# Conjunto das tarefas\n')
      fid.write('set N :=\n')
      for j in range(1, inst.numJobs+1):
         fid.write('   %d\n' % j)
      fid.write(';\n\n')

      fid.write('# Conjunto das máquinas\n')
      fid.write('set M :=\n')
      for r in range(1, inst.numMachines+1):
         fid.write('   %d\n' % r)
      fid.write(';\n\n')

      fid.write('# Tempos de processamento, [jobId, machineId]\n')
      fid.write('param T :=\n')
      for j in range(inst.numJobs):
         for r in range(inst.numMachines):
            fid.write('   %d %d %d\n' % (j+1, r+1, inst.procTimes[j][r]))
      fid.write(';\n\n')

      fid.write('end;\n\n')

   print('Instância escrita em "pfsp.dat".') 
