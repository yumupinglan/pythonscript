import os
import sys
import subprocess
import psutil
from shutil import rmtree
from aip import AipSpeech
import re
import datetime

APP_ID = '11375856'
API_KEY = 'PZK7NZRegvFBqXYKrwDhxRA9'
SECRET_KEY = '8wKyotCGAvsWpHgdDAsO2cKykW1zUNlD'

class convert_tool:

    def __init__(self):
        self.count = 0
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def generate_audio(self,text):
        if text.isspace() or len(text) == 0 or text.__eq__('”'):
            return
        sentences = re.split(r"[.。；;?!]",text)
        count = 1
        start = 0.0
        end = 0.0
        for sentence in sentences:
            if sentence.isspace() or len(sentence) == 0 or sentence.__eq__('”'):
                continue
            print('current sentence:'+sentence)
            start=end
            end=end+self.generate_subtitle(sentence,count)
            self.append_srt('test.srt',sentence, self.getSrtTime(start),self.getSrtTime(end),count)
            count = count+1


    def generate_subtitle(self, sentence, count):
        # every sentence have one mp3 and one srt file
        if sentence.isspace() or len(sentence) == 0 or sentence.__eq__('”'):
            return
        print(str(len(sentence)))
        print('current text ' + str(count) + ' to subtitle: ' + sentence)
        sentence = sentence.replace('\n', '')
        sentence = sentence.replace('\r', '')
        print(type(sentence))
        result = self.client.synthesis(sentence, 'zh', 5, {
            'vol': 10, 'per': 1, 'spd': 5, 'pit': 3})
        srtOrder = str(count)
        if len(srtOrder) == 1:
            srtOrder = '00' + srtOrder
        if len(srtOrder) == 2:
            srtOrder = '0' + srtOrder
        audio_file_name = srtOrder + '.mp3'
        if not isinstance(result, dict):
            with open(audio_file_name, 'wb') as w:
                w.write(result)
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
               'default=noprint_wrappers=1:nokey=1',
               '-sexagesimal', audio_file_name]
        cmd = map(lambda x: '%s' % x, cmd)
        time = subprocess.check_output(cmd)
        time = time.decode().replace('.', ',')
        time = time[0:len(time) - 4]
        sec = self.getStanderTime(time)
        print(time)
        print(sec)
        print(self.getSrtTime(sec))
        return sec


    def append_srt(self,srtFileName,sentence, start,end,count):
        with open(srtFileName, mode='a') as w:
            w.write(str(count) + '\n')
            w.write(start+' --> ' + end + '\n')
            if len(sentence) > 30:
                length = len(sentence)
                number = length / 30
                for i in range(0, int(number) + 1):
                    start = 30 * i
                    end = 30 * (1 + i)
                    if end >= length:
                        end = length
                    s = sentence[start:end]
                    w.write(s + '\n')
            else:
                w.write(sentence+'\n')

    def getStanderTime(self,srtTime):
        times = list(map(int, re.split(r"[:,]", srtTime)))
        sec = times[0] * 3600 + times[1] * 60 + times[2]+times[3]/1000
        return sec

    def getSrtTime(self,sec):
        times = str(datetime.timedelta(seconds=sec))
        if sec != 0:
            times = times[0:len(times) - 3]
        return times

if __name__ == '__main__':
    tool = convert_tool()
    s = "123456提到算卦，很多人对此嗤之以鼻，也有很多人对此深信不疑，更多人的态度是选择相信。嗤之以鼻者完全否定算卦的用处，认为算卦就是封建迷信，这类人信仰的是科学。深信不疑者把算卦作为行事的最高准则，把算卦作为一种宗教来信仰。选择相信者，这类人在现实中最多，持有信则有不信则无的态度， 或者选择好听的信，不好的就觉得是瞎扯的态度。"
    #tool.generate_subtitle('1',s,1)
    tool.generate_audio(s)