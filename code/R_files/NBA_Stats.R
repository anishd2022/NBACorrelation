# this script gets all NBA player stats from each game since the start of the 2023-2024 NBA regular season     
# importing libraries
library(tidyverse)
library(jsonlite)
library(tidyjson)

starting_page <- 464


# function to get all NBA player stats for each game:
get_all_player_stats <- function() {
  balldontlie_url <- "https://www.balldontlie.io/api/v1/stats"
  balldontlie_data <- fromJSON(paste0(balldontlie_url, "?seasons[]=2023"))
  total_pages <- balldontlie_data$meta$total_pages
  player_stats <- data.frame()

  for (page in starting_page:total_pages) {
    tryCatch({
      current_page_data <- fromJSON(paste0(balldontlie_url, "?seasons[]=2023&page=", page), 
                                    flatten = TRUE)$data
      player_stats <- rbind(player_stats, current_page_data)
      print(page)
    }, error = function(e) {
      # Handle the error here
      print(paste("Error on page", page, ": ", e$message))
      # format it accordingly...
      formatted_player_stats <- player_stats %>% select(-c(game.home_team_id, game.home_team_score, game.period,
                                                           game.postseason, game.season, game.status, game.time,
                                                           game.visitor_team_id, game.visitor_team_score, player.height_feet,
                                                           player.height_inches, player.weight_pounds, team.abbreviation,
                                                           team.city, team.conference, team.division, team.name)) %>%
        mutate(player_full_name = paste0(player.first_name, " ", player.last_name)) %>%
        select(-c(player.first_name, player.last_name, player.position, team.full_name,
                  fg3_pct, fg_pct, ft_pct, id, player.team_id)) %>% na.omit() %>% 
        mutate(blk_stl = blk + stl, pts_rebs = pts + reb, pts_rebs_ast = pts + reb + ast,
               pts_ast = pts + ast, rebs_ast = reb + ast,
               fantasy = 3*(blk_stl) + 1.5*(ast) + 1.2*(reb) + pts - turnover)
      # Save your data frame
      write.csv(formatted_player_stats, file = paste0("player_stats_", starting_page, "_to_", page-1))
      # Halt the program or take other appropriate actions
      stop("Program halted due to an error.")
    })
  }
  
  
  formatted_player_stats <- player_stats %>% select(-c(game.home_team_id, game.home_team_score, game.period,
                                                       game.postseason, game.season, game.status, game.time,
                                                       game.visitor_team_id, game.visitor_team_score, player.height_feet,
                                                       player.height_inches, player.weight_pounds, team.abbreviation,
                                                       team.city, team.conference, team.division, team.name)) %>%
    mutate(player_full_name = paste0(player.first_name, " ", player.last_name)) %>%
    select(-c(player.first_name, player.last_name, player.position, team.full_name,
              fg3_pct, fg_pct, ft_pct, id, player.team_id)) %>% na.omit() %>% 
    mutate(blk_stl = blk + stl, pts_rebs = pts + reb, pts_rebs_ast = pts + reb + ast,
           pts_ast = pts + ast, rebs_ast = reb + ast,
           fantasy = 3*(blk_stl) + 1.5*(ast) + 1.2*(reb) + pts - turnover)
  
  #return(formatted_player_stats)
  write.csv(formatted_player_stats, file = paste0("player_stats_", starting_page, "_to_", page))
}

get_all_player_stats()



