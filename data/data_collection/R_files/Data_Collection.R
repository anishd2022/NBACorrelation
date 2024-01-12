# importing packages
library(tidyverse)
library(jsonlite)
library(tidyjson)



# function to get current prizepicks projections 
get_current_prizepicks_projections <- function() {
  prizepicks_url <- "https://api.prizepicks.com/projections"
  prizepicks_data <- fromJSON(prizepicks_url, flatten = TRUE)
  
  # data frames for players and odds on prize picks
  odds_data <- prizepicks_data$data %>% filter(attributes.odds_type == 'standard') %>%
    select(c(attributes.game_id, attributes.line_score, attributes.stat_type,
             relationships.new_player.data.id, relationships.league.data.id,
             attributes.start_time))
  colnames(odds_data)[colnames(odds_data) == "relationships.new_player.data.id"] <- "id"
  
  nba_player_data <- prizepicks_data$included %>% 
    filter(attributes.league == 'NBA') %>% 
    select(c(id, attributes.combo, 
             attributes.display_name,
             attributes.team_name, 
             attributes.position,
             attributes.league,
             attributes.league_id))
  
  # inner join the two tables by player ID:
  PP_player_odds_data <- inner_join(nba_player_data, odds_data, by = "id") %>%
    filter(relationships.league.data.id == 7) %>% arrange(attributes.start_time)
  
  return(PP_player_odds_data)
}

current_PP_projections <- get_current_prizepicks_projections()


# write the current projections to a CSV file, labeling it based on earliest game start time  
write.csv(current_PP_projections, file = paste0("PP_projections", current_PP_projections$attributes.start_time[1]), row.names = FALSE)       

