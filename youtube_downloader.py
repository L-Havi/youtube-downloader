import os
import sys
import threading

from PyQt5 import QtWidgets, QtGui
from pytube import YouTube


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QFormLayout()

        self.setGeometry(0, 0, 300, 100)
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QtGui.QIcon("youtube.ico"))

        self.link_label = QtWidgets.QLabel("Link:")
        self.link_input = QtWidgets.QLineEdit()
        self.folder_label = QtWidgets.QLabel("Folder:")
        self.folder_input = QtWidgets.QLineEdit()
        self.folder_button = QtWidgets.QPushButton("Choose Folder")
        self.folder_button.clicked.connect(self.choose_folder)
        self.format_label = QtWidgets.QLabel("Format:")
        self.format_input = QtWidgets.QComboBox()
        self.format_input.addItems(["MP3", "MP4"])
        self.download_button = QtWidgets.QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        self.error_label = QtWidgets.QLabel("")

        layout.addRow(self.link_label, self.link_input)
        layout.addRow(self.folder_label, self.folder_input)
        layout.addRow(self.format_label, self.format_input)
        layout.addRow(self.folder_button)
        layout.addRow(self.download_button)
        layout.addRow(self.error_label)

        self.setLayout(layout)

        self.error_label = QtWidgets.QLabel("")
        layout.addRow(self.error_label)

    def choose_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Save Folder")
        self.folder_input.setText(folder)

    def download(self):
        link = self.link_input.text()
        folder = self.folder_input.text()
        output_format = self.format_input.currentText()

        try:
            yt = YouTube(link)
        except Exception as e:
            self.error_label.setText("Error: Invalid link")
            return

        try:
            os.chdir(folder)
        except Exception as e:
            self.error_label.setText("Error: Invalid folder")
            return

        def download_thread():
            try:
                if output_format == "MP4":
                    mp4files = yt.streams.filter(file_extension='mp4', progressive=True)
                    stream = mp4files[-1]
                elif output_format == "MP3":
                    stream = yt.streams.filter(only_audio=True).first()
                else:
                    self.error_label.setText("Error: Invalid output format")
                    return

                stream.download(output_path=folder)
                self.error_label.setText("Download completed successfully")
            except Exception as e:
                self.error_label.setText(f"Error: {str(e)}")

        download_thread = threading.Thread(target=download_thread)
        download_thread.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


while(True):
    main()
