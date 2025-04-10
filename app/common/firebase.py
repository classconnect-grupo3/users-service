import os
import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin.exceptions import FirebaseError

def initialize_firebase():
    try:
        if not firebase_admin._apps:  # pylint: disable=protected-access
            # Get the path to the credentials from the environment variable
            path = os.getenv("FIREBASE_CREDENTIALS")
            if not path:
                raise ValueError("The environment variable 'FIREBASE_CREDENTIALS' is not defined.")
                
            cred = credentials.Certificate(path)
            initialize_app(cred)
            print("Firebase has been initialized successfully.")
        else:
            print("Firebase is already initialized.")
    except FirebaseError as e:
        print(f"Error initializing Firebase: {e}")
        raise e
    except Exception as e:
        print(f"Unknown error: {e}")
        raise e