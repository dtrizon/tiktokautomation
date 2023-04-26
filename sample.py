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
def get_random_string():
    length = 10
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def startVideoProcess(vid1path, vid2path, modeChoice, typeConvert, zoomOptions, zoomOptionsF2, outputPathFile, movInclude):
    video1 = cv2.VideoCapture(vid1path)
    video2 = cv2.VideoCapture(vid2path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.now()
    fps = video1.get(cv2.CAP_PROP_FPS)
    currentTime = now.strftime("%H-%M-%S")
    zoomFactor2 = 1.25
    #video_writer = cv2.VideoWriter(f"{currentTime}.avi", fourcc, 30.0, (1080, 1920))

    if not video1.isOpened():
        print("error")
    else:
        retwhat, firstF = video1.read()
        #print(firstF.shape[1])
        if (typeConvert == "1"):
            video_writer = cv2.VideoWriter(f"{currentTime}.avi", fourcc, fps, (firstF.shape[1], firstF.shape[0]))
        else:
            video_writer = cv2.VideoWriter(f"{currentTime}.avi", fourcc, fps, (firstF.shape[1], int(firstF.shape[0] * 2 )))
    while video1.isOpened():
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()

        if ret1 == False or ret2 == False:
            break

        #frame1 = cv2.resize(frame1, (1080,960))
        #frame2 = cv2.resize(frame2, (1080,960))
        
        if (typeConvert == "1"): ##### this is for combining two videos with 2:3 ratio
            scale_percent = 125 # percentage of original size
            width = int(frame1.shape[1] * scale_percent / 100)
            height = int(frame1.shape[0] * scale_percent / 100)
            dim = (width, height)

            # Resize the image
            resized = cv2.resize(frame1, dim, interpolation = cv2.INTER_AREA)

            # Crop the image to get the zoomed portion
            start_row, start_col = int((height - frame1.shape[0]) / 2), int((width - frame1.shape[1]) / 2)
            end_row, end_col = start_row + frame1.shape[0], start_col + frame1.shape[1]
            end_rowF = int((frame1.shape[0] * .67) + start_row)
            #print(img.shape[0])
            if (zoomOptions == "1"):
                zoomed = resized[start_row:end_rowF, start_col:end_col]
            if (zoomOptions == "0"):
                zoomed = resized[0:int(frame1.shape[0] * .67), start_col:end_col]
            if (zoomOptions == "2"):
                zoomed = resized[frame1.shape[0]-end_rowF:frame1.shape[0], start_col:end_col]
            #print(zoomed.shape[1])
            end_rowF2 = int(frame1.shape[0] * .33)
            #print(end_rowF2)
            frame2_width = frame2.shape[1]
            frame2_height = frame2.shape[0]  
            if (frame2.shape[1] != frame1.shape[1]):
                frame2_width = frame1.shape[1]
                frame2_height = frame1.shape[0]         
                frame2 = cv2.resize(frame2, (frame2_width, frame2_height), interpolation=cv2.INTER_AREA)
            
            roi_width = int(frame2_width / zoomFactor2)
            roi_height = int(frame2_height / zoomFactor2)

            x = (frame2_width - roi_width) // 2
            y = (frame2_height - roi_height) // 2

            if (zoomOptionsF2 == "1"):
                roi = frame2[y:y + end_rowF2, x:x + roi_width]
            if (zoomOptionsF2 == "0"):
                roi = frame2[0:end_rowF2, x:x+roi_width]
            if (zoomOptionsF2 == "2"):
                roi = frame2[end_rowF2*2:frame2.shape[0], x:x+roi_width]
            #frame2 = cv2.resize(frame2, (frame1.shape[1],end_rowF2))
            zoomed2 = cv2.resize(roi, (frame2_width, end_rowF2), interpolation=cv2.INTER_CUBIC)
            print(zoomed.shape[1])
            vid_comb = cv2.vconcat([zoomed, zoomed2])
            if vid_comb.shape[0] != frame1.shape[0]:
                vid_comb = cv2.resize(vid_comb, (frame1.shape[1], frame1.shape[0]))
            video_writer.write(vid_comb)
        else: ###### this portion is for combining two videos with even height and width
            frame1 = cv2.resize(frame1, (firstF.shape[1],firstF.shape[0]))
            frame2 = cv2.resize(frame2, (firstF.shape[1],firstF.shape[0]))
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
    if (movInclude == "1"): ##### TESTING
        video = VideoFileClip(f"final-{currentTime}.avi")
        video.write_videofile(f"final-{currentTime}.mov", codec='libx264', audio_codec='aac', fps=video.fps)
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
    meta_data = get_random_string()
    try:
        subprocess.run(["exiftool", f"-Title={meta_data}", "-overwrite_original", f"final-{currentTime}.avi"])
        print(f"Changed the meta data of the final-{currentTime}.avi \n Title: {meta_data}")
    except:
        print("Exif tool not installed.")
    time.sleep(2)
    shutil.move(f"final-{currentTime}.avi", f"{outputPathFile}")
    if movInclude == "1":
        shutil.move(f"final-{currentTime}.mov", f"{outputPathFile}") ##### TESTING
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

    
startVideoProcess(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
