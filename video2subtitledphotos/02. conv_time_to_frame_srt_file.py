# -*- coding: utf-8 -*-
# convert list of subtitle times in srt file to the list of video frame numbers
import pysrt
# pip install pysrt <-- before you run this script
subname = 'youtube_video.ko.srt'
subs = pysrt.open(subname)
lenSubs = len(subs)
prev_text=""
fps = 30

for i in range(lenSubs):
    sub = subs[i]
    # convert start time to  start frame
    hour_start_frame = sub.start.hours * 60 * 60 * fps
    minute_start_frame = sub.start.minutes * 60 * fps
    second_start_frame = sub.start.seconds *  fps
    milisecond_start_frame = sub.start.milliseconds * 0.001 * fps
    start_frame = hour_start_frame + minute_start_frame + second_start_frame + milisecond_start_frame
    # convert end time to end frame
    hour_end_frame = sub.end.hours * 60 * 60 * fps
    minute_end_frame = sub.end.minutes * 60 * fps
    second_end_frame = sub.end.seconds *  fps
    milisecond_end_frame = sub.end.milliseconds * 0.001 * fps
    end_frame = hour_end_frame + minute_end_frame + second_end_frame + milisecond_end_frame
    # to safely calculate the current frame position
    # we should use both start frame and end frame
    frame = int(round((start_frame + end_frame) / 2, 0)) 
    
    if lenSubs == 0:
        break
    if sub.text == prev_text:
        continue
    print("video frame: ", frame)
    print(sub)

