library(ISLR)
library(e1071)
library(caret)

setwd("~/Data Science/Sem 3/Data Mining/Final Project")
MyData <- read.csv(file="creditcardfraud/creditcard.csv", header=TRUE, sep=",")
colnames(MyData[-31])

set.seed(10)  # setting seed to reproduce results of random sampling
trainingRowIndex <- sample(1:nrow(MyData), 0.8*nrow(MyData))  # row indices for training data
trainingData <- MyData[trainingRowIndex, ]
testData  <- MyData[-trainingRowIndex, ]  

linearMod <- lm(Class ~ V3+V4+V7+V9+V10+V11+V12+V14+V16+V17+V18, data=trainingData)
#+V1+V2+V5+V6+V8+V13+V15+V19+V20++V21+V22+V23+V24+V25+V26+V27+V28+Amount+Time
Pred <- predict(linearMod, testData)

Pred[Pred<0.1] = 0
Pred[Pred>0] = 1
sum(Pred==testData[31])/length(Pred)
confusionMatrix(as.factor(Pred), as.factor(testData$Class))

trainingData$Class = as.factor(trainingData$Class)

SVMmod <- svm(trainingData[c(4,5,8,10,11,12,13,15,17,18,19)], trainingData$Class, type = "C" ,kernel = "linear", tolerance = 0.01)
#SVMmod <- svm(trainingData[c(rep(TRUE,100000),trainingData$Class[-1:-100000]==1), c(4,5,8,10,11,12,13,15,17,18,19)], trainingData$Class[c(rep(TRUE,100000),trainingData$Class[-1:-100000]==1)], type = "C" ,kernel = "linear", tolerance = 0.1)
Pred1 <- predict(SVMmod, testData[c(4,5,8,10,11,12,13,15,17,18,19)])
confusionMatrix(Pred1, as.factor(testData$Class))

Pred_0.7_.01 = Pred1
test_0.7_.01 = testData$Class

getAnywhere(predict.default)
getAnywhere(randomForest.default)
