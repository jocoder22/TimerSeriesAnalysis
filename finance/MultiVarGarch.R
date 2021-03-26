install.packages(c("PerformanceAnalytics", "quantmod", "rugarch", "car", "FinTS", "rmgarch" , "mgarch"))
install.packages("https://cran.r-project.org/src/contrib/Archive/rmgarch/rmgarch_1.3-6.tar.gz",  repos = NULL, type="source")
install.packages("RiskPortfolios")

# https://www.r-graph-gallery.com/

# loading required libraries
library(PerformanceAnalytics)
library(quantmod)
library(rugarch)
library(car)
library(FinTS)
library(rmgarch)
library(mgarch)
library(repr)
library(RiskPortfolios)

options(repr.plot.width=14, repr.plot.height=10)
options(digits=4)


# source("https://github.com/R-Finance/FactorAnalytics/blob/master/sandbox/R/covEWMA.R")
# source("https://rdrr.io/github/R-Finance/FactorAnalytics/src/sandbox/R/covEWMA.R")
source("https://r-forge.r-project.org/scm/viewvc.php/*checkout*/pkg/factorAnalytics/R/covEWMA.R?revision=14&root=factoranalytics&pathrev=14")


# download dataset
symbol2.vec = c("AMZN", "^GSPC")
getSymbols(symbol2.vec, from ="2000-01-03", to = "2012-04-03", auto.assign=F)
colnames(AMZN)
start(AMZN)
end(AMZN)

# Merge adjusted close prices and change colnames
alldata = merge(AMZN[, "AMZN.Adjusted", drop=F], GSPC[, "GSPC.Adjusted", drop=F])
colnames(alldata) = c("AMZN", "GSPC")

# plot adjusted close prices
plot(alldata$AMZN, main="Amazon Adjusted Close Price")
plot(alldata$GSPC, main="S&P500 Adjusted Close Price")

# calculate log-returns for GARCH analysis and drop na 
alldata.ret = CalculateReturns(alldata, method="log")[-1, ] # method="compound" is same as "log"

# plot the returns
plot(alldata.ret, col=c("white", "black"), main="Amazon-S&P500 Returns") # returns highly overlap
plot(alldata.ret$AMZN, main="Amazon Returns")
plot(alldata.ret$GSPC, main="S&P500 Returns")

# Add confidence 95% confidence interval lines
tt = rep(sd(alldata.ret$GSPC)*1.96, nrow(alldata.ret))
# plot(index(alldata.ret), alldata.ret$GSPC, type="l", panel.first = grid(10, lty = 1, lwd = 1), xlab="Time", ylab="S&P500 Returns")
# lines(index(alldata.ret), tt, type = "l", col = "red", lty = 4)
plot(index(alldata.ret), alldata.ret$GSPC, type="l", xlab="Time", ylab="S&P500 Returns")
grid(lty = 1, lwd = 1.5)
abline(h=sd(alldata.ret$GSPC)*1.96, col = "red")
abline(h=sd(alldata.ret$GSPC)*-1.96, col = "red")


# scatterplot of returns
plot(coredata(alldata.ret$GSPC), coredata(alldata.ret$AMZN), xlab="GSPC", ylab="AMZN",
      type="p", pch=16, lwd=2, col="blue")
grid(lty = 1, lwd = 1.5)
abline(h=0,v=0)


# compute rolling correlations
chart.RollingCorrelation(alldata.ret$GSPC, alldata.ret$AMZN, width=20)

cor.fun = function(x){
  cor(x)[1,2]
}

cov.fun = function(x){
  cov(x)[1,2]
}


roll.cov = rollapply(as.zoo(alldata.ret), FUN=cov.fun, width=20,
                     by.column=FALSE, align="right")
roll.cor = rollapply(as.zoo(alldata.ret), FUN=cor.fun, width=20,
                     by.column=FALSE, align="right")

roll.cov10 = rollapply(as.zoo(alldata.ret), FUN=cov.fun, width=10,
                     by.column=FALSE, align="right")
roll.cor10 = rollapply(as.zoo(alldata.ret), FUN=cor.fun, width=10,
                     by.column=FALSE, align="right")

# plot the 20 day rolling covariance and correlations
par(mfrow=c(2,1))
plot(roll.cov, main="20-day rolling covariances",
     ylab="covariance", lwd=2, col="blue")
grid(lty = 1, lwd = 1.5)
abline(h=cov(alldata.ret)[1,2], lwd=2, col="red")
plot(roll.cor, main="20-day rolling correlations",
     ylab="correlation", lwd=2, col="blue")
grid(lty = 1, lwd = 1.5)
abline(h=cor(alldata.ret)[1,2], lwd=2, col="red")
par(mfrow=c(1,1))

# plot the 10 day rolling covariance and correlations
par(mfrow=c(2,1))
plot(roll.cov10, main="10-day rolling covariances",
     ylab="covariance", lwd=2, col="blue")
grid(lty = 1, lwd = 1.5)
abline(h=cov(alldata.ret)[1,2], lwd=2, col="red")
plot(roll.cor10, main="10-day rolling correlations",
     ylab="correlation", lwd=2, col="blue")
grid(lty = 1, lwd = 1.5)
abline(h=cor(alldata.ret)[1,2], lwd=2, col="red")
par(mfrow=c(1,1))



# calculate EWMA covariances and correlations
lambda <- 0.94 # 0.94 is default
cov.ewma <- covEWMA(as.data.frame(MSFT.GSPC.ret), lambda=lambda)
cov.ewma = covEstimation(MSFT.GSPC.ret, control = list(type = 'ewma', lambda = lambda))
