#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import time

from aip import AipSpeech
from pydub import AudioSegment
from welcome_phrase import welcome_phrase

# Step 1, Using baidu AI to generate mp3 file from text
# input your APP_ID/API_KEY/SECRET_KEY
APP_ID = '32174628'
API_KEY = 'BjzM7O32sVpYYpvlVkttbEKf'
SECRET_KEY = 'PoLKcMTR7cQKppWu1iXY7MSbzC6PCBth'




def generate_welcome_wav():
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    phrase = welcome_phrase()
    result = client.synthesis(phrase, 'zh', 1, {'vol': 5, 'per': 5})
    if not isinstance(result, dict):
        with open('welcome.mp3', 'wb') as f:
            f.write(result)

    # Step 2, convert the mp3 file to wav file
    sound = AudioSegment.from_mp3('welcome.mp3')
    sound.export("welcome.wav", format="wav")

if __name__ == '__main__':
    start = time.time()
    generate_welcome_wav()
    end = time.time()
    print(f'{(end - start):.2f}')
