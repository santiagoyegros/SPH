from django.apps import AppConfig


class OperariosConfig(AppConfig):
    name = 'Operarios'

    def ready(self):
        #from scheduler import planificador
        #planificador.start()
        """Registro de ausencias"""
        # from scheduler import register
        # register.start()

        

