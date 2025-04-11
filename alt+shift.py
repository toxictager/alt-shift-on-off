import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Enable high DPI support
except:
    pass  # If this fails, just continue without DPI awareness

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtGui import QIcon
import sys
import keyboard
import pyautogui
import time

class ToggleSwitch(QWidget):
    """Custom PyQt6 toggle switch with smooth animation."""
    def __init__(self, callback=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 34)  # Set switch size
        self._slider_pos = 30  # Start position for the slider (ON position)
        self.is_on = True  # Start with "ON" state
        self.animation = QPropertyAnimation(self, b"slider_pos")
        self.animation.setDuration(200)  # Speed of animation
        self.callback = callback  # Function to run when toggled

    def get_slider_pos(self):
        return self._slider_pos

    def set_slider_pos(self, pos):
        self._slider_pos = pos
        self.update()

    slider_pos = property(get_slider_pos, set_slider_pos)

    def mousePressEvent(self, event):
        """Handles toggle switch click event."""
        self.is_on = not self.is_on
        self.animate_toggle()
        self.update()

        if self.callback:
            self.callback(self.is_on)  # Run callback when toggled

    def animate_toggle(self):
        """Creates smooth animation effect when toggling."""
        self.animation.stop()
        self.animation.setStartValue(30 if not self.is_on else 4)
        self.animation.setEndValue(4 if not self.is_on else 30)
        self.animation.start()

    def paintEvent(self, event):
        """Custom paint function for switch background and slider."""
        painter = QPainter(self)

        # Draw background
        bg_color = QColor("#2196F3") if self.is_on else QColor("#ccc")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 60, 34, 17, 17)

        # Draw slider
        painter.setBrush(QColor("white"))
        painter.drawEllipse(self._slider_pos, 4, 26, 26)

class MainWindow(QWidget):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("turn on/off language shortcut")
        self.setFixedSize(300, 150)  # Set fixed window size
        self.center_window()  # Center the window
        self.setWindowIcon(QIcon("favicon.ico"))
        # Layout
        layout = QVBoxLayout()
        self.toggle_switch = ToggleSwitch(self.toggle_clicked)
        self.status_label = QLabel("Shortcut is ON", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arrange widgets
        layout.addWidget(self.toggle_switch, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def center_window(self):
        """Centers the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def toggle_clicked(self, is_on):
        """Runs when switch is toggled (calls the correct function)."""
        if is_on:
            self.status_label.setText("Shortcut is ON")
            self.open_advanced_keyboard_settings_on()
        else:
            self.status_label.setText("Shortcut is OFF")
            self.open_advanced_keyboard_settings_off()

    def open_advanced_keyboard_settings_off(self):
        """Automates disabling the shortcut in Windows settings."""
        pyautogui.press('win')
        time.sleep(3)

        keyboard.write('advanced keyboard')  
        time.sleep(2)

        pyautogui.press('enter')
        time.sleep(3)

        pyautogui.press('tab', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(3)

        pyautogui.press('tab', presses=2, interval=0.5)
        pyautogui.press('enter')
        time.sleep(3)

        pyautogui.press('left', presses=2, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('tab', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('enter')
        pyautogui.hotkey('alt', 'f4')  # Close settings

    def open_advanced_keyboard_settings_on(self):
        """Automates enabling the shortcut in Windows settings."""
        pyautogui.press('win')
        time.sleep(3)

        keyboard.write('advanced keyboard')  
        time.sleep(2)

        pyautogui.press('enter')
        time.sleep(3)

        pyautogui.press('tab', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('tab', presses=2, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('tab', presses=2, interval=0.5)
        pyautogui.press('down', presses=2, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('tab', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('enter')
        pyautogui.hotkey('alt', 'f4')  # Close settings

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())