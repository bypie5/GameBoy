from PyQt6 import QtCore, QtWidgets

import game_boy.game_boy as game_boy
import sdl.sdl_audio as sdl_audio

class SoundTab(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.volume_slider = None
        self.saved_volume = 100
        self.mute_box = None
        self.muted = False

        self._init_ui()


    def _init_ui(self):
        main_layout = QtWidgets.QGridLayout()

        # Channels
        channels = QtWidgets.QGroupBox("Channels")
        channel_layout = QtWidgets.QVBoxLayout()

        for i in range(1, 5):
            widget = QtWidgets.QCheckBox(f"Channel {i}")
            widget.setChecked(True)
            widget.toggled.connect(self._toggle_sound_channel)
            channel_layout.addWidget(widget)

        channels.setLayout(channel_layout)
        main_layout.addWidget(channels, 0, 0)

        # Options
        options = QtWidgets.QGroupBox("Options")
        options_layout = QtWidgets.QVBoxLayout()

        self.mute_box = QtWidgets.QCheckBox("Mute")
        self.mute_box.clicked.connect(self._toggle_mute)
        options_layout.addWidget(self.mute_box)

        mono_audio_box = QtWidgets.QCheckBox("Mono output")
        mono_audio_box.toggled.connect(self._toggle_mono_audio)
        options_layout.addWidget(mono_audio_box)

        sample_rate_label = QtWidgets.QLabel("Sample Rate")
        sample_rate = QtWidgets.QComboBox()
        sample_rate.addItems(["8000", "11025", "22050", "24000", "44100", "48000"])
        sample_rate.setCurrentIndex(4)
        sample_rate.activated.connect(self._set_sample_rate)
        options_layout.addWidget(sample_rate_label)
        options_layout.addWidget(sample_rate)

        options.setLayout(options_layout)
        main_layout.addWidget(options, 0, 1)

        # Volume
        volume = QtWidgets.QGroupBox("Volume")
        volume_layout = QtWidgets.QVBoxLayout()
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.setPageStep(0)
        self.volume_slider.setValue(self.saved_volume)
        self.volume_slider.sliderReleased.connect(self._set_volume)
        volume_layout.addWidget(self.volume_slider)

        volume.setLayout(volume_layout)
        main_layout.addWidget(volume, 1, 0, 1, 2)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        main_layout.addWidget(spacer, 2, 0)

        self.setLayout(main_layout)


    def _toggle_sound_channel(self):
        channel = int(self.sender().text()[-1])
        enabled = self.sender().isChecked()

        game_boy.enable_sound_channel(channel, enabled)


    def _toggle_mute(self):
        if self.sender().isChecked():
            self.saved_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
            self.muted = True
            game_boy.set_volume(0.0)
        else:
            self.volume_slider.setValue(self.saved_volume)
            game_boy.set_volume(self.saved_volume / 100)


    def _toggle_mono_audio(self):
        game_boy.set_mono_audio(self.sender().isChecked())


    def _set_sample_rate(self):
        sample_rate = int(self.sender().currentText())
        game_boy.set_sample_rate(sample_rate)
        sdl_audio.update_sample_rate(sample_rate)


    def _set_volume(self):
        new_volume = self.sender().value()

        if self.muted and new_volume > 0:
            self.mute_box.setChecked(False)

        game_boy.set_volume(new_volume / 100)
