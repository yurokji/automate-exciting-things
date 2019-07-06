# -*- coding: utf-8 -*-
# 비디오 영상을 이미지로 변환해보도록 하겠습니다
# lecture: 29/Jun/2019

import pylab
import imageio

filename = 'youtube_video.mp4'
reader = imageio.get_reader(filename, 'ffmpeg')
fps = 30
for i, image in enumerate(reader):
  # 비디오에서 1초마다 한장씩 이미지로 저장
  if i % fps == 0:
    print('captured frame: ', i)
    pylab.imsave('image {:04d}.jpg'.format(i), image)
