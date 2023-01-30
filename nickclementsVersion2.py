import cv2 
import numpy as np
import sys
from datetime import datetime
from pydub import AudioSegment
import glob
import sys
import os
import time
from moviepy.editor import *
import shutil
import subprocess
import random
import string
#vid1path = r"""C:\Users\Heathcliff\Desktop\Work\OnlineJobsPH\AutomateTikTokVods\2022-11-11 13-40-01.mkv"""
#vid2path = r"""C:\Users\Heathcliff\Pictures\Camera Roll\WIN_20230104_03_30_28_Pro.mp4"""
def get_random_string():
    length = 10
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def startVideoProcess(vid1path, vid2path, modeChoice):
    video1 = cv2.VideoCapture(vid1path)
    video2 = cv2.VideoCapture(vid2path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.now()
    currentTime = now.strftime("%H-%M-%S")
    video_writer = cv2.VideoWriter(f"{currentTime}.avi", fourcc, 30.0, (1080, 1920))

    while video1.isOpened():
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()   

        if ret1 == False or ret2 == False:
            break

        frame1 = cv2.resize(frame1, (1080,960))
        frame2 = cv2.resize(frame2, (1080,960))
        vid_comb = cv2.vconcat([frame1, frame2])

        #cv2.imshow('Frame', vid_comb)
        video_writer.write(vid_comb)

    video_writer.release()
    video1.release()
    video2.release()
    cv2.destroyAllWindows()

    ############## extracting audio ###################
    video1 = VideoFileClip(vid1path)
    video2 = VideoFileClip(vid2path)
    
    #audio2 = input(filePath2)
    video1.audio.write_audiofile(f"{currentTime}-1.wav")
    video2.audio.write_audiofile(f"{currentTime}-2.wav")

    ############## done extracting audio #################

    time.sleep(1)
    video1.close()
    video2.close()

    finalVideo = VideoFileClip(f"{currentTime}.avi")
    #audio1 = AudioFileClip(f"{timenow}-1.wav")
    #audio2 = AudioFileClip(f"{timenow}-2.wav")

    ########################### PYDUB
    audio1 = AudioSegment.from_wav(f"{currentTime}-1.wav")

    # Open the second audio file
    audio2 = AudioSegment.from_wav(f"{currentTime}-2.wav")

    # Make sure that the two audio signals have the same length
    min_length = len(audio1)

    audio1 = audio1[:min_length]
    audio2 = audio2[:min_length]

    # overlay the two audio signals
    overlay = audio1.overlay(audio2)

    # Write the combined audio to a new file
    overlay.export(f"final-{currentTime}.wav", format="wav")
    ########################### END OF PYDUB

    #audio1 = audio1.set_duration(finalVideo.duration)
    #audio2 = audio2.set_duration(finalVideo.duration)
    audioFinal = AudioFileClip(f"final-{currentTime}.wav")
    final_video = finalVideo.set_audio(audioFinal)
    #final_video = finalVideo.set_audio(audio2)

    #finalVideo.close()

    final_video.write_videofile(f"final-{currentTime}.avi", codec="h264")
    time.sleep(1)

    print(f"mode was {modeChoice}")
    files = glob.glob('*.wav')
    os.remove(f"{currentTime}.avi")
    print(f"{currentTime}.avi: removed.")
    for file in files:
        print(f"{file}: removed.")
        os.remove(file)
    #shutil.move(vid2path, r"c:\Users\Heathcliff\Desktop\Work\OnlineJobsPH\AutomateTikTokVods\dist\sample - Copy.mkv")
    print(vid2path)
    print(f"{os.getcwd()}{chr(92)}Cleared Files")
    if modeChoice == "1":
        try:
            shutil.move(vid2path, f"{os.getcwd()}{chr(92)}Cleared Files")
            print(f"{vid2path} - {chr(92)}Cleared Files{chr(92)}{vid2path.split(chr(92))[-1]}")
            print(f"{vid2path}: was moved to cleared files.")
        except:
            print(f"Either File 1 or File 2 is already in the path.")

    if modeChoice == "2":
        try:
            shutil.move(vid1path, f"{os.getcwd()}{chr(92)}Cleared Files")
            print(f"{vid1path} - {chr(92)}Cleared Files{chr(92)}{vid1path.split({chr(92)})[-1]}")
            print(f"{vid1path}: was moved to cleared files.")
        except:
            print(f"Either File 1 or File 2 is already in the path.")       
    if modeChoice == "3":
        print(f"{vid1path} and {vid2path} were retained.")
    if modeChoice == "4":
        try:
            shutil.move(vid1path, f"{os.getcwd()}{chr(92)}Cleared Files")
            shutil.move(vid2path, f"{os.getcwd()}{chr(92)}Cleared Files")
        except:
            print(f"Either File 1 or File 2 is already in the path.")
    meta_data = get_random_string()
    try:
        subprocess.run(["exiftool", f"-Title={meta_data}", "-overwrite_original", f"final-{currentTime}.mp4"])
        print(f"Changed the meta data of the final-{currentTime}.mp4 \n Title: {meta_data}")
    except:
        print("Exif tool not installed.")
    
startVideoProcess(sys.argv[1], sys.argv[2], sys.argv[3])
