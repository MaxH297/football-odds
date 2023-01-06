library(rsample)
library(tidyverse)
library(nnet)
library(caret)

create_odds <- function(train, test, i){
  model <- multinom(FTR ~ form_H + form_A + g_H + g_A + s_H + s_A + st_H + st_A + c_H + c_A, data=train)
  predictions_probs <- model %>% predict(test, "probs")
  new_table <- cbind(test, predictions_probs)
  new_table <- new_table %>% mutate(iter = i)
  return(new_table)
}