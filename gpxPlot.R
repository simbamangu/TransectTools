# Read GPX files and make a chart

gpxPlot <- function(gpxfile, spdfmt = "kmh", plotfn = NA) {
  # Plot ground speed against time for a GPX input file.
  # Input 'gpxfile' = path to a GPX file
  # Speed in km/h by default, set spdfmt to anything else for ms.
  # Output: graph, to save a file set plotfn to filename
  require(sf)
  require(tidyverse)
  trk <- read_sf(dsn = gpxfile, layer = "track_points") %>%
    select(c(1:5, 'ogr_agl'))  %>% # Get rid of everything except basic track data
    mutate(dist = st_distance(., lag(.), by_element = T)) %>% 
    mutate(speed = 3.6 * as.numeric(dist) / (as.numeric(time - lag(time)))) 
  
  if (spdfmt != "kmh") {
    trk$speed <- trk$speed / 3.6
  }
  
  g <- ggplot(data = trk, aes(x = time, y = speed))
  g + geom_point(cex = 0.1, color = "darkgray") + #ylim(150, 220) +
    stat_smooth(na.rm = T, span = 240 / nrow(trk), method = 'loess') +
    geom_hline(aes(yintercept = 55), colour = 'red') + 
    geom_hline(aes(yintercept = 47), colour = 'green')
  if (!is.na(plotfn)) {
    ggsave(plotfn)
  }
}