import requests
import os
from app.common.result import Success, Failure
from app.errors.authentication_errors import InvalidCredentialsError

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")



def verify_email_and_password(email: str, password: str):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    params = {
        "key": FIREBASE_API_KEY
    }
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, params=params, json=payload, timeout=10)
    if response.status_code == 200:
        id_token = response.json().get("idToken")
        return Success(id_token)  
    else:
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
        return Failure(InvalidCredentialsError(message=f"Authentication failed: {error_message}"))
    

