# Open file output matrix which includes every hit

# Identify the file
datafilename="output_01-08-14_1532.csv"

# Read the data file
target.data = read.csv(datafilename, header=TRUE)  #read the data file

# List the variables
names(target.data)



# Review the data
library(psych)


# Output Descriptives
library(R2HTML)

#   Output Table

printme <- j #printing variable
#   Code for outputting tables
HTMLStart(outdir=".",file="myreport",extension="html",ech=FALSE,HTMLframe=TRUE)
printme
HTMLStop()

library(reshape)

# Generate Appropriate Datasets to Test
target.data -> df
attach(df)

# Add Targets
tis <- targetsinspeech <- cast(df,speech ~ target)
tis$raw_pscore = rowSums(tis) 

# Add Wordcount
agg.df <- aggregate(df, by=list(speech), FUN=mean, na.rm=TRUE )
tis$wordcount = agg.df$wordcount

# Add adjusted pscore
tis$pscore = tis$raw_pscore / tis$wordcount

names(tis)[1] <- "speechnum"

#rename dataframe
sdf <- tis #sotu data frame)

# add dates
#   #list of speeches with dates
dates <- aggregate(speech ~ date,data = df, mean)
head(dates$date)
sdf$date <- dates$date
head(sdf)


aggregate(speech ~ president,date = df)


# Add Presidents
head(df$president)
q <- table(df$speech,df$president)
# biggest variable for each speech is president

q <- as.data.frame.matrix(q)
q <- t(q)

ncol(q)



for (i in (1:114)) {
  sdf$pres[i] <- names(which.max(q[,i]))

}

#### Time Series Calculations

sdf$date <- as.Date(sdf$date)
plot(sdf$date,sdf$pscore)

# use zoo library for irregularly spaced time series
library(zoo)
pscore.z <- zoo(x=sdf$pscore, order.by=sdf$date)

regl <- lm(sdf$pscore ~ sdf$date)
par(cex=.8)
plot(sdf$date,sdf$pscore)
abline(regl)
summary(regl)

## [[[ TODO Create a subset with LBJ set to NULL
which.max(sdf$pscore)
sdf_nolbj <- sdf[-65,]

sdf_nolbj <- sdf
sdf_nolbj[65,] <- NA
## ]]]

# Polynomial


library(lattice)
library(latticeExtra)
xyplot(pscore ~ date, sdf,par.settings = ggplot2like()) + 
  layer(panel.smoother(y ~ poly(x, 2), method = "lm"), style = 2)
# > Based on statsmooth

# Using statsmooth:
library(ggplot2)
ggplot(sdf,aes(date,pscore)) + 
  stat_smooth(method = "lm", formula = y ~ poly(x, 2), size = 1) + 
  geom_point()

# plot again without lbj
xyplot(pscore ~ date, sdf_nolbj,main = "Polynomial Regression with LBJ '64 Speech Removed",par.settings = ggplot2like()) + 
  layer(panel.smoother(y ~ poly(x, 2), method = "lm"), style = 2)

sdf.lm <- lm(pscore ~ date,sdf)
sdf.lm.poly2 <- lm(pscore ~ poly(date,2),sdf)
sdf_nolbj.lm.poly2 <- lm(pscore ~ poly(date,2),sdf_nolbj)

summary(sdf.lm)
plot(sdf.lm,1:6)
sdf$pscore[65]

# Note that rlm can be set to be more or lest responsive to outliers.

# Comparing it with top 1% Data

# Take a subset of sdf just date and pscore
myvars <- c("speechnum","date","pscore")
newdf <- sdf[myvars]
write.csv(newdf,file="newdf.csv")


# After munging data in excel, read back in
copdat <- read.delim("clipboard")
names(copdat)
library(hmisc)
j=cor.test(copdat$JusticeSpeechScore,copdat$TopOneShare,use="complete.obs")