install.packages("quantmod")
install.packages("rugarch")
library("quantmod")
library("rugarch")
fb <- getSymbols("FB", auto.assign=F)
head(fb)
chartSeries(fb)
fbClose <- fb$FB.Close
head(fbClose)

fb1 <- ugarchspec(variance.model=list(model="sGARCH", garchOrder=c(1,1)), mean.model=list(armaOrder=c(0,0)),
    distribution.model="std")
fbGarch1 <- ugarchfit(spec=fb1, data=fbClose)

fbGarch1
fbpredict <- ugarchboot(fbGarch1, n.ahead=10, method=c("Partial", "Full)[1])
plot(fbpredict,which=2,2)
