
create_table <- function(data, last=3){
  
  for (i in (11+last):22) {
    train <- data %>% filter(year >= i - last, year < i)
    test <- data %>% filter(year == i)
    if (i == 11 + last) {
      new_table <- create_odds(train, test, i)
    } else {
      new_table <- rbind(new_table, create_odds(train, test, i))
    }
  }
  new_table <- new_table %>% mutate(H_odds = 1/H, D_odds = 1/D, A_odds = 1/A)
  return(new_table)
}

last = 1

table_all <- create_table(data, last)
write.csv(table_all, paste("Odds/last",last,"-all.csv", sep=""))

divisions <- c("E0", "D1", "I1", "SP1", "F1")

for(i in divisions) {
  table <- create_table(data %>% filter(Div == i))
  write.csv(table, paste("Odds/last",last,"-",i,".csv", sep=""))
}