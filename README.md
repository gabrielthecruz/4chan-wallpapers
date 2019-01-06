# 4chan Wallpapers

A script to filter and download wallpapers from a 4chan board based on its resolution.

# Requirements
 - *requests*: ``pip install requests``

# Arguments
4chan-wallpapers.py *board* *resolution* *limit* *destination_path*
 - *board*: the chosen board to search the wallpapers, e.g.: wg
 - *resolution*: the wallpaper resolution you need, e.g.: 1920x1080 
 - *limit*: which filter you want to use, 'max' (to get >=), 'min' (to get <=) or 'equal' (to get ==)
 - *destination_path*: where all the wallpapers will be saved

