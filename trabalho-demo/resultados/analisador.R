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

generate.boxplots <- function() {
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

generate.tables <- function() {
   # Prepara a estrutura auxiliar para cálculo das médias e dos GAP para o BKS.
   tmp <- res %>% 
      dplyr::group_by(instancia,alpha) %>%
      dplyr::summarize(
         tempo.mean = mean(tempo),
         tempo.sd = sd(tempo),
         obj.grasp.mean = mean(obj.grasp),
         obj.grasp.sd = sd(obj.grasp),
         obj.best.mean = mean(obj.best),
         obj.best.sd = sd(obj.best)
      ) %>%
      dplyr::mutate(
         bks = unlist(bks.values[as.character(instancia)])
      ) %>%
      dplyr::mutate(
         bks.gap = round(100 * (obj.best.mean - bks)/(bks), 2)
      )

   # Gera a tabela de médias para todos os alphas.
   tmp2 <- tmp %>% dplyr::mutate(
      tempo = paste0('$', round(tempo.mean,1), ' \\pm ', round(tempo.sd, 2), '$'),
      fo = paste0('$', round(obj.best.mean, 1), ' \\pm ', round(obj.best.sd, 3), '$')
   ) %>%
   dplyr::select(
      instancia, bks, alpha, fo, bks.gap, tempo
   )
   tmp2$instancia <- sanitize(tmp2$instancia)
   colnames(tmp2) <- c('Instância', 'BKS', '$\\alpha$', 'Valor F.O.', 'GAP$_\\mathrm{BKS}$ (\\%)', 'Tempo (s.)')
   tmp2 <- xtable(tmp2)
   align(tmp2) <- c('l', 'l', 'r', 'r', 'r', 'r', 'r')
   sink('table-medias.tex')
   print(
      tmp2, 
      sanitize.colnames.function=as.is, 
      sanitize.text.function=as.is, 
      include.rownames=F,
      booktabs=T,
      hline.after=rep(6, nrow(tmp2)/6) * seq(1,nrow(tmp2)/6)
   )
   sink()
}

# generate.boxplots()
generate.tables()
