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
getSymbols(symbol2.vec, from ="2000-01-03", to = "2012-04-03")
colnames(AMZN)
start(AMZN)
end(AMZN)
