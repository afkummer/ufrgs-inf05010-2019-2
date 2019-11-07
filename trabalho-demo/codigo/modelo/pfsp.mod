#!/usr/bin/env glpsol 

# Conjunto das tarefas
set N;

# Conjunto das máquinas
set M;

# Conjunto do tempo de processamento das tarefas nas maquinas
param T {N cross M};

# Parametro big M
param P := 1e6;

# Variáveis do tempo de finalização das tarefas
var c {N cross M} >= 0;

# Variável do makespan
var Cmax >= 0;

# Variáveis da ordem de processamento.
var d { (i,k) in N cross N: i < k } binary;

minimize makespan: Cmax;

# Tempos de finalização na máquina 1
s.t. completionMach1 {i in N}:  c[i,1] >= T[i,1]; 

# Tempos de finalização nas demais máquinas
s.t. completionMachM {i in N, r in M: r >= 2}: c[i,r] - c[i,r-1] >= T[i,r];

# Primeira restrição da ordem de processamento
s.t. jobOrderA {i in N, k in N, r in M: k > i}: c[i,r] - c[k,r] + P*d[i,k] >= T[i,r];

# Segunda restrição da ordem de processamento
s.t. jobOrderB {i in N, k in N, r in M: k > i}: c[i,r] - c[k,r] + P*d[i,k] <= P - T[k,r];

# Restrição de cálculo do makespan.
s.t. MKSPAN {i in N}: Cmax >= c[i, max{m in M} m];

end;

