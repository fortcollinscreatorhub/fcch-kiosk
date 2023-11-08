#!/usr/bin/env python3

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

import argparse
from dataclasses import dataclass
import errno
import fcchkiosk
import os
import subprocess
import sys
import threading
import time
import traceback
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt, QRect, QTimer, QUrl, pyqtSignal
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QLabel, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

TIME_URL_ERROR = 10000
TIME_DEBUG_UPDATE = 5000
TIME_INITIAL_DEBUG = 60

@dataclass
class UrlInfo:
    url: str
    time: int

class KioskWindow(QWidget):
    sigDebugOn = pyqtSignal()
    sigDebugOff = pyqtSignal()
    sigReloadConfig = pyqtSignal()
    sigNextURL = pyqtSignal()
    sigPrevURL = pyqtSignal()

    def __init__(self, urlsPath):
        super().__init__()
        self.urlsPath = urlsPath
        self.initUI()
        self.initTimers()
        self.initURLs()
        self.initDebug()
        self.displayCurrentURL()
        self.initSignals()

    def initUI(self):
        self.webEngineView = QWebEngineView()
        self.statusText = QLabel('Status')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.webEngineView, stretch=True)
        self.layout.addWidget(self.statusText)

        with open('/sys/class/graphics/fbcon/rotate', 'rt') as f:
            fbrotate = f.read()
            rotate = 90 * int(fbrotate)

        if rotate == 0:
            self.w = None
            self.topLayout = self.layout
        else:
            self.w = QWidget()
            self.w.setLayout(self.layout)

            self.scene = QGraphicsScene()
            self.scene.addWidget(self.w)

            self.view = QGraphicsView()
            self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.view.setScene(self.scene)
            self.view.rotate(rotate)

            self.topLayout = QVBoxLayout()
            self.topLayout.setContentsMargins(0, 0, 0, 0)
            self.topLayout.addWidget(self.view, stretch=True)

        self.setLayout(self.topLayout)
        self.setCursor(Qt.CursorShape.BlankCursor)

        screenGeom = QGuiApplication.primaryScreen().geometry()
        print('screenGeom', screenGeom, file=sys.stderr)
        if self.w is not None:
            if rotate in (90, 270):
                w = screenGeom.width()
                h = screenGeom.height()
                (w, h) = (h, w)
                screenGeom.setWidth(w)
                screenGeom.setHeight(h)
            self.w.setGeometry(screenGeom)
        self.setGeometry(screenGeom)

    def initTimers(self):
        self.timerUrl = QTimer()
        self.timerUrl.timeout.connect(self.onTimerUrl)
        self.timerDebug = QTimer()
        self.timerDebug.timeout.connect(self.onTimerDebug)

    def initDebug(self):
        self.isInitialDebug = True
        self.initialDebugClearAt = 0
        self.isDebugOn = False
        self.setDebugOn()

    def initURLs(self):
        self.urls = []
        self.urlIndex = 0
        self.loadURLs()

    def initSignals(self):
        self.sigDebugOn.connect(self.onDebugOn)
        self.sigDebugOff.connect(self.onDebugOff)
        self.sigReloadConfig.connect(self.onReloadConfig)
        self.sigNextURL.connect(self.onNextURL)
        self.sigPrevURL.connect(self.onPrevURL)

    def onTimerUrl(self):
        self.nextUrl()

    def onTimerDebug(self):
        if self.isInitialDebug and self.initialDebugClearAt != 0 and time.time() >= self.initialDebugClearAt:
            self.isInitialDebug = False
            self.setDebugOff()
        else:
            self.updateDebugText()

    def onDebugOn(self):
        self.isInitialDebug = False
        self.setDebugOn()

    def onDebugOff(self):
        self.isInitialDebug = False
        self.setDebugOff()

    def onReloadConfig(self):
        try:
            self.loadURLs()
        except:
            traceback.print_exc(file=sys.stderr)
            self.urls = [
                UrlInfo('https://error-loading-config-file.kiosk-error.local/', TIME_URL_ERROR),
            ]
        self.displayCurrentURL()

    def onNextURL(self):
        self.nextUrl()

    def onPrevURL(self):
        self.prevUrl()

    def prevUrl(self):
        self.urlIndex -= 1
        self.urlIndex %= len(self.urls)
        self.displayCurrentURL()

    def nextUrl(self):
        self.urlIndex += 1
        self.urlIndex %= len(self.urls)
        self.displayCurrentURL()

    def setDebugOn(self):
        if self.isDebugOn:
            return
        self.isDebugOn = True
        self.updateDebugText()
        self.statusText.setVisible(True)
        self.timerDebug.start(TIME_DEBUG_UPDATE)

    def updateDebugText(self):
        hasIp, text = fcchkiosk.getStatusText()
        if hasIp:
            if self.initialDebugClearAt == 0:
                self.initialDebugClearAt = time.time() + TIME_INITIAL_DEBUG
                # FIXME: Perhaps keep the timer running always, and do this
                # any time the IP changes?
                self.displayCurrentURL()
        self.statusText.setText(text)

    def setDebugOff(self):
        if not self.isDebugOn:
            return
        self.timerDebug.stop()
        self.isDebugOn = False
        self.statusText.setVisible(False)

    def loadURLs(self):
        if self.urls:
            curURL = self.urls[self.urlIndex].url
        else:
            curURL = None

        self.urls = []
        with open(self.urlsPath) as urlFile:
            lineNum = 0
            for line in urlFile:
                lineNum += 1
                line = line.strip()
                if not line:
                    continue
                try:
                    urlTimeS, url = line.split(' ', maxsplit=1)
                    urlTime = int(urlTimeS) * 1000
                except:
                    traceback.print_exc(file=sys.stderr)
                    urlTime = TIME_URL_ERROR
                    url = f'https://config-file-line-{lineNum}-error.kiosk-error.local/'
                self.urls.append(UrlInfo(url, urlTime))
        if not self.urls:
            self.urls.append(UrlInfo('https://empty-config-file.kiosk-error.local/', TIME_URL_ERROR))

        self.urlIndex = None
        if curURL is not None:
            matches = [index for (index, urlInfo) in enumerate(self.urls) if urlInfo.url == curURL]
            if matches:
                self.urlIndex = matches[0]
        if self.urlIndex is None:
            self.urlIndex = 0

    def displayCurrentURL(self):
        self.timerUrl.stop()
        urlInfo = self.urls[self.urlIndex]
        url = urlInfo.url
        urlTime = urlInfo.time
        self.webEngineView.setUrl(QUrl.fromUserInput(url))
        self.timerUrl.start(urlTime)

class KioskApiThread():
    def __init__(self, pipePath, window):
        self.pipePath = pipePath
        self.window = window
        try:
            os.mkfifo(self.pipePath)
        except OSError as oe: 
            if oe.errno != errno.EEXIST:
                raise

        self.thread = threading.Thread(target=self.threadFunc)

    def start(self):
        self.thread.start()

    def threadFunc(self):
        while True:
            try:
                with open(self.pipePath) as fifo:
                    while True:
                        data = fifo.read(1)
                        if len(data) == 0:
                            break
                        if data == 'D':
                            self.window.sigDebugOn.emit()
                        if data == 'd':
                            self.window.sigDebugOff.emit()
                        elif data == 'N':
                            self.window.sigNextURL.emit()
                        elif data == 'P':
                            self.window.sigPrevURL.emit()
                        elif data == 'R':
                            self.window.sigReloadConfig.emit()
                        elif data == 'Q':
                            os._exit(0)
            except:
                traceback.print_exc(file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='Display a series of web pages in kiosk mode')
    parser.add_argument('--urls-file', required=True)
    parser.add_argument('--control-pipe', required=True)
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = KioskWindow(args.urls_file)
    window.show()
    api = KioskApiThread(args.control_pipe, window)
    api.start()
    app.exec()

if __name__ == '__main__':
    main()
