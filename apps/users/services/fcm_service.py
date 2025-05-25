import json
import requests
from google.oauth2 import service_account
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        settings.FCM_SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    access_token_info = credentials.refresh(requests.Request())
    return access_token_info.token

def send_fcm_notification(token, title, body, data=None):
    """
    Envía una notificación push usando Firebase Cloud Messaging API v1
    
    Args:
        token: El token FCM del dispositivo
        title: Título de la notificación
        body: Cuerpo/mensaje de la notificación
        data: Diccionario opcional con datos adicionales
    """
    access_token = get_access_token()
    
    url = f'https://fcm.googleapis.com/v1/projects/{settings.FCM_PROJECT_ID}/messages:send'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }
    
    # Añadir datos adicionales si se proporcionan
    if data:
        message["message"]["data"] = data
    
    response = requests.post(url, headers=headers, data=json.dumps(message))
    
    if response.status_code == 200:
        return {"success": True, "response": response.json()}
    else:
        return {"success": False, "error": response.text}