from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.users.seralizers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response(
        {"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(status=HTTP_200_OK)


@api_view(["POST"])
def google_auth(request):
    """
    Endpoint para autenticar usuarios con Google
    """
    id_token_str = request.data.get("idToken")
    
    if not id_token_str:
        return Response(
            {"error": "El idToken de Google es obligatorio"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Lista de Client IDs aceptados
        client_ids = [
            settings.GOOGLE_CLIENT_ID,  # Tu Client ID actual
            settings.GOOGLE_CLIENT_ID_ALCO
        ]
        
        # Intentar verificar con cada client_id
        idinfo = None
        last_error = None
        
        for client_id in client_ids:
            try:
                # Verificar el ID token con los servidores de Google
                idinfo = id_token.verify_oauth2_token(
                    id_token_str, 
                    requests.Request(), 
                    client_id
                )
                # Si llegamos aquí, la verificación fue exitosa
                break
            except ValueError as e:
                last_error = e
                continue
                
        # Si ningún Client ID funcionó
        if not idinfo:
            return Response(
                {"error": f"Token de Google inválido o expirado: {str(last_error)}"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar que el token es de Google
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return Response(
                {"error": "Token de Google inválido"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Obtener el email del token verificado
        email = idinfo['email']
        
        # Verificar si el usuario ya existe
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Si no existe, creamos un nuevo usuario
            username = email.split('@')[0]
            
            # Asegurarnos de que el username sea único
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=idinfo.get('given_name', ''),
                last_name=idinfo.get('family_name', ''),
                password=None
            )
        
        # Generar o recuperar token para el usuario
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        
        return Response(
            {"token": token.key, "user": serializer.data}, 
            status=status.HTTP_200_OK
        )
            
    except ValueError:
        return Response(
            {"error": "Token de Google inválido o expirado"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return Response(
            {"error": f"Error al procesar la autenticación: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

