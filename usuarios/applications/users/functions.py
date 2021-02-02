# funciones extras de la aplicacion users

import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits): # devuelve string plano y todo en mayuscula y agregue digitos
    return ''.join(random.choice(chars) for _ in range(size)) #generar 6 letras random