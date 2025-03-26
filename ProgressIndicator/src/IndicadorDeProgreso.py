import sys
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton, QMessageBox


class IndicadorDeProgreso(QWidget):
    progreso_actualizar = Signal(int) #el número que indica el progreso

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Indicador de progreso circular")
        self.setGeometry(100, 100, 300, 500)
        self.progreso = 0 #inicializar el progreso

        #crear el layout principal para la ventana
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        #crear el widget para el indicador y añadirlo al layout principal
        self.circle_widget = QWidget()
        layout_principal.addWidget(self.circle_widget)

        #botón para incrementar progreso
        self.boton_aumentar = QPushButton("Aumentar progreso")
        self.boton_aumentar.setStyleSheet("background-color: #47e675; font-family: Courier New; ")
        layout_principal.addWidget(self.boton_aumentar)
        self.boton_aumentar.clicked.connect(self.aumentar_progreso)

        #botón para disminuir progreso
        self.boton_disminuir = QPushButton("Disminuir progreso")
        self.boton_disminuir.setStyleSheet("background-color: #f65780; font-family: Courier New; ")
        layout_principal.addWidget(self.boton_disminuir)
        self.boton_disminuir.clicked.connect(self.disminuir_progreso)

        self.progreso_actualizar.connect(self.progreso_cambiado)

    def establecer_progreso(self, valor):
        self.progreso = max(0, min(100, valor)) #valor del progreso de 0 a 100
        self.progreso_actualizar.emit(self.progreso)
        self.circle_widget.update() #actualizar el progreso para que sea visible en el indicador gráfico

    #utilizar el event handler que Qt va a invocar para cambiar la apariencia del elemento
    def paintEvent(self, event):

        painter = QPainter(self)

        # Calculate the center and radius for the circle
        centro = self.rect().center() #centro del rectangulo cuya forma va a ser cambiada al circulo
        radio = min(self.width(), self.height()) // 3 #calcular el radio del circulo

        #dibujar el círculo: usar sus coordinatas y radio para calcular el diametro y dibujar la figura
        pen_fondo = QPen(QColor("#fbf5fa"), 20) #establecer el color para el circulo con el porcentaje 0 - el circulo del fondo
        painter.setPen(pen_fondo) #establecer el fondo
        x = centro.x() - radio
        y = centro.y() - radio
        diametro = 2 * radio
        #usar el metodo drawArc para crear el círculo dentro del widget
        painter.drawArc(x, y, diametro, diametro, 0, 360 * 16)

        #usar otro pen para que se colorea el círculo depepndiendo del porcentaje
        pen_progreso = QPen(self.cambiar_color(), 20) #el tamaño es igual al cirlulo del fondo; se utiliza la función para cambiar el color
        painter.setPen(pen_progreso)
        progress_angle = -self.progreso * 360 * 16 // 100 #cálculo para que se colorean las partes específicas del circulo - efecto del crecimiento
        painter.drawArc(x, y, diametro, diametro, 90 * 16, progress_angle)

        #mostrar el porcentaje dentro del circulo
        painter.setPen(Qt.black)
        painter.setFont(QFont("Courier New", 18))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.progreso}%")

    #cambiar el color de la línea del indicador dependiendo del porcentaje del progreso
    def cambiar_color(self):
        if (self.progreso < 20):
            return QColor("#fb6262")
        elif (self.progreso >= 20 and self.progreso < 40):
            return QColor("#f9b606")
        elif (self.progreso >= 40 and self.progreso < 60):
            return QColor("#e3f138")
        elif (self.progreso >= 60 and self.progreso < 80):
            return QColor("#d3e034")
        elif (self.progreso >= 80 and self.progreso <= 90):
            return QColor("#84e843")
        else:
            return QColor("#3cc21b")

    def progreso_completado(self):
        if (self.progreso == 100):
            QMessageBox.information(self, "Completado", "¡Enhorabuena, tu progsreso es del 100%!")

    def progreso_en_cero(self):
        if (self.progreso == 0):
            QMessageBox.information(self, "Completado", "¡Tienes que empezar de nuevo!")

    def aumentar_progreso(self):
        nuevo_valor = self.progreso + 10
        self.establecer_progreso(nuevo_valor)
        self.progreso_completado() #llamar el metodo para poder parar el contador y mostrar un mensaje al llegar al 100

    def disminuir_progreso(self):
        nuevo_valor = self.progreso - 10
        self.establecer_progreso(nuevo_valor)
        self.progreso_en_cero() ##llamar el metodo para poder parar el contador y mostrar un mensaje al llegar al 0

    #función para debug para que los mensajes con el porcentaje se muestren por consola
    def progreso_cambiado(self, nuevo_valor):
        print(f"El progreso ha cambiado a: {nuevo_valor}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IndicadorDeProgreso()
    window.show()
    sys.exit(app.exec())

