#library(tictoc)
#tic()
mstrap = NULL
cstrap = NULL
for (i in 1:75) {
  raw = Five[sample(1:dim(Five)[1], dim(Five)[1], replace=T),]
  
  buff = lmer(RT ~ I(-1*Bigram) + I(-1*Bigram2) + I(-1*Bigram3) + I(-1*Bigram4) + I(-1*Bigram5) + 
                Unigram + Unigram2 + Unigram3 + Unigram4 + Unigram5 +
                I(scale(Length)) + Position + (1|SubjNo) + (1|Story), 
              data=raw)
  
  fitcoef = as.vector(coef(buff)$Story[1,2:6])
  
  buffer = function(R, m=raw, NWORDS=5, data=fitcoef) {
    D = NA
    residualInfo = NULL
    for(i in 1:nrow(m)) {
      procbuf <- rep(NA, NWORDS) # how many bits are left after processing
      info <- -1*c(m$Bigram[i], m$Bigram2[i], m$Bigram3[i], m$Bigram4[i], m$Bigram5[i])
      info[is.na(info)] = rep(9, length(info[is.na(info)]))
      for(pos in 1:NWORDS) {
        procbuf[pos] <- info[pos]
        
        # and remove
        remaining <- R
        ri <- 1
        while(remaining > 0 & ri <= pos) {
          if(procbuf[ri] > remaining) { 
            procbuf[ri] <- procbuf[ri] - remaining 
            break
          }
          else {
            remaining <- remaining - procbuf[ri]
            procbuf[ri] <- 0
            ri <- ri+1
          }
        }
      }
      D = rbind(D, data.frame(w1=info[1], w2=info[2], w3=info[3], w4=info[4], w5=info[5], rt=147*sum(procbuf)/R))
    }
    l <- lm(rt ~ -1 + w1 + w2 + w3 + w4 + w5, data=D)
    sum((coef(l)-data)**2)
  }
  
  buffer.pred = function(R, m=raw, NWORDS=5, data=fitcoef) {
    D = NA
    residualInfo = NULL
    for(i in 1:nrow(m)) {
      procbuf <- rep(NA, NWORDS) # how many bits are left after processing
      info <- -1*c(m$Bigram[i], m$Bigram2[i], m$Bigram3[i], m$Bigram4[i], m$Bigram5[i])
      info[is.na(info)] = rep(9, length(info[is.na(info)]))
      for(pos in 1:NWORDS) {
        procbuf[pos] <- info[pos]
        
        # and remove
        remaining <- R
        ri <- 1
        while(remaining > 0 & ri <= pos) {
          if(procbuf[ri] > remaining) { 
            procbuf[ri] <- procbuf[ri] - remaining 
            break
          }
          else {
            remaining <- remaining - procbuf[ri]
            procbuf[ri] <- 0
            ri <- ri+1
          }
        }
      }
      D = rbind(D, data.frame(w1=info[1], w2=info[2], w3=info[3], w4=info[4], w5=info[5], rt=147*sum(procbuf)/R))
    }
    l <- lm(rt ~ -1 + w1 + w2 + w3 + w4 + w5, data=D)
    coef(l)
  }
  
  o = optim(c(9), buffer, method='L-BFGS-B', lower=c(0))
  
  mstrap = rbind(mstrap, o$par)
  cstrap = rbind(cstrap, buffer.pred(o$par))
}
#toc()

save(cstrap, file='cstrap.RData')
save(mstrap, file='mstrap.RData')
