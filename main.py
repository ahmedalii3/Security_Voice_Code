import sys
from os import path

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUiType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import convolve2d

from recording import AudioRecorder
from voice import Voice

FORM_CLASS, _ = loadUiType(
    path.join(path.dirname(__file__), "main.ui")
)  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.handle_button()
        self.passwords = {
            "unlock_the_gate": [
                ["voice_data_base/ahmed_ali_unlock_the_gate.wav", "voice_data_base/ahmed_ali_unlock_the_gate_1.wav",
                 "voice_data_base/ahmed_ali_unlock_the_gate_2.wav", "voice_data_base/ahmed_ali_unlock_the_gate_3.wav",
                 "voice_data_base/bedro_unlock_the_gate.wav", "voice_data_base/bedro_unlock_the_gate_1.wav",
                 "voice_data_base/bedro_unlock_the_gate_2.wav", "voice_data_base/bedro_unlock_the_gate_3.wav",
                 "voice_data_base/hassan_unlock_the_gate.wav", "voice_data_base/hassan_unlock_the_gate_1.wav",
                 "voice_data_base/hassan_unlock_the_gate_2.wav", "voice_data_base/hassan_unlock_the_gate_3.wav"]
                # list of wav files stored in voice_data_base folder
                , None  # similarity factor
                , [None, None, None, None, None, None, None, None, None, None, None, None]  # instance
                , True  # Have access
            ],
            "open_middle_door": [
                ["voice_data_base/ahmed_ali_open_middle_door.wav", "voice_data_base/ahmed_ali_open_middle_door_1.wav",
                 "voice_data_base/ahmed_ali_open_middle_door_2.wav", "voice_data_base/ahmed_ali_open_middle_door_3.wav",
                 "voice_data_base/bedro_open_middle_door.wav", "voice_data_base/bedro_open_middle_door_1.wav",
                 "voice_data_base/bedro_open_middle_door_2.wav", "voice_data_base/bedro_open_middle_door_3.wav",
                 "voice_data_base/hassan_open_middle_door.wav", "voice_data_base/hassan_open_middle_door_1.wav",
                 "voice_data_base/hassan_open_middle_door_2.wav", "voice_data_base/hassan_open_middle_door_3.wav"]
                # list of wav files stored in voice_data_base folder
                , None  # similarity factor
                , [None, None, None, None, None, None, None, None, None, None, None, None]  # instance
                , True  # Have access
            ],
            "grant_me_access": [
                ["voice_data_base/ahmed_ali_grant_me_access.wav", "voice_data_base/bedro_grant_me_access.wav",
                 "voice_data_base/bedro_grant_me_access_1.wav", "voice_data_base/bedro_grant_me_access_2.wav",
                 "voice_data_base/bedro_grant_me_access_3.wav", "voice_data_base/ahmed_ali_grant_me_access_1.wav",
                 "voice_data_base/ahmed_ali_grant_me_access_2.wav", "voice_data_base/ahmed_ali_grant_me_access_3.wav",
                 "voice_data_base/hassan_grant_me_access.wav", "voice_data_base/hassan_grant_me_access_1.wav",
                 "voice_data_base/hassan_grant_me_access_2.wav", "voice_data_base/hassan_grant_me_access_3.wav"
                 ]
                # list of wav files stored in voice_data_base folder
                , None  # similarity factor
                , [None, None, None, None, None, None, None, None, None, None, None, None]  # instance
                , True  # Have access
            ],
        }
        # voice
        self.voice = {
            "ahmed_ali": [
                ["voice_data_base/ahmed_ali_unlock_the_gate.wav", "voice_data_base/ahmed_ali_unlock_the_gate_1.wav",
                 "voice_data_base/ahmed_ali_unlock_the_gate_2.wav", "voice_data_base/ahmed_ali_unlock_the_gate_3.wav",
                 "voice_data_base/ahmed_ali_open_middle_door.wav", "voice_data_base/ahmed_ali_open_middle_door_1.wav",
                 "voice_data_base/ahmed_ali_open_middle_door_2.wav", "voice_data_base/ahmed_ali_open_middle_door_3.wav",
                 "voice_data_base/ahmed_ali_grant_me_access.wav", "voice_data_base/ahmed_ali_grant_me_access_1.wav",
                 "voice_data_base/ahmed_ali_grant_me_access_2.wav", "voice_data_base/ahmed_ali_grant_me_access_3.wav"],
                None,  # similarity factor
                [None, None, None, None, None, None, None, None, None, None, None, None],
                True  # Have access
            ],
            "bedro": [["voice_data_base/bedro_unlock_the_gate.wav", "voice_data_base/bedro_unlock_the_gate_1.wav",
                       "voice_data_base/bedro_unlock_the_gate_2.wav", "voice_data_base/bedro_unlock_the_gate_3.wav",
                       "voice_data_base/bedro_open_middle_door.wav", "voice_data_base/bedro_open_middle_door_1.wav",
                       "voice_data_base/bedro_open_middle_door_2.wav", "voice_data_base/bedro_open_middle_door_3.wav",
                       "voice_data_base/bedro_grant_me_access.wav", "voice_data_base/bedro_grant_me_access_1.wav",
                       "voice_data_base/bedro_grant_me_access_2.wav", "voice_data_base/bedro_grant_me_access_3.wav"],
                      None,  # similarity factor
                      [None, None, None, None, None, None, None, None, None, None, None, None],
                      True  # Have access
                      ],

            # "muhannad":[["voice_data_base/muhannad_unlock_the_gate.wav" , "voice_data_base/muhannad_open_middle_door.wav" , "voice_data_base/muhannad_grant_me_access.wav"],
            # None, #similarity factor
            # [None,None,None]
            # ]

            "hassan": [["voice_data_base/hassan_unlock_the_gate.wav", "voice_data_base/hassan_unlock_the_gate_1.wav",
                        "voice_data_base/hassan_unlock_the_gate_2.wav", "voice_data_base/hassan_unlock_the_gate_3.wav",
                        "voice_data_base/hassan_open_middle_door.wav", "voice_data_base/hassan_open_middle_door_1.wav",
                        "voice_data_base/hassan_open_middle_door_2.wav",
                        "voice_data_base/hassan_open_middle_door_3.wav",
                        "voice_data_base/hassan_grant_me_access.wav", "voice_data_base/hassan_grant_me_access_1.wav",
                        "voice_data_base/hassan_grant_me_access_2.wav", "voice_data_base/hassan_grant_me_access_3.wav"],
                       None,  # similarity factor
                       [None, None, None, None, None, None, None, None, None, None, None, None],
                       True  # Have access
                       ]
        }

        self.create_password_audio_instance()  # create instance of each password

    def handle_button(self):
        self.pushButton.clicked.connect(self.start_recording)

    def create_password_audio_instance(self):
        for password in (self.passwords.keys()):
            for i in range(len(self.passwords[password][0])):
                self.passwords[password][2][i] = Voice(self.passwords[password][0][i])

        for voice in (self.voice.keys()):
            for i in range(len(self.voice[voice][0])):
                self.voice[voice][2][i] = Voice(self.voice[voice][0][i])

    def start_recording(self):
        print("Start Recording")
        if (self.pushButton.text() == "Start"):
            self.pushButton.setText("Stop")
            self.recorder = AudioRecorder()
            self.recorder.start_recording()
        else:
            self.pushButton.setText("Start")
            self.recorder.stop_recording()
            self.spectrogram(self.recorder.frames, 44100, self.widget)
            self.recorder.save_audio('trial.wav')
            test_voice = Voice('trial.wav')
            for voice in self.voice:
                self.voice[voice][1] = self.check_similarity(test_voice, self.voice[voice][2], voice, False)
            for password in self.passwords:
                self.passwords[password][1] = self.check_similarity(test_voice, self.passwords[password][2], password,
                                                                    True)
            max_similarity = 0
            max_voice = 0
            Access = ""
            for password in self.passwords:
                if self.passwords[password][1] > max_similarity:
                    max_similarity = self.passwords[password][1]
                    similar_word = password
            for voice in self.voice:
                if self.voice[voice][1] > max_voice:
                    max_voice = self.voice[voice][1]
                    similar_person = voice

            if max_similarity < 80 or self.passwords[similar_word][3] == False:
                Access = "Access Denied"
            else:
                Access = "Access Granted"
            if max_voice < 80 or self.voice[similar_person][3] == False:
                Access = "Access Denied"
            else:
                Access = "Access Granted"

            self.label.setText(similar_word)
            print(similar_person)

    def check_similarity(self, test_voice, password_voice, keyword, word=True):
        similarity_score = []
        correlation = []
        convulotion = []

        for i in range(len(password_voice)):
            if word:
                features1 = test_voice.get_stft()
                features2 = password_voice[i].get_stft()
            else:
                features1 = test_voice.extract_features()
                features2 = password_voice[i].extract_features()

            features1, features2 = self.match_signal_length(features1, features2)

            # similarity_score = np.linalg.norm(features1 - features2)
            similarity_score.append(
                np.mean(np.dot(features1.T, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))))
            # Compute Pearson correlation coefficient
            correlation.append(np.corrcoef(features1.flatten(), features2.flatten())[0, 1])
            # Compute convolution
            convulotion.append(convolve2d(features1, features2, mode='valid'))

        similarity_score = np.mean(similarity_score) * 10000
        correlation = np.mean(correlation) * 100
        convulotion = np.mean(convulotion)

        print(keyword)
        print('correlation', correlation)
        print("similarity_score", similarity_score)
        print("convulotion", convulotion)
        print("")

        return correlation

    def match_signal_length(self, signal1, signal2):
        len1, len2 = signal1.shape[1], signal2.shape[1]
        max_len = max(len1, len2)

        if len1 < max_len:
            signal1 = np.pad(signal1, ((0, 0), (0, max_len - len1)), 'constant')
        elif len2 < max_len:
            signal2 = np.pad(signal2, ((0, 0), (0, max_len - len2)), 'constant')

        return signal1, signal2

    def spectrogram(self, data, sampling_rate, widget):
        if widget.layout() is not None:
            widget.layout().deleteLater()

        data = np.frombuffer(b''.join(data), dtype=np.int16)
        # print(data)
        fig = Figure()
        fig = Figure(figsize=(2, 3))
        ax = fig.add_subplot(111)
        Sxx = ax.specgram(data, Fs=sampling_rate, cmap='plasma')
        # time_axis = np.linspace(0, len(data) / sampling_rate, num=Sxx.shape[1])

        # ax.imshow(10 * np.log10(Sxx), aspect='auto', cmap='viridis',extent=[time_axis[0], time_axis[-1], 0, sampling_rate / 2])
        ax.axes.plot()
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget.setLayout(layout)
        widget.show()


def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == "__main__":
    main()
