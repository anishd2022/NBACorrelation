# Import necessary libraries
library(tidyverse)
library(jsonlite)
library(tidyjson)

# Function to get current prizepicks projections 
get_current_prizepicks_projections <- function() {
  prizepicks_url <- "https://api.prizepicks.com/projections"
  prizepicks_data <- fromJSON(prizepicks_url, flatten = TRUE)
  
  # Data frames for players and odds on prize picks
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
  
  # Inner join the two tables by player ID:
  PP_player_odds_data <- inner_join(nba_player_data, odds_data, by = "id") %>%
    filter(relationships.league.data.id == 7) %>% arrange(attributes.start_time) %>%
    select(-c(attributes.combo, attributes.league, attributes.league_id, relationships.league.data.id))
  
  return(PP_player_odds_data)
}

# Function to merge current projections with the master CSV
merge_with_master <- function(new_data, master_csv_path) {
  # Read the existing master CSV
  master_data <- read.csv(master_csv_path)
  
  # Merge new data with master data and remove duplicates
  merged_data <- unique(rbind(master_data, new_data))
  
  # Write the merged data back to the master CSV
  write.csv(merged_data, file = master_csv_path, row.names = FALSE)
}

# Get current projections
current_PP_projections <- get_current_prizepicks_projections()

# Specify the path to the master CSV
master_csv_path <- "All_NBA_Projections.csv"

# Merge current projections with the master CSV
merge_with_master(current_PP_projections, master_csv_path)


# run this line once at the beginning
# write.csv(current_PP_projections, "All_NBA_Projections.csv", row.names = FALSE)

