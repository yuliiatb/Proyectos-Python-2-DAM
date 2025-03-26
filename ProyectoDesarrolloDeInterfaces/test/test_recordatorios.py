import pytest
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QApplication

from src.Recordatorio import Recordatorio
from src.Recordatorios import MainWindow, AgregarRecordatorioDialog

@pytest.fixture(scope="session")
def app_instance():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture()
def window(app_instance):
    window = MainWindow()
    window.show()
    return window

def test_mostrar_todos_los_recordatorios(window):
    '''
    Prueba para llamar la función de mostrar todos los recordatorios cuando las listas están vacías
    :param window: la ventana en la que trabajamos
    :return: la lista, en el caso de esta prueba, vacía
    '''
    # inicializar listas de recordatorios vacías
    window.lista_rec_personal = []
    window.lista_rec_trabajo = []
    window.lista_rec_ocio = []

    window.mostrar_todos_los_recordatorios() # llamar la función que muestre todos los recordatorios
    assert window.recordatorios_layout.count() == 0, "No deben aparecer los recordatorios en la pantalla"

def test_borrar_recordatorio(window):
    '''
    Prueba para borrar un recordatorio
    :param window: la ventana en la que trabajamos
    :return: si se ha borrado el recordatorio (debe haber 0 elementos en la lista)
    '''
    # crear un recordatorio para borrarlo
    recordatorio = Recordatorio("enviar email a Juan - urgente!", "Trabajo", QDate.fromString("20/03/2025", "dd/MM/yyyy"))
    window.borrar_rec_funcion(recordatorio)
    assert window.recordatorios_layout.count() == 0, "Se ha borrado el recordatorio creado"

def test_agregar_recordatorio_a_la_lista(window):
    '''
    Prueba de agregar un objeto del recordatorio a la lista correspondiente
    :param window: la ventana en la que trabajamos
    :return: recordatorio en la lista correspondiente
    '''
    # inicializar listas de recordatorios vacías
    window.lista_rec_personal = []
    window.lista_rec_trabajo = []
    window.lista_rec_ocio = []

    # crear un recordatorio que vamos a agregar a la lista
    recordatorio = Recordatorio("enviar email a Juan - urgente!", "Trabajo", QDate.fromString("20/03/2025", "dd/MM/yyyy"))
    window.agregar_a_la_lista(recordatorio)

    assert recordatorio in window.lista_rec_trabajo, "El recordatorio debería estar en la lista 'Trabajo'"
    assert recordatorio not in window.lista_rec_personal, "El recordatorio no debería estar en la lista 'Personal'"
    assert recordatorio not in window.lista_rec_ocio, "El recordatorio no debería estar en la lista 'Ocio'"

