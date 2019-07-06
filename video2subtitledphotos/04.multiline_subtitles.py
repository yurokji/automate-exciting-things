# -*- coding: utf-8 -*-
# Yurok Ji, 04/Jul/2019 
# yurokji@gmail.com
from PIL import ImageFont

myText = u"안녕하세요. 오늘은 긴 문장으로 된 자막을 나누는 방법을 알아보도록 하겠습니다. 긴 문장은 화면에서 잘리는 일이 종종 발생하므로 화면의 특정 크기에 따라 여러 줄로 미리 나눠주어야 문제가 없습니다"

max_width = 1024
font_size = 40
# 화면에 출력되는 폰트를 설정하고 자막을 넣어 화면에 자막이 잘리는지 확인하여 긴 문장을 여러 줄로 표시하도록 텍스트를 잘라줍니다
my_font = ImageFont.truetype("C:\\Windows\\Font\\NanumBarunGothicBold.ttf", font_size)
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
    
  for _, txt in enumerate(multiText):
    print(txt)
    