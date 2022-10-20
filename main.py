# by ['João Pedro', 'Percival']
# Harley Davidson error codes hardcoded from https://www.uti.edu/blog/motorcycle/trouble-codes
# Harley Davidson logos are trademarks from Harley Davidson Company
#
# me.dividesbyzero@gmail.com
#

from datetime import datetime
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QFileDialog
import sys, os
from erros import lista_erros
from siglas import lista_siglas
import images
from winsound import Beep
from time import sleep


resumo = {}

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()        
        uic.loadUi('window.ui', self) 
        self.show()                        
        self.about = about()
        
        self.submit_code.clicked.connect(self.show_line1) 
        self.submit_code.clicked.connect(self.resumao)
        #self.submit_code.clicked.connect(self.resumao)
        
        self.save_log.clicked.connect(self.save_txt)


        
        self.about_btn.clicked.connect(self.about.show)
        self.about_btn.clicked.connect(self.bipe)
        
        


        # code_input line edit
        self.code_input.setStyleSheet('background-color: rgb(50,50,50); border-radius:10px; color: rgb(201,52,19); font-size:24px; font-weight: bold; text-align: center')

    
    def show_line1(self):        
        cod = str(self.code_input.text()).strip().upper()
        self.code_input.clear()
        self.system_output.clear()
        
        if cod in lista_erros:            
                self.error_output.setText(f'\nERROR CODE {cod}\n {lista_erros[cod]}\n')
                Beep(900,200)
                resumo.update({cod: lista_erros[cod]})              
        else:
            Beep(400,400)

        try:
                for a in lista_siglas:
                        if a in lista_erros[cod]:
                                self.system_output.setText(f'{lista_siglas[a]}')
                        #else:
                        #        self.system_output.setText('GENERIC')
        except KeyError:
                self.error_output.setText(f'Error code {cod} not found.')
        
       
    def resumao(self):
        self.log_area.clear()
        date = datetime.today().strftime('%d-%d-%Y')
        self.log_area.addItem(f'DATE:  {date}')
        self.log_area.addItem('ERROR CODE            DESCRIPTION')
        self.log_area.addItem('¨' * 83)
        for k, v in resumo.items():
                date = datetime.today().strftime('%d-%d-%Y')
                self.log_area.addItem(f'{k}                       {v}')

    def save_txt(self):
        file = str(QFileDialog.getExistingDirectory(self, "Choose where to save log"))                
        
        list_widget = self.log_area
        entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
        with open(f'{file}/HD_ERROR_LOG.txt', 'w') as lista:
                lista.write(entries)

    def bipe(self):
        Beep(100,300)

class about(QtWidgets.QMainWindow):
    def __init__(self):
        super(about, self).__init__()        
        uic.loadUi('about.ui', self)

        self.setWindowIcon(QtGui.QIcon('window_logo.png'))
        
        

app = QtWidgets.QApplication(sys.argv)     # Create an instance of QtWidgets.QApplication
window = Ui()                              # Create an instance of our class
app.exec_()                                # Start the application