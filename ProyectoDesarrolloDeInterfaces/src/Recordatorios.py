import sys

from PySide6.QtCore import QDate
from PySide6.QtGui import QKeySequence, QPixmap, Qt, QAction
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMenuBar, QMainWindow, QDialog, QLineEdit, \
    QComboBox, QPushButton, QDateEdit, QMessageBox, QScrollArea, QMenu, QHBoxLayout, QCheckBox

from src.Recordatorio import Recordatorio

class AgregarRecordatorioDialog(QDialog):
    '''
    Ventana de diálogo para agregar o editar un recordatorio
    '''
    def __init__(self, main_window, recordatorio = None):
        super().__init__()

        self.main_window = None
        self.main_window = main_window
        self.recordatorio = recordatorio # variable para que se muestren los datos del objeto Recordatorio si hay que editar uno

        # añadir los mensajes de consola para seguir el comportamiento de la aplicación
        print("Atributos del recordatorio:")
        if self.recordatorio:
            print(f"- Nombre: {self.recordatorio.nombre}")
            print(f"- Categoria: {self.recordatorio.categoria}")
            print(f"- Fecha: {self.recordatorio.fecha.toString()}")

        # establecer dos posibles nombres de la ventana: para crear y editar recordatorio
        self.setWindowTitle("Agregar un nuevo recordatorio" if not recordatorio else "Editar recordatorio")
        self.setGeometry(100, 100, 300, 200)

        self.nombre_recordatorio = QLineEdit()
        self.nombre_recordatorio.setPlaceholderText("Escribe tu recordatorio aquí")

        if self.recordatorio:
            self.nombre_recordatorio.setText(self.recordatorio.nombre)

        # añadir un menú desplegable para que el usuario elija la categoría del recordatorio
        self.dropdown_label = QLabel("Elige la categoría del recordatorio: ")
        self.dropdown_categorias = QComboBox()
        self.dropdown_categorias.addItems(["Personal", "Trabajo", "Ocio"])

        # asignar la categoría: buscar el texto que coincide con el texto de las categorías del menú y asignarle el índice
        if self.recordatorio:
            index = self.dropdown_categorias.findText(self.recordatorio.categoria)
            if index >= 0:
                self.dropdown_categorias.setCurrentIndex(index)

        # añadir la fecha para el recordatorio
        self.fecha_label = QLabel("Elije la fecha del recordatorio")
        self.fecha_elegir = QDateEdit()
        self.fecha_elegir.setCalendarPopup(True) #mostrar el calendario para elegir la fecha
        self.fecha_elegir.setDate(QDate.currentDate())

        if self.recordatorio:
            self.fecha_elegir.setDate(self.recordatorio.fecha)
        else:
            self.fecha_elegir.setDate(QDate.currentDate())

        # botones para confirmar o calcelar la operación
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_recordatorio)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar_recordatorio)

        layout_dialog = QVBoxLayout()
        layout_dialog.addWidget(self.nombre_recordatorio)
        layout_dialog.addWidget(self.dropdown_label)
        layout_dialog.addWidget(self.dropdown_categorias)
        layout_dialog.addWidget(self.fecha_label)
        layout_dialog.addWidget(self.fecha_elegir)
        layout_dialog.addWidget(self.btn_guardar)
        layout_dialog.addWidget(self.btn_cancelar)

        self.setLayout(layout_dialog)

    def guardar_recordatorio(self):
        '''
        Función para guardar el recordatorio
        :return: devuelve el recordatorio guardado
        '''
        nombre = self.nombre_recordatorio.text()
        categoria = self.dropdown_categorias.currentText()  # acceder al elemento seleccionado
        fecha = self.fecha_elegir.date()  # recoger la fecha elegida en el calendario

        if nombre == "":
            QMessageBox.warning(self, "Error", "El recordatorio no puede estar vacío.")
            return

        if fecha < QDate.currentDate():
            QMessageBox.warning(self, "Error", "La fecha para el recordatorio no puede ser anterior a la fecha actual")
            return

        print(f"Nuevo recordatorio: Nombre: {nombre}, Categoría: {categoria}, Fecha: {fecha.toString('dd/MM/yyyy')}")

        # si el recordatorio existe y lo modificamos
        if self.recordatorio:
            # eliminar el recordatorio anterior de su lista
            if self.recordatorio.categoria == "Personal":
                self.main_window.lista_rec_personal.remove(self.recordatorio)
            elif self.recordatorio.categoria == "Trabajo":
                self.main_window.lista_rec_trabajo.remove(self.recordatorio)
            elif self.recordatorio.categoria == "Ocio":
                self.main_window.lista_rec_ocio.remove(self.recordatorio)

            # actualizar los valores (si hubo cambios)
            self.recordatorio.nombre = nombre
            self.recordatorio.categoria = categoria
            self.recordatorio.fecha = fecha

            # añadir el recordatorio a nueva lista (si se ha cambiado la categoría)
            if categoria == "Personal":
                self.main_window.lista_rec_personal.append(self.recordatorio)
            elif categoria == "Trabajo":
                self.main_window.lista_rec_trabajo.append(self.recordatorio)
            elif categoria == "Ocio":
                self.main_window.lista_rec_ocio.append(self.recordatorio)

            QMessageBox.information(self, "Éxito", f"El recordatorio '{nombre}' se ha actualizado correctamente.")
            self.main_window.actualizar_vista()

        # si el recordatorio no ha sido encontrado, creamos uno nuevo
        else:
            nuevo_recordatorio = Recordatorio(nombre, categoria, fecha)
            print(f"Creando nuevo recordatorio: {nuevo_recordatorio.nombre}")

            self.main_window.agregar_a_la_lista(nuevo_recordatorio)
            QMessageBox.information(self, "Éxito", f"El recordatorio '{nombre}' se ha creado correctamente a {categoria}.")

        self.accept() # cerrar la ventana

    def cancelar_recordatorio(self):
        '''
        Para cancelar la operación de la creación o la edición del recordatorio y cerrar la ventana de diálogo
        :return: Cierra la ventana al pulsar el botón correspondiente
        '''
        QMessageBox.warning(self,"Atención", "Cancelamos la operación. Los datos no se van a guardar")
        self.reject()


class MainWindow(QMainWindow):
    '''
    Clase con la lógica principal de la aplicación
    '''
    def __init__(self):
        super().__init__()
        self.dialog = None
        self.setWindowTitle("Recordatorios")
        self.setGeometry(100, 100, 500, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)

        self.label_titulo = QLabel("Mis recordatorios")
        self.label_titulo.setStyleSheet("font-family: 'Caviar Dreams'; font-size: 18px; font-weight: bold;")
        layout_principal.addWidget(self.label_titulo)

        # añadir un contenedor para mostrar las tareas
        self.recordatorios_contenedor = QWidget()
        self.recordatorios_layout = QVBoxLayout(self.recordatorios_contenedor)

        # añadir un scroll area por si las tareas sobrepasan el tamaño del contenedor
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.recordatorios_contenedor)

        layout_principal.addWidget(self.scroll_area)  # añadir scroll area al layout principal

        # las listas para los tres tipos de recordatorios
        self.lista_rec_personal = []
        self.lista_rec_trabajo = []
        self.lista_rec_ocio = []

        # agregar la barra de menú a la ventana principal
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # primer menú: opciones y acciones
        menu_recordatorios = menu_bar.addMenu("Recordatorios")
        agregar_menu_action = menu_recordatorios.addAction("Agregar nuevo recordatorio")
        agregar_menu_action.triggered.connect(self.agregar_recordatorio)

        todos_menu_action = menu_recordatorios.addAction("Todos los recordatorios")
        todos_menu_action.triggered.connect(self.mostrar_todos_los_recordatorios)

        proximos_menu_action = menu_recordatorios.addAction("Próximos recordatorios")
        proximos_menu_action.triggered.connect(self.mostrar_proximos_recordatorios)

        # segundo menú: opciones y acciones; shortcuts para abrir esas opciones del menú
        menu_categorias = menu_bar.addMenu("Categorías")
        personal_menu_action = menu_categorias.addAction("Personal")
        personal_menu_action.setShortcut(QKeySequence("CTRL+P"))
        personal_menu_action.triggered.connect(self.mostrar_rec_personales)

        trabajo_menu_action = menu_categorias.addAction("Trabajo")
        trabajo_menu_action.setShortcut(QKeySequence("CTRL+T"))
        trabajo_menu_action.triggered.connect(self.mostrar_rec_trabajo)

        ocio_menu_action = menu_categorias.addAction("Ocio")
        ocio_menu_action.setShortcut(QKeySequence("CTRL+O"))
        ocio_menu_action.triggered.connect(self.mostrar_rec_ocio)

        # guía de colores para que el usuario sepa la categoría del recordatorio por su color
        self.guia_colores = QWidget()
        self.guia_colores_layout = QVBoxLayout(self.guia_colores)

        # crear las etiquetas para cada categoría con su color
        self.guia_colores_layout.addWidget(self.crear_categoria_color("Personal", "#F3C301"))
        self.guia_colores_layout.addWidget(self.crear_categoria_color("Trabajo", "#ADCACB"))
        self.guia_colores_layout.addWidget(self.crear_categoria_color("Ocio", "#87C159"))

        layout_principal.addWidget(self.guia_colores)

    def agregar_recordatorio(self):
        '''
        Función para crear el recordatorio y establecer sus valores según los datos del usuario.
        :return: Se abre la ventana de diálogo y se sigue su lógica para crear el recordatorio
        '''
        self.dialog = AgregarRecordatorioDialog(self)
        self.dialog.exec()

    def agregar_a_la_lista(self, recordatorio):
        '''
        Agregar el recordatorio a la lista correspondiente
        :param recordatorio: el objeto que ha sido creado
        :return: la lista a la que está añadido según la elección del usuario
        '''
        # añadir recordatorio a la lista correspondiente

        if recordatorio.categoria == "Personal":
            self.lista_rec_personal.append(recordatorio)
        elif recordatorio.categoria == "Trabajo":
            self.lista_rec_trabajo.append(recordatorio)
        elif recordatorio.categoria == "Ocio":
            self.lista_rec_ocio.append(recordatorio)

        self.mostrar_recordatorio(recordatorio)

    def mostrar_recordatorio(self, recordatorio):
        '''
        Mostrar el recordatorio en la ventana principal
        :param recordatorio: el objeto que ha sido creado
        :return: lo muestra en la pantalla dentro de su contenedor coloreado según la categoría, con checkbox, nombre y fecha.
        '''
        checkbox = QCheckBox() # para marcar si el recordatorio está completo
        checkbox.toggled.connect(self.checkbox_marcado)

        un_recordatorio = QLineEdit(f"{recordatorio.nombre}")
        un_recordatorio.setReadOnly(True) # no permitir la edición del campo

        fecha_rec = QLineEdit(f"{recordatorio.fecha.toString('dd/MM/yyyy')}")
        fecha_rec.setReadOnly(True) # no permitir la edición del campo

        if recordatorio.categoria == "Personal":
            un_recordatorio.setStyleSheet("background-color: #F3C301; font-family: 'Caviar Dreams'; font-weight: bold; font-size: 14px;")
        elif recordatorio.categoria == "Trabajo":
            un_recordatorio.setStyleSheet("background-color: #ADCACB; font-family: 'Caviar Dreams'; font-weight: bold; font-size: 14px;")
        elif recordatorio.categoria == "Ocio":
            un_recordatorio.setStyleSheet("background-color: #87C159; font-family: 'Caviar Dreams'; font-weight: bold; font-size: 14px;")

        # establecer meú contextual para cada recordatorio
        un_recordatorio.setContextMenuPolicy(Qt.CustomContextMenu)
        un_recordatorio.customContextMenuRequested.connect(lambda pos, r=recordatorio: self.mostrar_context_menu(pos, r))

        # crear un layout para cada recordatorio que consiste de un checkbox, el nombre del recordatorio (coloreado) y la fecha
        layout_un_recordatorio = QHBoxLayout()
        layout_un_recordatorio.addWidget(checkbox)
        layout_un_recordatorio.addWidget(un_recordatorio)
        layout_un_recordatorio.addWidget(fecha_rec)

        # para que aparezcan desde arriba al añadir recordatorios
        layout_un_recordatorio.setAlignment(Qt.AlignTop)

        widget_recordatorio = QWidget()
        widget_recordatorio.setLayout(layout_un_recordatorio)
        self.recordatorios_layout.addWidget(widget_recordatorio)

    def mostrar_todos_los_recordatorios(self):
        '''
        Muestra todos los recordatorios
        :return: todas las listas
        '''
        # mostrar mensaje si no hay recordatorios en las listas
        if not self.lista_rec_personal and not self.lista_rec_trabajo and not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios")

        # quitar los recordatorios de la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # buscar los recordatorios en todas las listas
        for recordatorio in self.lista_rec_personal + self.lista_rec_trabajo + self.lista_rec_ocio:
            # revisamos si el recordatorio es un objeto válido
            if isinstance(recordatorio, Recordatorio):
                self.mostrar_recordatorio(recordatorio)
            else:
                print(f"Recordatorio: {recordatorio} no es válido")

    def mostrar_proximos_recordatorios(self):
        '''
        Mostrar recordatorios próximos (su fecha finaliza con un máximo de 5 días)
        :return: los recordatorios cuya fecha coincide con la condición
        '''
        # mostrar mensaje si no hay recordatorios en las listas
        if not self.lista_rec_personal and not self.lista_rec_trabajo and not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios")

        # quitar los recordatorios de la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # inicializar la fecha de hoy
        hoy = QDate.currentDate()
        # añadir la fecha máxima para el recordatorio próximo: hoy + 5 días
        limite = hoy.addDays(5)

        # filtrar los recordatorios según la condición establecida anteriormente
        recordatorio_encontrado = False
        for recordatorio in self.lista_rec_personal + self.lista_rec_trabajo + self.lista_rec_ocio:
            if hoy <= recordatorio.fecha <= limite:
                self.mostrar_recordatorio(recordatorio)
                recordatorio_encontrado = True

        # si no hay recordatorios próximos
        if not recordatorio_encontrado:
            QMessageBox.information(self, "No hay próximos", "No hay recordatorios próximos")

    def mostrar_rec_personales(self):
        '''
        Muestra los recordatorios de la categoría "Personal"
        :return: la lista de estos recordatorios y los muestra en pantalla
        '''
        # mostrar mensaje si no hay recordatorios en las listas
        if not self.lista_rec_personal and not self.lista_rec_trabajo and not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios")

        if not self.lista_rec_personal:
            QMessageBox.information(self, "Error", "No hay recordatorios de la categoría 'Personal'")
            return

        # quitar los recordatorios de la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        for recordatorio in self.lista_rec_personal: #mostrar recordatorios personales
            self.mostrar_recordatorio(recordatorio)

    def mostrar_rec_trabajo(self):
        '''
        Muestra los recordatorios de la categoría "Trabajo"
        :return: la lista de estos recordatorios y los muestra en pantalla
        '''
        # mostrar mensaje si no hay recordatorios en las listas
        if not self.lista_rec_personal and not self.lista_rec_trabajo and not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios")

        if not self.lista_rec_trabajo:
            QMessageBox.information(self, "Error", "No hay recordatorios de la categoría 'Trabajo'")
            return

        # quitar los recordatorios de la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        for recordatorio in self.lista_rec_trabajo:
            self.mostrar_recordatorio(recordatorio)

    def mostrar_rec_ocio(self):
        '''
        Muestra los recordatorios de la categoría "Ocio"
        :return: la lista de estos recordatorios y los muestra en pantalla
        '''
        # mostrar mensaje si no hay recordatorios en las listas
        if not self.lista_rec_personal and not self.lista_rec_trabajo and not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios")

        if not self.lista_rec_ocio:
            QMessageBox.information(self, "Error", "No hay recordatorios de la categoría 'Ocio'")
            return

        # quitar los recordatorios de la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        for recordatorio in self.lista_rec_ocio:
            self.mostrar_recordatorio(recordatorio)

    def mostrar_context_menu(self, position, recordatorio):
        '''
        Muestra el menú contextual para cada recordatorio
        :param position: posición del menú
        :param recordatorio: el objeto para que se abre el menú
        :return: el menú con acciones
        '''

        context_menu = QMenu(self)
        editar_recordatorio = QAction("Editar recordatorio", self)
        # usar lambda para llamar la función para editar el recordatorio
        editar_recordatorio.triggered.connect(lambda: self.editar_rec_funcion(recordatorio))

        borrar_recordatorio = QAction("Borrar recordatorio", self)
        borrar_recordatorio.triggered.connect(lambda: self.borrar_rec_funcion(recordatorio))

        context_menu.addAction(editar_recordatorio)
        context_menu.addAction(borrar_recordatorio)
        context_menu.exec(self.mapToGlobal(position))

    def checkbox_marcado(self):
        '''
        Checkbox asignado a cada recordatorio
        :return: checkbox marcado o desmarcado
        '''
        checkbox = self.sender()
        if checkbox.isChecked():
            QMessageBox.information(self, "Marcado", "El recordatorio marcado como hecho. Puedes borrarlo.")
        else:
            QMessageBox.information(self, "Desmarcado", "El recordatorio desmarcado")

    def editar_rec_funcion(self, recordatorio):
        '''
        LLama la ventana de diálogo para editar el recordatorio. Se abre la ventana con los datos de objeto rellenados y editables
        :param recordatorio: el objeto a editar
        :return: abre la ventana y devuelve el objeto modificado
        '''
        dialog = AgregarRecordatorioDialog(self, recordatorio)
        dialog.exec()

    def actualizar_vista(self):
        '''
        Función para asegurarnos que la información del objeto coincide con los datos que se muestran en la pantalla
        :return: la vista actualizada (por ejemplo, si editamos el recordatorio o lo borramos)
        '''
        # borrar los widgets para actualizar la información que se muestra en la pantalla
        while self.recordatorios_layout.count():
            widget = self.recordatorios_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # volver a añadir los widgets
        for recordatorio in self.lista_rec_personal + self.lista_rec_trabajo + self.lista_rec_ocio:
            self.mostrar_recordatorio(recordatorio)

    def borrar_rec_funcion(self, recordatorio):
        '''
        Función para borrar el recordatorio
        :param recordatorio: el objeto para borrar
        :return: si se ha eliminado el recordatorio
        '''
        # buscar y borrar el recordatorio de la lista correspondiente
        if recordatorio.categoria == "Personal":
            if recordatorio in self.lista_rec_personal:
                self.lista_rec_personal.remove(recordatorio)

        elif recordatorio.categoria == "Trabajo":
            if recordatorio in self.lista_rec_trabajo:
                self.lista_rec_trabajo.remove(recordatorio)

        elif recordatorio.categoria == "Ocio":
            if recordatorio in self.lista_rec_ocio:
                self.lista_rec_ocio.remove(recordatorio)

        QMessageBox.information(self, "Eliminado", f"El recordatorio '{recordatorio.nombre}' se ha eliminado.")
        self.actualizar_vista()

    def crear_categoria_color(self, nombre_categoria, color):
        '''
        Función para mostrar los colores de los recordatorios a los usuarios.
        :param nombre_categoria: nombre de la categoría del recordatorio
        :param color: color que corresponde a cada actegoria
        :return: la lista de categorías con una muestra de color
        '''
        categoria_widget = QWidget()
        categoria_layout = QHBoxLayout(categoria_widget)

        # crear un pequeño rectangulo con el color dependiando de la categoría
        color_ejemplo = QLabel()
        color_ejemplo.setStyleSheet(f"background-color: {color}; border-radius: 5px;")

        # especificar el nombre de la categoría y su estilo
        nombre_label = QLabel(f"{nombre_categoria}")
        nombre_label.setStyleSheet("font-family: 'Caviar Dreams'; font-size: 14px; ")

        categoria_layout.setSpacing(5) # añadir espacio entre el cuadrado de color y el nombre
        categoria_layout.setAlignment(Qt.AlignLeft)

        categoria_layout.addWidget(color_ejemplo)
        categoria_layout.addWidget(nombre_label)

        return categoria_widget

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())