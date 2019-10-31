#!/usr/bin/env Rscript

options(width = 300)

library(dplyr)
library(ggplot2)
library(xtable)
library(reshape2)

res <- read.csv('grasp-hn3.csv')
inst <- unique(res$instancia)

# Gráficos boxplot para o GRASP com e sem LS vs alpha.
if (F) {
   for (i in inst) {
      tmp <- dplyr::filter(res, instancia == i)
      tmp$alpha <- as.factor(tmp$alpha)
      tmp <- melt(tmp, id.var='alpha', measure.vars=c('obj.grasp', 'obj.best'))
      plt <- ggplot(tmp, aes(x=alpha, y=value)) + 
         ggtitle(paste0('Instância ', i)) +
         geom_boxplot(aes(fill=variable)) +
         xlab(expression('Valor de ' * alpha)) +
         ylab('Função objetivo') + 
         scale_fill_discrete(name='Experimento', labels=c('GRASP', 'GRASP+LS'))
      ggsave(paste0('boxplot-', i, '.pdf'), plt, width=8, height=6)
      warnings()
   }
}

