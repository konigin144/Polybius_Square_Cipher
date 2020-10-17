from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import re, os

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        #region Window and widgets
        #Window
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("Polybius Square Cipher")
        self.setWindowIcon(QIcon('Icons/key.png'))

        #Title
        titleText = QLabel()
        titleText.setText("Polybius Square Cipher")
        titleText.setAlignment(Qt.AlignHCenter)
        titleText.setFont(QFont('Lucida Console',30))

        titleButton = QPushButton()
        titleButton.setFixedSize(40,40)
        titleButton.setIcon(QIcon('Icons/info.png'))
        titleButton.clicked.connect(self.infoWindow)

        titleLayout = QHBoxLayout()
        titleLayout.addWidget(titleText)
        titleLayout.addWidget(titleButton)
        titleLayoutW = QWidget()
        titleLayoutW.setLayout(titleLayout)

        #Message and key
        self.messageField = QLineEdit()
        self.messageField.setPlaceholderText("Enter message here...")

        messageButton = QPushButton()
        messageButton.setFixedSize(40,40)
        messageButton.setIcon(QIcon('Icons/folder.png'))
        messageButton.clicked.connect(self.messageFileClicked)

        self.keyField = QLineEdit()
        self.keyField.setPlaceholderText("Enter key here...")

        keyButton = QPushButton()
        keyButton.setFixedSize(40,40)
        keyButton.setIcon(QIcon('Icons/folder.png'))
        keyButton.clicked.connect(self.keyFileClicked)

        textFieldsLayout = QHBoxLayout()
        textFieldsLayout.addWidget(self.messageField)
        textFieldsLayout.addWidget(messageButton)
        textFieldsLayout.addWidget(self.keyField)
        textFieldsLayout.addWidget(keyButton)
        textFieldsLayoutW = QWidget()
        textFieldsLayoutW.setLayout(textFieldsLayout)

        #Message and key from files
        self.messageFromFileButton = QFileDialog()
        self.messageFromFileButton.hide()

        self.keyFromFileButton = QFileDialog()
        self.keyFromFileButton.hide()

        #Buttons
        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT")
        encryptButton.setFont(QFont('Lucida Console',10))
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("DECRYPT")
        decryptButton.setFont(QFont('Lucida Console',10))
        decryptButton.clicked.connect(self.decryptClicked)

        self.matrixButton = QPushButton()
        self.matrixButton.setText("Show matrix")
        self.matrixButton.setFont(QFont('Lucida Console',10))
        self.matrixButton.clicked.connect(self.matrixWindow)
        self.matrixButton.setEnabled(False)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(encryptButton)
        buttonsLayout.addWidget(self.matrixButton)
        buttonsLayout.addWidget(decryptButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)

        #Output
        titleOutputText = QLabel()
        titleOutputText.setText("Output:")
        titleOutputText.setAlignment(Qt.AlignCenter)
        titleOutputText.setFont(QFont('Lucida Console',20))

        self.outputText = QLineEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setText("")
        self.outputText.setAlignment(Qt.AlignCenter)
        self.outputText.setFont(QFont('Lucida Console',16))

        self.saveButton = QPushButton()
        self.saveButton.setFixedSize(40,40)
        self.saveButton.setIcon(QIcon('Icons/save.png'))
        self.saveButton.clicked.connect(self.saveClicked)
        self.saveButton.setEnabled(False)

        outputLayout = QHBoxLayout()
        outputLayout.addWidget(titleOutputText)
        outputLayout.addWidget(self.outputText)
        outputLayout.addWidget(self.saveButton)
        outputLayoutW = QWidget()
        outputLayoutW.setLayout(outputLayout)

        #Main layout
        main = QVBoxLayout()
        main.setAlignment(Qt.AlignCenter)
        main.addWidget(titleLayoutW)
        main.addWidget(textFieldsLayoutW)
        main.addWidget(buttonsLayoutW)
        main.addWidget(outputLayoutW)

        mainW = QWidget()
        mainW.setLayout(main)

        self.setCentralWidget(mainW)
        #endregion

    def encryptClicked(self):
        """Handles encrypt button"""
        self.outputText.setText(encrypt(self.messageField.text(), self.keyField.text()))
        self.saveButton.setEnabled(True)
        self.matrixButton.setEnabled(True)

    def decryptClicked(self):
        """Handles decrypt button"""
        self.outputText.setText(decrypt(self.messageField.text(), self.keyField.text()))
        self.saveButton.setEnabled(True)
        self.matrixButton.setEnabled(True)

    def messageFileClicked(self):
        """Loads message from file"""
        self.keyFromFileButton.hide()
        self.messageFromFileButton.show()

        if self.messageFromFileButton.exec():
            files = self.messageFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.read()
                self.messageField.setText(data)

    def keyFileClicked(self):
        """Loads key from file"""
        self.messageFromFileButton.hide()
        self.keyFromFileButton.show()

        if self.keyFromFileButton.exec():
            files = self.keyFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.read()
                self.keyField.setText(data)

    def saveClicked(self):
        """Saves output to file"""
        filename = QFileDialog.getSaveFileName(self, "Open Text File", os.path.abspath(os.getcwd()), "Text Files (*.txt)")
        if filename[0] != '':
            f = open(filename[0], "w")
            f.write(self.outputText.text())
            f.close

    def infoWindow(self):
        """Opens info window"""
        infoW = QMessageBox()
        infoW.setWindowTitle("Polybius Square Cipher")
        infoW.setWindowIcon(QIcon('Icons/info.png'))
        f = open("info.txt", "r", encoding='utf8')
        text = f.read()
        infoW.setText(text)
        infoW.setWindowModality(Qt.ApplicationModal)
        infoW.exec_()

    def matrixWindow(self):
        """Shows matrix"""
        self.matrix = QTableWidget()
        self.matrix.setWindowTitle("Matrix")
        self.matrix.setRowCount(5)
        self.matrix.setColumnCount(5)
        key = self.keyField.text()
        key = key.upper()
        key = re.sub(r'J','I', key)
        key = unPolishText(key)
        key = re.sub('[^A-Z]','', key)
        arr = generate_array(key)
        for i in range(5):
            for j in range(5):
                self.matrix.setItem(i,j, QTableWidgetItem(arr[i][j]))
        self.matrix.resizeColumnsToContents()
        self.matrix.resizeRowsToContents()
        self.matrix.show()

def unPolishText(text):
    """Converts Polish letters to Latin"""
    polish = "ĄĆĘŁŃÓŚŹŻ"
    normal = "ACELNOSZZ"
    table = text.maketrans(polish, normal)
    return text.translate(table)


def generate_array(key=''):
    """Generates Polybius square"""
    abc = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    arr_el=[]
    arr = []
    row = []
    if key:
        for char in key:
            if char not in arr_el:
                arr_el.append(char)
        for char in abc:
            if char not in arr_el:
                arr_el.append(char)
    else:
        arr_el = abc
    for i in range(5):
        for j in range(5):
            row.append(arr_el[i*5 + j])
        arr.append(row)
        row = []
    return arr
        
def encrypt(word, key=''):
    """Encrypts message"""
    word = word.upper()
    key = key.upper()
    word = re.sub(r'J','I', word)
    key = re.sub(r'J','I', key)
    word = unPolishText(word)
    key = unPolishText(key)
    word = re.sub('[^A-Z]','', word)
    key = re.sub('[^A-Z]','', key)
    arr = generate_array(key)
    output = ''
    for char in word:
        for i in range(5):
            for j in range(5):
                if char is arr[i][j]:
                    output+=str(j+1)
                    output+=str(i+1)
    return output

def decrypt(word, key=''):
    """Decrypts message"""
    word = word.upper()
    key = key.upper()
    key = re.sub(r'J','I', key)
    key = unPolishText(key)
    key = re.sub('[^A-Z]','', key)
    arr = generate_array(key)
    output = ''
    for i in range(int(len(word)/2)):
        col = int(word[i*2])
        row = int(word[i*2+1])
        letter = arr[row-1][col-1]
        output+=str(letter)
    return output

#App and window initialization
app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(600, 400)
window.setStyleSheet("background-color: rgb(220,220,220);")
window.show()

app.exec_()