import os
import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin.exceptions import FirebaseError
import json

def initialize_firebase():
    try:
        if not firebase_admin._apps:  # pylint: disable=protected-access
            # Obtener el JSON de las credenciales desde la variable de entorno
            firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
            if not firebase_credentials:
                raise ValueError("La variable de entorno 'FIREBASE_CREDENTIALS' no está definida.")
            
            # Parsear el JSON
            credentials_dict = json.loads(firebase_credentials)
            
            # Crear un objeto de credenciales a partir del diccionario
            cred = credentials.Certificate(credentials_dict)
            initialize_app(cred)
            print("Firebase se ha inicializado correctamente.")
        else:
            print("Firebase ya está inicializado.")
    except FirebaseError as e:
        print(f"Error al inicializar Firebase: {e}")
        raise e
    except Exception as e:
        print(f"Error desconocido: {e}")
        raise e
