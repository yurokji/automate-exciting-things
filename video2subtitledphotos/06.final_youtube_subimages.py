# -*- coding: utf-8 -*-
# Yurok Ji, 06/Jul/2019 
# yurokji@gmail.com
# 유튜브 영상을 자막 이미지로 만들기 강좌
# 6강: 프로그램 통합 

import os
import pysrt
import pylab
import imageio
from PIL import ImageFont, Image, ImageDraw


def convMultiLine(myText, max_width, my_font):
  multiText = []
  # 만약 텍스트 길이가 max_width보다 작다면
  # 텍스트를 여러 줄로 나누지 않고
  # 그대로 결과를 반환합니다
  if my_font.getsize(myText)[0] <= max_width:
    multiText.append(myText)
    
  else:
    # 텍스트 줄 나누기를 시작합니다
    # 텍스트를 모두 단어 단위로 분할하기 시작합니다
    # 한 줄씩 멀티텍스트에 붙여주고 완성된 결과를 반환합니다
    words = myText.split(' ')
    count  = 0
    while count < len(words):
      singleLine = ''
      while count < len(words) and my_font.getsize(singleLine + words[count])[0] <= max_width:
        singleLine += words[count]
        singleLine += ' '
        count += 1
      if not singleLine:
        singleLine = words[count]
        count += 1
      multiText.append(singleLine)
  return multiText  

url = 'https://www.youtube.com/watch?v=GzD3Wask0Nk'

videoname = 'youtube_video'
filename = videoname + '.mp4'
sub_language = 'ko'
subname = videoname + '.' + sub_language + '.srt' 
'youtube_video_ko.srt'
download_command ='youtube-dl -f22 --write-sub --convert-subs srt -o ' + filename + ' --sub-lang ' + sub_language + ' ' + url
os.system(download_command)



subname = 'youtube_video.ko.srt'
subs = pysrt.open(subname)
lenSubs = len(subs)
prev_text=""
fps = 30
filename = 'youtube_video.mp4'
reader = imageio.get_reader(filename, 'ffmpeg')


count = 0
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
	image = reader.get_data(frame)
	pylab.imsave('temp.jpg', image)

	if lenSubs == 0:
		break
	if sub.text == prev_text:
		continue
	print("video frame: ", frame)
	print(sub)




	# 영상 프레임 이미지 열기
	photo = Image.open('temp.jpg')
	# 영상위에 합성할 자막 이미지 만들기
	draw = ImageDraw.Draw(photo)
	photoWidth, photoHeight = photo.size

	font_size = 40
	# 화면에 출력되는 폰트를 설정하고 자막을 넣어 화면에 자막이 잘리는지 확인하여 긴 문장을 여러 줄로 표시하도록 텍스트를 잘라줍니다
	my_font = ImageFont.truetype("C:\\Windows\\Font\\NanumBarunGothicBold.ttf", font_size)

	multiLine = convMultiLine(sub.text, photoHeight, my_font)

	lenLines = len(multiLine)

	# 영상의 프레임에서 자막 한 줄당 최대 높이를 구해봅시다
	# th; 자막의 최대 높이
	th = 0
	for line in multiLine:
	  # 자막의 빈줄을 제거
	  line = " ".join(line.splitlines())
	  _, ty = draw.textsize(line, font=my_font)
	  if th < ty:
	    th = ty


	# 자막을 영상의 프레임에 입혀봅시다
	# cntLine; 현재 프레임에서 처리할 현재 자막의 행번호
	cntLine = 0
	padY = photoHeight / 10
	padRectX = 10
	padRectY = 10
	for line in multiLine:
	  line = " ".join(line.splitlines())
	  # tw: 자막의 최대 너비
	  tw, _ = draw.textsize(line, font=my_font)
	  # 이미지에서 자막과 자막 배경의 시작 위치 (왼쪽 상단 ) 계산
	  # x1, y1; 자막의 시작 위치
	  x1 = (photoWidth - tw) / 2
	  y1 = photoHeight - ((lenLines - cntLine) * th) - padY

	  # 두번째 줄부터는 자막과 자막 배경(사각형) 위치를 아래로 살짝 내려줍니다
	  if cntLine > 0:
	    y1 += padRectY * cntLine

	  # 이미지에서 자막과 자막 배경 사각형의 끝 위치 (오른쪽 하단) 계산
	  x2 = x1 + tw
	  y2 = y1 + th

	  # 자막이 자막 배경 안에 안정적으로 위치하도록 가로 세로 패딩을 넣어줍니다
	  rx1 = x1 - padRectX // 2
	  ry1 = y1 - padRectY // 2
	  rx2 = x2 + padRectX // 2
	  ry2 = y2 + padRectY // 2

	  # 자막 배경을 그려줍시다
	  draw.rectangle( ((rx1, ry1), (rx2, ry2)), fill="black")
	  # 자막을 그려줍시다.
	  draw.text((x1, y1), line, font=my_font, fill="white")
	  cntLine += 1

	  # 자막과 합성한 영상 프레임 이미지를 저장해줍니다.
	photo.save('image {:05d}.jpg'.format(count))
	count += 1


  
