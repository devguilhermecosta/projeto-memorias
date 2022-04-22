from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit
from PyQt5 import QtGui, QtCore


class AppMemorise(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Memories')
        self.setWindowIcon(QtGui.QIcon('note.ico'))
        self.setFixedSize(840, 640)
        self.cw = QWidget()
        self.grid = QGridLayout(self.cw)
        self.btn_open = QPushButton('Ler Nota')
        self.btn_search = QPushButton('Pesquisar')
        self.input_number = QLineEdit()
        self.input_search = QLineEdit()
        self.btn_add = QPushButton('Add Nota')
        self.input_title = QLineEdit()
        self.label_title = QLabel('Título da nova nota:')
        self.btn_clear = QPushButton('Limpar')
        self.btn_to_save = QPushButton('Salvar')
        self.btn_edit_note = QPushButton('Editar nota')
        self.label_edit_note = QLabel('Digite o número da nota que deseja editar:')
        self.input_edit_note = QLineEdit()
        self.label_search = QLabel('Tema da pesquisa:')
        self.label_open = QLabel('Digite o número da nota:')
        self.label_del_note = QLabel('Digite o número da nota para deletar:')
        self.input_del_note = QLineEdit()
        self.btn_del = QPushButton('Deletar')
        self.display = QTextEdit()
        self.btn_show_notes = QPushButton('Listar todas as notas')

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.display.setStyleSheet(
            'background: blue; color: white; size: 30px; font: 25px;'
            )
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_edit_note.setAlignment(QtCore.Qt.AlignCenter)
        self.label_search.setAlignment(QtCore.Qt.AlignCenter)
        self.label_open.setAlignment(QtCore.Qt.AlignCenter)
        self.label_del_note.setAlignment(QtCore.Qt.AlignCenter)

        self.label_title.setFont(font)
        self.label_edit_note.setFont(font)
        self.label_search.setFont(font)
        self.label_open.setFont(font)
        self.label_del_note.setFont(font)

        self.grid.addWidget(self.display, 0, 0, 5, 3)
        self.grid.addWidget(self.btn_open, 7, 2, 1, 1)
        self.grid.addWidget(self.input_number, 7, 1, 1, 1)
        self.grid.addWidget(self.label_open, 7, 0, 1, 1)
        self.grid.addWidget(self.input_search, 6, 1, 1, 1)
        self.grid.addWidget(self.label_search, 6, 0, 1, 1)
        self.grid.addWidget(self.btn_search, 6, 2, 1, 1)
        self.grid.addWidget(self.btn_add, 8, 2, 1, 1)
        self.grid.addWidget(self.input_title, 8, 1, 1, 1)
        self.grid.addWidget(self.label_title, 8, 0, 1, 1)
        self.grid.addWidget(self.btn_clear, 12, 2, 1, 1)
        self.grid.addWidget(self.label_edit_note, 9, 0, 1, 1)
        self.grid.addWidget(self.input_edit_note, 9, 1, 1, 1)
        self.grid.addWidget(self.btn_edit_note, 9, 2, 1, 1)
        self.grid.addWidget(self.btn_to_save, 10, 2, 1, 1)
        self.grid.addWidget(self.input_del_note, 11, 1, 1, 1)
        self.grid.addWidget(self.btn_del, 11, 2, 1, 1)
        self.grid.addWidget(self.label_del_note, 11, 0, 1, 1)
        self.grid.addWidget(self.btn_show_notes, 12, 0, 1, 1)

        # self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.btn_open.clicked.connect(self.open_file)
        self.btn_search.clicked.connect(self.search_note)
        self.btn_add.clicked.connect(self.add_note)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_edit_note.clicked.connect(self.edit_note)
        self.btn_to_save.setDisabled(True)
        self.btn_to_save.clicked.connect(self.to_save)
        self.btn_del.clicked.connect(self.del_note)
        self.btn_show_notes.clicked.connect(self.show_notes)

        self.setCentralWidget(self.cw)
