#/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" && export PATH="/usr/local/opt/python/libexec/bin:$PATH" && brew install python && brew install openssl@1.1 && pip3 install PyQt5 opencv-python numpy pydub moviepy 
#https://drive.google.com/file/d/1ma5HBTPV2E7FkEfr79dxbI0g4zX_B4Mf/view?usp=share_link
#export CPPFLAGS="${CPPFLAGS} -I$(brew --prefix openssl)/include"
#export LDFLAGS="${LDFLAGS} -L$(brew --prefix openssl)/lib"
#https://drive.google.com/drive/u/0/folders/15nU34WeQUOgGaB-pGQqlee3UVlvz-sIX
#brew install openssl@1.1

import sys
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QListView, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaObject
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os
import cv2 
import numpy as np
from datetime import datetime
from pydub import AudioSegment
import glob
import time
from moviepy.editor import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Media Player")
        self.resize(1280, 800)

        # Create the list view
        self.list_view = QListView(self)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDragEnabled(True)
        self.list_view.setDefaultDropAction(Qt.MoveAction)
        self.list_view.setSelectionMode(QListView.SingleSelection)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setModel(QStandardItemModel())
        self.list_view.move(10, 60)
        self.list_view.resize(557, 513)

        # Create the media player
        self.media_player = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.videoWidget.setGeometry(0, 0, 100, 100)

        self.media_player2 = QMediaPlayer()
        self.videoWidget2 = QVideoWidget()
        self.videoWidget2.setGeometry(0, 0, 100, 100)

       # self.videoWidget.resize(492, 358)
        
        self.videoWidget.setVisible(True)
        self.videoWidget2.setVisible(True)

        self.addFileButton = QPushButton("Browse Files", self)
        self.addFileButton.resize(100, 32)
        self.addFileButton.move(480, 20)
        self.addFileButton.clicked.connect(self.addFilesToListBox)

        self.entryBox = QLineEdit("", self)
        self.entryBox.resize(459,30)
        self.entryBox.move(10, 20)

        # Connect signals
        self.list_view.doubleClicked.connect(self.play_media)

        self.playButton = QPushButton(">>", self)
        self.playButton.clicked.connect(self.resumeMedia)

        self.pauseButton = QPushButton("||", self)
        self.pauseButton.clicked.connect(self.pauseMedia)

        self.playButton2 = QPushButton(">>", self)
        self.playButton2.clicked.connect(self.resumeMedia2)

        self.pauseButton2 = QPushButton("||", self)
        self.pauseButton2.clicked.connect(self.pauseMedia2)

        self.convertButton = QPushButton("Convert", self)
        self.convertButton.clicked.connect(self.convertFunc)
        # Create the layout
        #layout = QHBoxLayout()
        layout = QGridLayout()
        layout.addWidget(self.entryBox, 0 , 0, 1, 3)
        layout.addWidget(self.convertButton, 0, 4)     
        layout.addWidget(self.addFileButton, 0, 3)
        layout.addWidget(self.list_view, 1,0, 6, 4)
        layout.addWidget(self.videoWidget, 1, 4, 2, 5)
        layout.addWidget(self.playButton, 3, 4, 1, 1)
        layout.addWidget(self.pauseButton, 3, 5, 1, 1)

        layout.addWidget(self.videoWidget2, 4, 4, 2, 5)   
        layout.addWidget(self.playButton2, 6, 4, 1, 1)
        layout.addWidget(self.pauseButton2, 6, 5, 1, 1)
        widgetWhat = QWidget(self)
        widgetWhat.setLayout(layout)
        self.setCentralWidget(widgetWhat)

    def resumeMedia(self):
        if (self.media_player != ""):
            self.media_player.play()
    def pauseMedia(self):
        if (self.media_player != ""):
            self.media_player.pause()
            print(self.media_player.currentMedia().canonicalUrl().toString().split(r"file:///")[1])

    def resumeMedia2(self):
        if (self.media_player2 != ""):
            self.media_player2.play()
    def pauseMedia2(self):
        if (self.media_player2 != ""):
            self.media_player2.pause()

    def addFilesToListBox(self):
        model = self.list_view.model()
        pathFiles = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        self.entryBox.setText(pathFiles)
        files_list = [os.path.join(pathFiles, file) for file in os.listdir(pathFiles)]
        for file_path in files_list:
            item = QStandardItem(file_path)
            model.appendRow(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        model = self.list_view.model()
        for url in event.mimeData().urls():
            item = QStandardItem(url.toLocalFile())
            model.appendRow(item)

    def play_media(self, index):
        item = self.list_view.model().itemFromIndex(index)
        reply = QMessageBox.question(self, 'Select Player', "Press 'Yes' for player 1. 'No' for player 2",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(item.text())))
            self.media_player.setVideoOutput(self.videoWidget)
            #self.videoWidget.show()
            self.media_player.play()
        else:
            self.media_player2.setMedia(QMediaContent(QUrl.fromLocalFile(item.text())))
            self.media_player2.setVideoOutput(self.videoWidget2)
            #self.videoWidget2.show()
            self.media_player2.play()

    def convertFunc(self):
        vid1path = self.media_player.currentMedia().canonicalUrl().toString().split(r"file:///")[1]
        vid2path = self.media_player2.currentMedia().canonicalUrl().toString().split(r"file:///")[1]
        self.media_player = QMediaPlayer()
        self.media_player2 = QMediaPlayer()
        video1 = cv2.VideoCapture(vid1path)
        video2 = cv2.VideoCapture(vid2path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        now = datetime.now()
        currentTime = now.strftime("%H-%M-%S")
        video_writer = cv2.VideoWriter(f"{currentTime}.mp4", fourcc, 30.0, (1080, 1920))

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

        finalVideo = VideoFileClip(f"{currentTime}.mp4")
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

        final_video.write_videofile(f"final-{currentTime}.mp4", codec='mpeg4')
        time.sleep(1)

        print("Cleaning Uncessary Files:")

        #animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
        animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

        for i in range(len(animation)):
            time.sleep(0.2)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()

        files = glob.glob('*.wav')
        os.remove(vid1path)
        print(f"{vid1path}: removed.")
        os.remove(vid2path)
        print(f"{vid2path}: removed.")
        os.remove(f"{currentTime}.mp4")
        print(f"{currentTime}.mp4: removed.")
        for file in files:
            print(f"{file}: removed.")
            os.remove(file)
        time.sleep(5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
