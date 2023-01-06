library(tidyverse)
library(nnet)
library(caret)

set.seed(05012023)

data <- read_csv("game_data.csv")

data <- data %>% filter(enough_games > 0, Div=='I1')

plot(data$form_H, data$form_A, col=factor(data$FTR))

training.samples <- data$Div %>% createDataPartition(p = 0.8, list = FALSE)
train <- data[training.samples,]
test <- data[-training.samples,]

model <- multinom(FTR ~ form_H + form_A + g_H + g_A + s_H + s_A + st_H + st_A + c_H + c_A, data=train)

summary(model)

predictions <- model %>% predict(test)

confusionMatrix(table(data=predictions, reference=test$FTR))

predictions_probs <- model %>% predict(test, "probs")

new_table <- cbind(test, predictions_probs)

new_table <- new_table %>% mutate(H_odds = 1/H, D_odds = 1/D, A_odds = 1/A)

write.csv(new_table, "predicted_odds.csv")
