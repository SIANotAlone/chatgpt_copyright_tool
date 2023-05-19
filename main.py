import os
import openai
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import sys
from threading import Thread
import time

openai.api_key = "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"

class WorkerThread(QThread):
    progressChanged = pyqtSignal(int)  # Сигнал для передачі відсотка прогресу
    gpt_list = None
    answer = ''
    def run(self):
        
        count = len(self.gpt_list)
        print(f'Paragraph count: {count}')

        
        for index, value in enumerate(self.gpt_list):
          
          response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Перефразуй текст: {value}',
            temperature=1,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
          )
          self.answer += response['choices'][0]['text'] 
          self.progressChanged.emit(index+1)
        #print(self.answer)
          



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.show()
        self.pb.setVisible(False)

        
        self.send.clicked.connect(self.startProcessing)
    def startProcessing(self):
        #self.pb.setMaximum(101)
        self.pb.setVisible(True)
        
        gpt_list = self.text.toPlainText().split('*****')
        self.pb.setMaximum(len(gpt_list))
        self.thread = WorkerThread()
        self.thread.gpt_list = gpt_list
        self.thread.progressChanged.connect(self.updateProgress)
        self.thread.finished.connect(self.processingFinished)
        self.thread.start()
        self.send.setEnabled(False)


    def updateProgress(self, value):
        self.pb.setValue(value)
        print(f'Current paragraph {value} is processing')

    def processingFinished(self):
        print('finished')
        self.text.setPlainText(self.thread.answer)
        self.send.setEnabled(True)


    # def worker(self):
    #     gpt_list = self.text.toPlainText().split('*****')
    #     count = len(gpt_list)
    #     print(f'Paragraph count: {count}')
    #     self.pb.setVisible(True)
    #     self.pb.setMaximum(count)
        
    #     self.pb.setValue(0)
    #     answer = ''
    #     for index, value in enumerate(gpt_list):
          
    #       response = openai.Completion.create(
    #         model="text-davinci-003",
    #         prompt=f'Перефразуй текст: {value}',
    #         temperature=1,
    #         max_tokens=1024,
    #         top_p=1.0,
    #         frequency_penalty=0.0,
    #         presence_penalty=0.0
    #       )
    #       answer += response['choices'][0]['text'] 
    #       self.pb.setValue(index)
        

    def send_click(self):

        t = Thread(target=self.worker)
        t.run()
      
    
   

    
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

