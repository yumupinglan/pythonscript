#-*- coding: utf-8 -*-
import os
import sys
import subprocess
from shutil import rmtree
from aip import AipSpeech
from langconv import *

APP_ID = '11375856'
API_KEY = 'PZK7NZRegvFBqXYKrwDhxRA9'
SECRET_KEY = '8wKyotCGAvsWpHgdDAsO2cKykW1zUNlD'

class mytool:
    def __init__(self):
        self.count = 0
        self.slideshow_list_filename = 'mytext.txt'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def rm_file(self,file):
        cmd = ['rm','-rf',file]
        cmd = map(lambda x: '%s' % x, cmd)
        subprocess.call(cmd)

    def resize_files(self,fname):
        # ffmpeg -i a.jpg -vf scale=640:480 a.png
        out_fname = fname.replace('orig','img')
        out_fname = out_fname.split('.')[0]+'.jpg'

        #print out_fname
        subprocess.call(['ffmpeg', '-i', fname, '-vf', 'scale=640:480', out_fname ])

    def list_orig(self,dir):
        basedir = dir
        subdirlist = []
        for item in os.listdir(dir):
                fullpath = os.path.join(basedir,item)
                if os.path.isdir(fullpath):
                        print  ('dir item=',fullpath)
                        subdirlist.append(fullpath)
                else:
                        print ('file item=',fullpath)
                        if item.startswith('orig'):
                                self.resize_files(fullpath)
        for subdir in subdirlist:
                self.list_orig(subdir)

    def generate_audio(self, dirname):
        basedir = dirname
        subdir = []
        slides = []
        sorted_texts = []
        for item in os.listdir(dirname):
            fullpath = os.path.join(basedir, item)
            if os.path.isdir(fullpath):
                subdir.append(fullpath)
            else:
               if item.startswith('text') and item.endswith('txt'):
                   slides.append(fullpath)
        sorted_texts = sorted(slides)
        for item in sorted_texts:
            with open(item, mode='r') as f:
                text = f.read()
                shortText = text.split('。')
                count = 0;
                for sentence in shortText:
                    self.generate_subtitle(item,sentence,count)
                    count += 1

    def simple2tradition(self,line):
        #将简体转换成繁体
        line = Converter('zh-hant').convert(line)
        return line

    def tradition2simple(self,line):
        # 将繁体转换成简体
        line = Converter('zh-hans').convert(line.decode('utf-8'))
        line = line.encode('utf-8')
        return line

    def generate_subtitle(self,item,sentence,count):
        #every sentence have one mp3 and one srt file
        if sentence.isspace() or len(sentence)==0 or sentence.__eq__('”'):
            return
        print(str(len(sentence)))
        print('current text ' + str(count) + ' to subtitle: ' + sentence)
        sentence = sentence.replace('\n','')
        sentence = sentence.replace('\r','')
        print(type(sentence) )
        result = self.client.synthesis(sentence, 'zh', 5, {
                        'vol': 10,'per':1,'spd':5,'pit':3})
        srtOrder = str(count)
        if len(srtOrder) == 1:
            srtOrder = '00' + srtOrder
        if len(srtOrder) == 2:
            srtOrder = '0' + srtOrder
        audio_file_name = item + '_' + srtOrder + '.mp3'
        if not isinstance(result, dict):
            with open(audio_file_name, 'wb') as w:
                w.write(result)
        cmd = ['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1','-sexagesimal',audio_file_name]
        cmd = map(lambda x: '%s' %x, cmd)
        time = subprocess.check_output(cmd)
        time = time.decode().replace('.',',')
        time = time[0:len(time)-3]


        srtFileName = item + '_' + srtOrder + '.srt'
        with open(srtFileName, mode='w') as w:
            w.write('1'+'\n')
            w.write('00:00:00,100 --> '+str(time)+'\n')
            if len(sentence) > 30 :
                length = len(sentence)
                number = length/30
                for i in range(0,int(number)+1):
                    start = 30*i
                    end = 30*(1+i)
                    if end >= length:
                        end = length
                    s = sentence[start:end]
                    w.write(self.simple2tradition(s)+'\n')
            #    s1 = sentence[0:30]
             #   s2 = sentence[30:len(sentence)]
              #  w.write(self.simple2tradition(s1)+'\n')
               # w.write(self.simple2tradition(s2)+'\n')
            else:
                w.write(self.simple2tradition(sentence))

    def add_fade_effect(self, infilename, outfilename = 'final'):
        # Makes two frames : at the beginning and at the end
        # This is done by copying one I-Frame for a slide
        # Then, adds fades at both ends
 
       # for f in self.copied_file:
        #    cmd = map(lambda x: '%s' %x, ['cp', infilename, f])
         #   subprocess.call(cmd)

        # make normal slide
        # ffmpeg -r 1/5 -i in%03d.png -c:v libx264 -r 30 -y -pix_fmt yuv420p slide.mp4 
        in_framerate = 1./5
        out_framerate = 30
        cmd = ['ffmpeg', '-loop', '1', '-i',infilename,'-c:v','libx264', 
                '-t', 15, '-y','-pix_fmt','yuv420p','-vf','scale=320:240','slide.mp4'] 
        cmd = map(lambda x: '%s' %x, cmd)
        subprocess.call(cmd)

        # add fade-in effect - from 0th to 30th frame
        #ffmpeg -i slide.mp4 -y -vf fade=in:0:30 slide_fade_in.mp4
        cmd = ['ffmpeg', '-i','slide.mp4','-y','-vf','fade=in:st=0:d=5','slide_fade_in.mp4']
        subprocess.call(cmd)

        # add fade-out effect to the slide that has fade-in effect already : 30 frames starting from 120th  
        #ffmpeg -i slide_fade_in.mp4 -y -vf fade=out:120:30 slide_fade_in_out.mp4 
        cmd = ['ffmpeg', '-i','slide_fade_in.mp4','-y','-vf','fade=out:st=10:d=5', 'slide_fade_in_out.mp4'] 
        subprocess.call(cmd)

        # rename the output to 'final#.mp4'
        slide_name = outfilename+str(self.count)+'.mp4'
        cmd = map(lambda x: '%s' %x, ['cp', 'slide_fade_in_out.mp4', slide_name]) 
        subprocess.call(cmd)

        # remove the copied files
        #for f in self.copied_file:
         #   cmd = map(lambda x: '%s' %x, ['rm','-f', f])
          #  subprocess.call(cmd)

        self.count += 1
 
        return slide_name
 
    # make concat list
    def make_slideshow_list(self, slides, fname='mylist.txt'):
        self.slideshow_list_filename = fname
        with open(self.slideshow_list_filename, mode='w') as f:
            for slide in slides:
                f.write('file ' + slide +'\n')

    # concat all slides in the slideshow list
   # def concat_slides(self, slideshow_name = 'my_slideshow.mp4' ):
    #    cmd = ['ffmpeg', '-y', '-f','concat','-i', self.slideshow_list_filename, '-c', 'copy', slideshow_name] 
     #   subprocess.call(cmd)


    # get the list of file 
    def file_list(self, d):
        basedir = d
    def concat_slides(self, path, slideshow_name = 'my_slideshow.mp4'):
        with open('/home/willieyu/youtubeWork/article/title.txt', mode='r') as f:
            slidesshow_name = f.read()
        slideshow_name = path+self.simple2tradition(slidesshow_name)+'.mp4'
        cmd = ['ffmpeg', '-y', '-f','concat','-safe','0','-i', self.slideshow_list_filename, '-c', 'copy', slideshow_name] 
        subprocess.call(cmd)

    # get the list of file 
    def file_list(self, d):
        basedir = d
        subdir = []
        slides = []
        sorted_slides = []
        for item in os.listdir(d):
            fullpath = os.path.join(basedir, item)
            if os.path.isdir(fullpath):
                subdir.append(fullpath)
            else:
               if item.startswith('img') and item.endswith('.jpg') :
                   slides.append(fullpath)
        return sorted(slides)

    #get the list of audio and image
    def a_i_map(self,d):
        basedir = d
        subdir = []
        audios = []
        for item in os.listdir(d):
            fullpath = os.path.join(basedir, item)
            if os.path.isdir(fullpath):
                subdir.append(fullpath)
            else:
               if item.endswith('.mp3') :
                   audios.append(fullpath)
        return sorted(audios)

    # get images for audio
    def img_by_audio(self,audio,images):
        index = audio.find('text')
        img_path = 'img'+audio[index+4:index+8]
        for item in images:
            if img_path in item:
                return item

    def audio_to_video(self,audio,images):
        img_path = self.img_by_audio(audio,images)
        srt_path = audio.replace('mp3','srt')
        video_name = audio.replace('mp3','mp4')
        srt_video_name = audio.replace('.mp3','')+'_srt.mp4'
        cmd = ['ffmpeg','-loop', '1','-i',img_path,'-i',audio,'-c:v', 'libx264','-c:a','copy','-shortest',video_name]
        cmd = map(lambda x: '%s' %x,cmd)
        subprocess.call(cmd)
        cmd = ['ffmpeg','-i',video_name,'-vf', 'subtitles='+srt_path,srt_video_name]
        cmd = map(lambda x: '%s' %x,cmd)
        subprocess.call(cmd)
        return srt_video_name

    def genereateVideo(self,path,videoPath):
        self.list_orig(path)
        self.generate_audio(path)
        audios = self.a_i_map(path)
        slides = self.file_list(path)
        videos = []
        for audio in audios:
            videos.append(self.audio_to_video(audio, slides))
        self.make_slideshow_list(videos)
        self.concat_slides(videoPath)
        # clear directory
        rmtree(path)
        os.mkdir(path)

if __name__ == '__main__':
    path = '/home/willieyu/youtubeWork/article/'
    m = mytool()
    m.list_orig(path)
    m.generate_audio(path)
    audios = m.a_i_map(path)
    slides = m.file_list(path)
    videos = []
    for audio in audios:
        videos.append(m.audio_to_video(audio,slides))
    m.make_slideshow_list(videos)
    m.concat_slides('/home/willieyu/youtubeWork/')
    #rmtree(path)
    #os.mkdir(path)
# make slideshow list file
