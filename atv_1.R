# https://bigrquery.r-dbi.org/
# https://www.infoworld.com/article/3622926/how-to-use-r-with-bigquery.html


#install package
pacotes <- c("bigrquery","purrr")

if(sum(as.numeric(!pacotes %in% installed.packages())) != 0){
  instalador <- pacotes[!pacotes %in% installed.packages()]
  for(i in 1:length(instalador)) {
    install.packages(instalador, dependencies = T)
    break()}
  sapply(pacotes, require, character = T) 
} else {
  sapply(pacotes, require, character = T) 
}

# install.packages('devtools')
devtools::install_github("r-dbi/bigrquery")


billing <- bq_test_project() # replace this with your project ID 
sql <- "SELECT * FROM `bigquery-public-data.fda_food.food_events`"

tb <- bq_project_query(billing, sql)
bq_table_download(tb, n_max = 10)


library(bigrquery)
library(dplyr)
con <- dbConnect(
  bigrquery::bigquery(),
  project = "bigquery-public-data",
  dataset = "fda_food",
  billing = "greenpeace-360016"
)

dbListTables(con)


