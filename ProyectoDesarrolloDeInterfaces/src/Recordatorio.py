from PySide6.QtCore import QDate

class Recordatorio:
    def __init__(self, nombre: str, categoria: str, fecha: QDate):
        '''
        Inicializar un nuevo recordatorio con los valores específicos
        :param nombre: el nombre/ la descripción del recordatorio.
        :param categoria: la categoría a la que pertenece el recordatorio
        :param fecha: la fecha para finalizar el recordatorio
        '''
        self.nombre = nombre
        self.categoria = categoria
        self.fecha = fecha

    def __repr__(self):
        '''
        :return: una cadena con el formato especificado
        '''
        return f"{self.nombre} ({self.categoria}) - {self.fecha.toString('dd/MM/yyyy')}"