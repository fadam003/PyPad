import os
import sys
import uuid

from PyQt5.QtWidgets import QWidget, QFileDialog, QPlainTextEdit, QGridLayout


from pypad import config, dialog, numbers, window


class Editor(QWidget):

    def __init__(self, path: str=''):
        super().__init__()

        self.layout = QGridLayout(self)

        self.editor = QPlainTextEdit()
        self.editor.setFont(config.config.font)
        self.editor.setTabStopWidth(config.config['editor']['tabWidth'])

        self.path = path

        if path:
            self.open_file()
        else:
            self.new_file()

        self.line_numbers = numbers.NumberBar(self.editor)

        self.layout.addWidget(self.line_numbers, 0, 0)
        self.layout.addWidget(self.editor, 0, 1)

    def get_name(self):
        return os.path.basename(self.path)

    def new_file(self):
        temp = '/tmp'
        if sys.platform == 'win32':
            temp = os.getenv('temp') or ''

        if not os.path.exists(temp):
            dialog.FatalError("Couldn't find your config directory")

        path = os.path.join(temp, 'pypad-' + str(uuid.uuid4()).split('-')[0] + '.txt')

        try:
            open(path, 'a').close()
        except PermissionError:
            dialog.FatalError("Couldn't write to", path)

        self.path = path
        self.editor.setPlainText('')

    def open_file(self):
        with open(self.path, 'r') as file:
            text = file.read()
        self.editor.setPlainText(text)

    def save(self):
        try:
            with open(self.path, 'w') as file:
                file.write(self.editor.toPlainText())
        except PermissionError:
            dialog.Error("Couldn't write to", self.path)

    def save_as(self):
        options = QFileDialog.Options()
        paths = QFileDialog.getSaveFileName(self, 'Save File', '',
                                            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                            options=options)
        self.path = paths[0]
        window.main_window.set_filename(self.path)
        self.save()