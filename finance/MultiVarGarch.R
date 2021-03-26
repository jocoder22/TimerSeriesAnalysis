install.packages(c("PerformanceAnalytics", "quantmod", "rugarch", "car", "FinTS", "rmgarch" , "mgarch"))
install.packages("https://cran.r-project.org/src/contrib/Archive/rmgarch/rmgarch_1.3-6.tar.gz",  repos = NULL, type="source")

# https://www.r-graph-gallery.com/

# loading required libraries
library(PerformanceAnalytics)
library(quantmod)
library(rugarch)
library(car)
library(FinTS)
library(rmgarch)
library(mgarch)
options(digits=4)


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
plot(alldata.ret, col=c("white", "black"), main="Amazon-S&P500 Returns")


