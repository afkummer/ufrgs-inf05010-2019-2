#!/usr/bin/env Rscript

options(width = 300)

library(dplyr)
library(ggplot2)
library(xtable)
library(reshape2)

bks.values <- list(
   'VFR10_15_1' = 1307,
   'VFR20_10_3' = 1592,
   'VFR20_20_1' = 2270,
   'VFR60_5_10' = 3663,
   'VFR60_10_3' = 3423,
   'VFR100_60_1' = 9395,
   'VFR500_40_1' = 28548,
   'VFR500_60_3' = 31125,
   'VFR600_20_1' = 31433,
   'VFR700_20_10' = 36417
)

res <- read.csv('grasp-hn3.csv')
inst <- unique(res$instancia)

create.blocks <- function() {
   # Cria a tabela com resultados sem busca local.
   tmp <- res %>%
      select(-obj.best) %>%
      mutate(meth = paste0('grasp_', alpha))
   colnames(tmp)[5] <- 'obj.value'

   # Agora cria a outra tabela só com o GRASP+BL.
   tmp2 <- res %>%
      select(-obj.grasp) %>%
      mutate(meth = paste0('grasp_bl_', alpha))
   colnames(tmp2)[5] <- 'obj.value'

   # Junta tudo em um dataframe só.
   tmp3 <- bind_rows(tmp, tmp2)

   # Aplica o teste para cada repetição.
   # for (r in unique(res$seed)) {
   #    aux <- tmp3 %>% dplyr::filter(seed == r)
   #    
   #    cat('\nTestes estatísticos da repetição #', r)
   #    tbl <- friedman.test(aux$obj.value, aux$meth, aux$instancia)
   #    print(tbl)

   #    tbl <- pairwise.wilcox.test(aux$obj.value, aux$meth, p.adj = 'bonf', paired=T)
   #    print(tbl)
   # }

   # Faz os testes para a média de execuções.
   aux <- tmp3 %>% 
      group_by(instancia,meth) %>%
      summarize(obj.mean = mean(obj.value))

   cat('\nTestes estatísticos para a média das execuções:\n')
   tbl <- friedman.test(aux$obj.mean, aux$meth, aux$instancia)
   print(tbl)

   tbl <- pairwise.wilcox.test(aux$obj.mean, aux$meth, p.adj = 'bonf', paired=T, alt='t')
   print(tbl)

   invisible()
}

create.blocks()

