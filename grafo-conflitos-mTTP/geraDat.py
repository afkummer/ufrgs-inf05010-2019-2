#!/usr/bin/env python

# Utilidades para print decente com python.
import pprint
pp = pprint.PrettyPrinter(indent=3)

# Ponto de entrada do programa.
# Argumentos:
# 0: Nome do script python (automático)
# 1: Caminho até a instância do problema.
if __name__ == '__main__':
   from sys import argv
   from os.path import basename
   if len(argv) != 2:
      print('Utilização: %s <instância do mTTP>' % argv[0])
      exit(1)

   print('=== Conversor txt -> dat ===') 

   # Carrega a instância do problema.
   n = -1 # Número de equipes
   d = [] # Distâncias entre as cidades
   with open(argv[1], 'rt') as fid:
      for line in fid:
         row = [float(x.strip()) for x in line.split()]
         d.append(row)
      n = len(d[0])
   print('Carregou instância: %s.' % basename(argv[1]))
   print('Número de equipes: %d.' % n)
   
   # Cria as tuplas das equipes.
   matches = []  # Lista linear dos confrontos
   revMatches = [[-1] * (n) for i in range(n)]  # Matriz reversa dos confrontos
   for i in range(n):
      for j in range(n):
         if i < j:
            matches.append((i,j))
            revMatches[i][j] = len(matches)-1
            matches.append((j,i))
            revMatches[j][i] = len(matches)-1
   print('Quantidade de vértices do GC: %d.' % len(matches))
      
   # Cria uma matriz de adjacências para representar o grafo 
   # de conflitos das rodadas.
   adjMat = [([0] * len(matches)) for i in range(len(matches))]

   # Adiciona os conflitos das equipes em mais de uma partida
   # ao mesmo tempo. Isso é o grafo de conflitos!
   for (i,j) in matches:
      for (a,b) in matches:
         if (i,j) == (a,b):
            continue
         if i == a or i == b or j == a or j == b:
            # Adiciona conflito se duas tuplas distintas tem alguma 
            # equipe em comum.
            adjMat[revMatches[i][j]][revMatches[a][b]] = 1

   # Escreve alguma informação de depuração na saída do programa.
   print("Partidas:")
   pp.pprint(matches)

   print("Matriz de conflitos:")
   pp.pprint(adjMat)

   # Cria o arquivo dat.
   # Faz as adaptações necessárias para que as indexações iniciem em 1.
   with open('mttp.dat', 'wt') as fid:
      fid.write("# mTTP instance file for %s.\n\ndata;\n\n" % argv[1])

      fid.write("param n := %d;\n\n" % n)
      fid.write("param p := %d;\n\n" % (n-1))
      fid.write("param m := %d;\n\n" % len(matches))

      fid.write("set E :=\n")
      for i in range(len(matches)):
         for j in range(len(matches)):
            if (adjMat[i][j] != 0):
               fid.write("   %d %d\n" % (i+1, j+1))
      fid.write(";\n\n")

      fid.write("param g :=\n")
      for m in matches:
         fid.write("   %d %d\n" % (matches.index(m)+1, d[m[0]][m[1]]))
      fid.write(";\n\n")

      fid.write("param d :=\n")
      for i in range(len(matches)):
         for k in range(len(matches)):
            if adjMat[i][k] == 0:
               continue
            m1 = matches[i]
            m2 = matches[k]
            fid.write('   %d %d %d\n' % (i+1, k+1, d[m1[0]][m2[1]]))
      fid.write(";\n\n")




      fid.write("end;\n")
