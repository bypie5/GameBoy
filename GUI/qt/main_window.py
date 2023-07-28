import game_boy.game_boy as game_boy
import sdl.sdl_audio as sdl_audio
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets

WIDTH = 160
HEIGHT = 144

class MainWindow(QtWidgets.QMainWindow):
    window_sizes = {"2x2": 2, "3x3": 3, "4x4": 4, "5x5": 5, "6x6": 6}
    game_speeds = {"x1/4": 0.25, "x1/2": 0.5, "x1": 1.0, "x2": 2.0, "x3": 3.0, "x4": 4.0}

    def __init__(self, audio_device_id: int, file_dialog_path: Path):
        super().__init__()
        self.window_scale = 4
        self.game_speed = 1.0
        self.audio_device_id = audio_device_id
        self.file_dialog_path = file_dialog_path
        self.keys_pressed = set()

        self.last_checked_window_size: QtGui.QAction = None
        self.last_checked_game_speed: QtGui.QAction = None

        self.frame_counter = 0
        self.fps_timer = QtCore.QTimer(self)
        self.fps_timer.timeout.connect(self._update_fps_counter)
        self.fps_timer.start(1000)

        self._init_ui()
        self.show()

    def _init_ui(self):
        # Set window settings
        self.setWindowTitle("Game Boy (0 fps)")
        self.setContentsMargins(0, 0, 0, 0)

        # Create menu bar
        file = self.menuBar().addMenu("File")
        emulation = self.menuBar().addMenu("Emulation")
        options = self.menuBar().addMenu("Options")
        debug = self.menuBar().addMenu("Debug")

        # File menu
        file_loadrom_action = QtGui.QAction("Load ROM...", self)
        file_loadrom_action.triggered.connect(self._load_rom_trigger)
        file_loadrom = file.addAction(file_loadrom_action)

        file_exit_action = QtGui.QAction("Exit", self)
        file_exit_action.triggered.connect(QtWidgets.QApplication.quit)
        file_exit = file.addAction(file_exit_action)

        # Emulation menu
        emulation_pause_action = QtGui.QAction("Pause", self)
        emulation_pause_action.triggered.connect(self._pause_emulation_trigger)
        emulation_pause_action.setCheckable(True)
        emulation_pause = emulation.addAction(emulation_pause_action)

        emulation_gamespeed = emulation.addMenu("Game speed")

        for speed_str, speed_float in self.game_speeds.items():
            action = QtGui.QAction(speed_str, self)
            action.setCheckable(True)

            if speed_float == self.game_speed:
                action.setChecked(True)
                self.last_checked_game_speed = action

            action.triggered.connect(self._game_speed_trigger)
            emulation_gamespeed.addAction(action)

        emulation.addSeparator()

        emulation_savestate = emulation.addMenu("Save state")
        emulation_loadstate = emulation.addMenu("Load state")

        emulation.addSeparator()

        emulation_reset_action = QtGui.QAction("Restart", self)
        emulation_reset_action.triggered.connect(self._reset_trigger)
        emulation.addAction(emulation_reset_action)

        # Options menu
        options_windowsize = options.addMenu("Window size")

        for size_str, size_int in self.window_sizes.items():
            action = QtGui.QAction(size_str, self)
            action.setCheckable(True)

            if size_int == self.window_scale:
                action.setChecked(True)
                self.last_checked_window_size = action

            action.triggered.connect(self._window_size_trigger)
            options_windowsize.addAction(action)

        # Debug menu
        debug_sound_channels = debug.addMenu("Sound channels")

        # Create LCD output label
        self.lcd = QtWidgets.QLabel(self)
        self.setCentralWidget(self.lcd)

        # Update window size
        self._resize_window()

    def _resize_window(self):
        width = WIDTH * self.window_scale
        lcd_height = HEIGHT * self.window_scale
        window_height = self.menuBar().height() + lcd_height
        self.setFixedSize(width, window_height)
        self.lcd.resize(width, lcd_height)

    def _update_fps_counter(self):
        self.setWindowTitle(f"Game Boy ({self.frame_counter} fps)")
        self.frame_counter = 0

    def refresh_screen(self):
        self.frame_counter += 1
        self._update_joypad()

        image = QtGui.QImage(game_boy.get_frame_buffer(),
                             WIDTH,
                             HEIGHT,
                             QtGui.QImage.Format.Format_RGB888)

        self.lcd.setPixmap(QtGui.QPixmap.fromImage(image).scaled(self.lcd.width(), self.lcd.height()))

    def _update_joypad(self):
        joypad = game_boy.JoyPad(
            QtCore.Qt.Key.Key_S in self.keys_pressed,
            QtCore.Qt.Key.Key_W in self.keys_pressed,
            QtCore.Qt.Key.Key_A in self.keys_pressed,
            QtCore.Qt.Key.Key_D in self.keys_pressed,
            QtCore.Qt.Key.Key_Return in self.keys_pressed,
            QtCore.Qt.Key.Key_Shift in self.keys_pressed,
            QtCore.Qt.Key.Key_K in self.keys_pressed,
            QtCore.Qt.Key.Key_L in self.keys_pressed,
        )
        game_boy.set_joypad_state(joypad)


    #######################################################################
    #    __  __                                 _   _                     #
    #   |  \/  |                      /\       | | (_)                    #
    #   | \  / | ___ _ __  _   _     /  \   ___| |_ _  ___  _ __  ___     #
    #   | |\/| |/ _ \ '_ \| | | |   / /\ \ / __| __| |/ _ \| '_ \/ __|    #
    #   | |  | |  __/ | | | |_| |  / ____ \ (__| |_| | (_) | | | \__ \    #
    #   |_|  |_|\___|_| |_|\__,_| /_/    \_\___|\__|_|\___/|_| |_|___/    #
    #                                                                     #
    #######################################################################

    def _load_rom_trigger(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        rom_path, _ = file_dialog.getOpenFileName(self,
                                                  "Load ROM...",
                                                  str(self.file_dialog_path.absolute()),
                                                  "Game Boy files (*.gb *.gbc)")

        if rom_path:
            sdl_audio.lock_audio(self.audio_device_id)
            game_boy.insert_cartridge(rom_path)
            game_boy.power_on()
            sdl_audio.unlock_audio(self.audio_device_id)

    def _pause_emulation_trigger(self):
        if self.sender().isChecked():
            sdl_audio.lock_audio(self.audio_device_id)
        else:
            sdl_audio.unlock_audio(self.audio_device_id)

    def _reset_trigger(self):
        game_boy.power_on()

    def _window_size_trigger(self):
        self.last_checked_window_size.setChecked(False)
        self.last_checked_window_size = self.sender()
        self.window_scale = self.window_sizes[self.sender().text()]

        sdl_audio.lock_audio(self.audio_device_id)
        self._resize_window()
        sdl_audio.unlock_audio(self.audio_device_id)

    def _game_speed_trigger(self):
        self.last_checked_game_speed.setChecked(False)
        self.last_checked_game_speed = self.sender()

        sdl_audio.lock_audio(self.audio_device_id)
        game_boy.change_emulation_speed(self.game_speeds[self.sender().text()])
        sdl_audio.unlock_audio(self.audio_device_id)


    ########################################
    #     ______                           #
    #    |  ____|             | |          #
    #    | |____   _____ _ __ | |_ ___     #
    #    |  __\ \ / / _ \ '_ \| __/ __|    #
    #    | |___\ V /  __/ | | | |_\__ \    #
    #    |______\_/ \___|_| |_|\__|___/    #
    #                                      #
    ########################################

    def keyPressEvent(self, event: QtGui.QKeyEvent | None):
        if event is None:
            return

        self.keys_pressed.add(event.key())
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent | None):
        if event is None:
            return
        self.keys_pressed.discard(event.key())
        super().keyReleaseEvent(event)

