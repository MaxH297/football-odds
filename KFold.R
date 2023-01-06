library(rsample)

set.seed(05012023)

data <- read_csv("game_data.csv")

data <- data %>% filter(enough_games > 0)



create_table <- function(data, v=10){
  folds <- data %>% vfold_cv(v=v)
  
  train_splits <- map(folds$splits,analysis)
  test_splits <- map(folds$splits,assessment)
  
  for (i in 1:v) {
    train <- train_splits[[i]]
    test <- test_splits[[i]]
    if (i == 1) {
      new_table <- create_odds(train, test, i)
    } else {
      new_table <- rbind(new_table, create_odds(train, test, i))
    }
  }
  new_table <- new_table %>% mutate(H_odds = 1/H, D_odds = 1/D, A_odds = 1/A)
  return(new_table)
}

table_all <- create_table(data)
write.csv(table_all, "Odds/kf-all.csv")

divisions <- c("E0", "D1", "I1", "SP1", "F1")

for(i in divisions) {
  table <- create_table(data %>% filter(Div == i))
  write.csv(table, paste("Odds/kf-",i,".csv", sep=""))
}
