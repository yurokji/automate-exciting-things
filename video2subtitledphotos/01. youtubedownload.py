import os
# copy and paste your Youtuble url
url = 'https://www.youtube.com/watch?v=GzD3Wask0Nk'
quality = 'best'
subtitle_language = 'ko'
subtitle_ext = 'srt'
videoname = 'youtube_video'
filename = videoname + '.mp4'
subname = videoname + '.' + subtitle_language +'.' + subtitle_ext
resultname = 'result.mp4'
download_command = 'youtube-dl -f22 --write-sub --convert-subs ' + subtitle_ext + ' -o ' + filename + ' --sub-lang' + ' ' + subtitle_language + ' ' + url
# execute the command in command prompt
# you need to install youtube-dl using 'pip install youtube-dl' beforehand 
os.system(download_command)


