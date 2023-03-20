# Ukraine-VHI-easy-reader
app that takes raw data from www.star.nesdis.noaa.gov and make it easier to search needed info by year/region


basically just uses pandas to make data more accessable

indexes at NOAA are weird so i made them alphabetical
tried fuzzywuzzy method to get name of region and replace them,but it didn't work properly and so i decided to link indexes manually
you can get min and max values for chosen region and also info about VHI value by every week