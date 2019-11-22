#!/usr/bin/env python

# Script para geração do grafo de conflitos para o problema Mirrored 
# Traveling Tournment Problem (mTTP), que é usado junto à formulação
# matemática do trabalho "New models for the Mirrored Traveling 
# Tournament Problem", de Carvalho e Lorena (2012).
#
# @author Alberto Francisco Kummer Neto
# @license CC BY-SA
#

# Grava o arquivo no formato que o Graphviz consegue renderizar.
# Para visualizar, usa um comando similar com:
# $ circo gc.dot -Tx11
def writeDotfile(matches, revMatches, adjMatrix):
   with open('gc.dot', 'wt') as fid:
      fid.write('graph {\n')
      fid.write('   ranksep=3;\n')
      fid.write('   ratio=auto;\n')
      for (i,j) in matches:
         for (a,b) in matches:
            row = revMatches[i][j]
            col = revMatches[a][b]
            if adjMat[row][col] == 1 and row < col:
               fid.write('   "(%d,%d)" -- "(%d,%d)"\n' % (i, j, a, b))
      fid.write('}\n')
   print('Arquivo para Graphviz (circo) salvo em: gc.dot.')

# Grava um arquivo com o grafo de conflitos.
def writeGc(matches, revMatches, adjMatrix):
   nzz = sum([sum(x) for x in adjMatrix])
   with open('gc.txt', 'wt') as fid:
      fid.write('%d %d\n' % (len(matches), nzz))
      for (i,j) in matches:
         fid.write('%d %d\n' % (i,j))
      for (i,j) in matches:
         for (a,b) in matches:
            row = revMatches[i][j]
            col = revMatches[a][b]
            if adjMat[row][col] == 1 and row < col:
               fid.write('%d %d\n' % (row, col))
   print('Grafo de conflitos salvo em: gc.txt.')

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

   print('=== Gerador de Grafos de Conflito ===') 

   # Carrega a instância do problema.
   n = -1 # Número de equipes
   d = [] # Distâncias entre as cidades
   with open(argv[1], 'rt') as fid:
      for line in fid:
         row = [float(x.strip()) for x in line.split()]
         d.append(row)
      n = len(d[0])
   print('Carregou instância: %s.' % basename(argv[1]))
   print('Conteúdo: %d equipes.' % n)
   
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
         if (i,j) == (a,b):  # Não existe conflito consigo mesmo.
            continue

         if i == a or i == b or j == a or j == b:
            # Adiciona conflito se duas tuplas distintas tem alguma 
            # equipe em comum.
            adjMat[revMatches[i][j]][revMatches[a][b]] = 1

   writeDotfile(matches, revMatches, adjMat)
   writeGc(matches, revMatches, adjMat)

