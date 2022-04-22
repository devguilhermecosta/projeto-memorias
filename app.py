from note.interface import AppMemorise
from sys import argv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
import sqlite3 as sq
from contextlib import contextmanager

# CRIA A BASE DE DADOS SE NÃO EXISTIR
primary_connection = sq.connect('base.db')
primary_cursor = primary_connection.cursor()

primary_cursor.execute('CREATE TABLE IF NOT EXISTS notes('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'title TEXT,'
                       'description TEXT'
                       ')')

primary_cursor.close()
primary_connection.close()


class Program(AppMemorise):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.description = ''

    # GERENCIADOR DE CONTEXTO PARA ABRIR E FECHAR E CONEXÃO COM A BASE DE DADOS
    @staticmethod
    @contextmanager
    def connect_base():
        connection = sq.connect('base.db')
        try:
            yield connection
        finally:
            connection.close()

    # ADICIONA DADOS NA BASE DE DADOS
    def add_note(self):
        self.btn_to_save.setDisabled(True)
        self.description = self.display.toPlainText()
        if not self.description:
            QMessageBox.about(self.cw, "Alerta", "Você não está escrevendo nada na descrição de sua nota.")
            return
        elif not self.input_title.text():
            QMessageBox.about(self.cw, "Alerta", "Sua nota está sem título.")
            return
        else:
            try:
                with self.connect_base() as connection:
                    cursor = connection.cursor()
                    cursor.execute('INSERT INTO notes (title, description) VALUES(?, ?)',
                                   (self.input_title.text(), self.description))
                    connection.commit()
                    QMessageBox.about(self.cw, "Alerta", "Nota adicionada com sucesso.")
                    self.clear()
                    cursor.close()
            except Exception as error:
                msg = f'Não foi possível criar a nota. Error: {error}'
                QMessageBox.about(self.cw, "Alerta", msg)

    # ABRE A BASE DE DADOS PARA LEITURA
    def open_file(self):
        self.btn_to_save.setDisabled(True)
        self.display.clear()

        try:
            if not self.input_number.text():
                QMessageBox.about(self.cw, "Alerta", "Digite um número de nota para abrir.")
                return
        except Exception as error:
            msg = f'Erro ao brir a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)

        try:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                cont = 0
                cursor.execute('SELECT * FROM notes')
                for line in cursor.fetchall():
                    identification, title, description = line
                    if self.input_number.text() in str(identification):
                        self.display.append(description)
                        msg = f'ID: {identification} - Título: {title}'
                        self.input_search.setText(msg)
                        cont += 1
                        cursor.close()
                if cont == 0:
                    msg = f'Não existe nota com "{self.input_number.text()}"'
                    QMessageBox.about(self.cw, "Alerta", msg)
        except Exception as error:
            msg = f'Erro ao abrir a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)

    # BUSCA INFORMAÇÕES NA BASE DE DADOS
    def search_note(self):
        self.btn_to_save.setDisabled(True)
        self.display.clear()

        try:
            if not self.input_search.text():
                QMessageBox.about(self.cw, "Alerta", "Digite algo para buscar.")
                return
        except Exception as error:
            QMessageBox.about(self.cw, "Alerta", "Erro:", error)

        try:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM notes')
                cont = 0
                for line in cursor.fetchall():
                    identification, title, description = line
                    if self.input_search.text() in title or self.input_search.text() in description:
                        self.display.append(str(identification) + '-' + title)
                        cont += 1
                    cursor.close()
                if cont == 0:
                    msg = f'Nenhuma nota encontra com "{self.input_search.text()}"'
                    QMessageBox.about(self.cw, "Alerta", msg)
                    self.clear()
                    return
        except Exception as error:
            QMessageBox.about(self.cw, "Alerta", 'Erro ao exibir as notas:', error)
            return

    # EDITA A BASE DE DADOS
    def edit_note(self):
        self.display.clear()
        QMessageBox.about(self.cw, "Alerta", "Clique no botão SALVAR após as alterações.")

        try:
            if not self.input_edit_note.text():
                QMessageBox.about(self.cw, "Alerta", "Digite um número de nota para editar.")
                return
        except Exception as error:
            msg = f'Erro ao brir a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)

        try:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                cont = 0
                cursor.execute('SELECT * FROM notes')
                for line in cursor.fetchall():
                    identification, title, description = line
                    if self.input_edit_note.text() in str(identification):
                        self.display.append(description)
                        self.input_title.setText(title)
                        self.btn_to_save.setDisabled(False)
                        cont += 1
                        cursor.close()
                if cont == 0:
                    msg = f'Não existe nota com "{self.input_edit_note.text()}"'
                    QMessageBox.about(self.cw, "Alerta", msg)
        except Exception as error:
            msg = f'Erro ao abrir a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)

    # SALVA AS INFORMAÇÕES EDITADAS
    def to_save(self):
        try:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                if not self.display.toPlainText():
                    QMessageBox.about(self.cw, "Alerta", "Você não pode salvar uma nota sem descrição.")
                    return
                elif not self.input_title.text():
                    QMessageBox.about(self.cw, "Alerta", "Você não pode salvar uma nota sem título.")
                    return
                else:
                    cursor.execute('UPDATE notes SET title=:title WHERE id=:id',
                                   {'title': f'{self.input_title.text()}',
                                    'id': f'{int(self.input_edit_note.text())}'}
                                   )

                    cursor.execute('UPDATE notes SET description=:description WHERE id=:id',
                                   {'description': f'{self.display.toPlainText()}',
                                    'id': f'{int(self.input_edit_note.text())}'}
                                   )
                    connection.commit()
                    cursor.close()

                QMessageBox.about(self.cw, "Alerta", "Nota salva com sucesso.")

                self.btn_to_save.setDisabled(True)

                self.clear()
        except Exception as error:
            msg = f'Erro ao salvar a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)
            print(error)

    # DELETA INFORMAÇÕES DA BASE DE DADOS
    def del_note(self):
        self.display.clear()
        if not self.input_del_note.text():
            QMessageBox.about(self.cw, "Alerta", "Digite um número de nota para deletar.")
            return

        try:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM notes')
                cont = 0
                for line in cursor.fetchall():
                    identification, title, description = line
                    if str(self.input_del_note.text()) in str(identification):
                        self.ask(int(self.input_del_note.text()))
                        cont += 1
                        cursor.close()
                if cont == 0:
                    QMessageBox.about(self.cw, "Alerta", f"Nota {self.input_del_note.text()} não existe.")
                    self.clear()
                    return
        except Exception as error:
            QMessageBox.about(self.cw, "Alerta", str(error))
            return

    # FUNÇÃO PARA ABRIR MESSAGEBOX DE SIM OU NÃO PARA DELETAR INFORMAÇÕES DA BASE DE DADOS
    def ask(self, num):
        response = QMessageBox
        ret = response.question(self.cw, "Alerta", f"Deseja realmente deletar a nota '{num}'?",
                                response.Yes | response.No)
        if ret == response.Yes:
            with self.connect_base() as connection:
                cursor = connection.cursor()
                num = self.input_del_note.text()
                cursor.execute('DELETE FROM notes WHERE id=:id',
                               {'id': f'{num}'},
                               )
                connection.commit()
                cursor.close()
                QMessageBox.about(self.cw, "Alerta", f"Nota {num} deletada com sucesso.")
                self.clear()
        elif ret == response.No:
            return

    def show_notes(self):
        try:
            with self.connect_base() as connection:
                cont = 0
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM notes')
                for line in cursor.fetchall():
                    identification, title, description = line
                    self.display.append(f'{identification} - {title}')
                    cont += 1
                QMessageBox.about(self.cw, "Total de notas", f"Total de notas encontradas: {cont}")
                cursor.close()
        except Exception as error:
            msg = f'Erro ao abrir a nota: {error}'
            QMessageBox.about(self.cw, "Alerta", msg)

    # LIMPA TODOS OS CAMPOS DO APP
    def clear(self):
        self.btn_to_save.setDisabled(True)
        self.display.clear()
        self.input_title.clear()
        self.input_search.clear()
        self.input_number.clear()
        self.input_edit_note.clear()
        self.input_del_note.clear()


if __name__ == '__main__':
    qt = QApplication(argv)
    testing = Program()
    testing.show()
    qt.exec_()
