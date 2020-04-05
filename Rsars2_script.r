#Required libraries
library(RCurl)
library(ggplot2)
library(reshape)

#URL with data
url <- getURL('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
data <- read.csv(text = url,header=F)

#Reshape
#First date is 22 Jan 2020
dates<-as.Date(as.vector(as.matrix(data[1,5:length(data)])), format='%m/%d/%Y')
names(data) <- c('ps','cr','lat','lon',paste('d',1:length(dates),sep=''))  

#Melt and order
datam<-melt(data[-c(1),-c(1,3,4)],id.vars='cr',measure.vars=paste('d',1:length(dates),sep=''))
levels(datam$variable) <- dates
datam$value <- as.numeric(as.character(datam$value))
datamagg <- aggregate(value~cr+variable, datam,'sum')
datamagg$variable<-as.Date(datamagg$variable)
datamagg<-datamagg[order(datamagg$value),]
datamagg$cr <- as.factor(datamagg$cr)
datamagg$cr<-droplevels(datamagg$cr)

#Derive total number of cases for ordering plots
sumcases <- aggregate(value~cr, datamagg[which(as.Date(datamagg$variable)==format(Sys.time(), '%y-%m-%d')),],'sum')
datamagg$cr<-factor(datamagg$cr,levels=levels(datamagg$cr)[order(sumcases$value,decreasing=T)],ordered=T)

#Trend overview
ggplot(datamagg, aes(x=variable, y=value, col=cr)) + 
geom_line(show.legend=F) +
scale_x_date(date_breaks='4 week',date_labels='%d-%m') +
facet_wrap(~cr,scale='free_y') + 
theme_bw() + 
labs(x=NULL, y=NULL) +
theme(axis.text.y=element_text(size=5),axis.text.x=element_text(size=5))