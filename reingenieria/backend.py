import logging
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from Operarios.models import Cargo, CargoAsignado

class ElMejorBackend(object):

    def authenticate(self, request, **kwargs):
        '''
        kwargs will receive the python dict that may contain 
        username & password to authenticate which will be 
        received from the Custom admin site.
        '''
        try:
            username = kwargs['username']
            password = kwargs['password']
            
            #if not my_portal_authenticate(username, password):
            #    raise forms.ValidationError(
            #        _("El usuario no tiene cargo asignado")
            #    )
        
            '''
            Check if the user exist in the django_auth_user 
            table, if not then UserNotExist exception will  
            be raised automatically and user will be added 
            (with or without password) in the exception 
            handling block
            '''
            
            #Check if the user exist in the database, if it exist in the 
            #database, auth_user will not be updated and exception will not be raised
            user = User.objects.get(username = username)
            CargoA = CargoAsignado.objects.get(user=user)

        except KeyError as e:
            raise forms.ValidationError(_("Programming Error") )

        except User.DoesNotExist:
            '''
            Si el usuario no existe se logguea el error.
            '''
            logging.getLogger("error_logger").error("El usuario %s no existe", username)
            raise forms.ValidationError(_('El usuario no existe'))
            return None

        except CargoAsignado.DoesNotExist:
            '''
            Si el usuario no existe se logguea el error.
            '''
            if user.is_superuser:
                return user
            else:
                logging.getLogger("error_logger").error("El usuario %s no tiene cargo asignado", user)
                raise forms.ValidationError(_('El usuario no tiene cargo asignado'))
                return None
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            #Djano Admin treats None user as anonymous your who have no right at all.
            logging.getLogger("error_logger").error("El usuario %s no existe", user_id)
            return None