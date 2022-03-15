"""
Widgets that build the interface
Core is for Signals and slots
GUI is Color and font classes etc.
"""
import sys, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# scales the UI to different screen resolutions
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class EditSecret(qtw.QWidget):

    submitted = qtc.pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        print(message)
        self.edit_secret = qtw.QLineEdit(message)
        self.cancel_button = qtw.QPushButton("Cancel")
        self.submit_button = qtw.QPushButton("Save")

        layout = qtw.QFormLayout()
        layout.addRow("Edit Message", self.edit_secret)

        cta_row = qtw.QHBoxLayout()
        cta_row.addWidget(self.cancel_button)
        cta_row.addWidget(self.submit_button)

        layout.addRow(cta_row)

        self.cancel_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self.on_submit)

        self.setLayout(layout)
        self.show()

    def on_submit(self):
        self.submitted.emit(self.edit_secret.text())
        self.close()

class Profile(qtw.QWidget):

    def __init__(self, username):
        super().__init__()

        self.message = qtw.QLabel(f"Hello {username}!")
        self.secretMsgLabel = qtw.QLabel("Your Secret Message is:")
        self.secretMsg = qtw.QLabel("Green Pigeons")
        self.edit_button = qtw.QPushButton("Edit Secret Message")

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.secretMsgLabel)
        layout.addWidget(self.secretMsg)
        layout.addWidget(self.edit_button)

        self.edit_button.clicked.connect(self.edit_sm)

        self.setLayout(layout)
        self.show()

    @qtc.pyqtSlot(str)
    def update_secret(self, msg):
        self.secretMsg.setText(msg)

    def edit_sm(self):
        message = self.secretMsg.text()
        self.edited_message = EditSecret(message)
        self.edited_message.submitted.connect(self.update_secret)

class MainWindow(qtw.QWidget):

    authenticated = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Code will go here
        self.username_input = qtw.QLineEdit()
        self.password_input = qtw.QLineEdit()
        self.password_input.setEchoMode(qtw.QLineEdit.Password)

        self.cancel_button = qtw.QPushButton("Cancel")
        self.login_button = qtw.QPushButton("Login")

        '''
        Create a layout by stacking widgets
        1. QtWidgets.QGridLayout() Allows for grid and row/column input as integers
        |--layout.addWidget(password_input, row=0, column=1)
        2. QtWidgets.QHBoxLayout() Layout elements horizontally
        3. QtWidgets.QVBoxLayout() Layout elements vertically
        4. QtWidgets.QFormLayout() Layout for forms with label, will adjust by OS
        '''
        layout = qtw.QFormLayout()
        layout.addRow('Username', self.username_input)
        layout.addRow('Password', self.password_input)

        cta_widget = qtw.QHBoxLayout()
        cta_widget.addWidget(self.cancel_button)
        cta_widget.addWidget(self.login_button)
        layout.addRow(cta_widget)

        # signal is the action that can be taken
        # slot is the method, in this instance 'self.close'
        self.cancel_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.authenticate)

        self.username_input.textChanged.connect(self.set_button_text)
        self.authenticated.connect(self.user_logged_in)

        self.setLayout(layout)
        # Code will end here
        self.show()

    # declare slot to only take in str
    # ensures the right datatype is sent.
    @qtc.pyqtSlot(str)
    def set_button_text(self, text):
        if text:
            self.login_button.setText(f"Login as {text}")
        else:
            self.login_button.setText("Login")

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "user" and password == "password":
            self.authenticated.emit(username)
        else:
            qtw.QMessageBox.critical(self, "Failed", "Failed to login")

    def user_logged_in(self, username):
        self.auth = Profile(username)
        self.close()

# Only run this code if this is the script I specifically ran
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    # add underscore because exec is another keyword
    sys.exit(app.exec_())