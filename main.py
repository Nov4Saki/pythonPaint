import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QColorDialog, QSlider, 
                             QLabel, QSpinBox)
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QImage
from PyQt5.QtCore import Qt, QPoint


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StaticContents)
        self._image = None
        self._brush_color = Qt.black
        self._brush_size = 5
        self._last_point = QPoint()
        self._path = QPainterPath()
        self.clear_canvas()

    def clear_canvas(self):
        self._image = self._create_blank_image()
        self.update()

    def _create_blank_image(self):
        image = self._image if self._image else None
        if image is None or image.size() != self.size():
            if self.size().width() > 0 and self.size().height() > 0:
                image = QImage(self.size(), QImage.Format_RGB32)
                image.fill(Qt.white)
        return image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self._image, self._image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._last_point = event.pos()
            self._path.moveTo(self._last_point)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self._image)
            painter.setPen(QPen(self._brush_color, self._brush_size, 
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self._last_point, event.pos())
            self._last_point = event.pos()
            self.update()

    def resizeEvent(self, event):
        if self._image is None or self._image.size() != self.size():
            self.clear_canvas()
        super().resizeEvent(event)

    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, color):
        self._brush_color = color

    @property
    def brush_size(self):
        return self._brush_size

    @brush_size.setter
    def brush_size(self, size):
        self._brush_size = size


class PythonPaint(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PythonPaint")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create canvas
        self.canvas = Canvas()
        layout.addWidget(self.canvas)

        # Create controls
        controls_layout = QHBoxLayout()

        # Color button
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(self.choose_color)
        controls_layout.addWidget(self.color_btn)

        # Brush size slider
        controls_layout.addWidget(QLabel("Brush Size:"))
        self.brush_slider = QSlider(Qt.Horizontal)
        self.brush_slider.setMinimum(1)
        self.brush_slider.setMaximum(50)
        self.brush_slider.setValue(5)
        self.brush_slider.valueChanged.connect(self.update_brush_size)
        controls_layout.addWidget(self.brush_slider)

        # Brush size spin box
        self.brush_spin = QSpinBox()
        self.brush_spin.setMinimum(1)
        self.brush_spin.setMaximum(50)
        self.brush_spin.setValue(5)
        self.brush_spin.valueChanged.connect(self.update_brush_size)
        controls_layout.addWidget(self.brush_spin)

        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.canvas.clear_canvas)
        controls_layout.addWidget(clear_btn)

        layout.addLayout(controls_layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.brush_color = color

    def update_brush_size(self, size):
        self.canvas.brush_size = size
        self.brush_slider.setValue(size)
        self.brush_spin.setValue(size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PythonPaint()
    window.show()
    sys.exit(app.exec_())