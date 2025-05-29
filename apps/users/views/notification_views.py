from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from ..serializers import UserFCMTokenSerializer, NotificationSerializer
from ..models import UserFCMToken, Notification
from django.conf import settings
from ..services.fcm_service import send_fcm_notification


# Endpoint para registrar o actualizar el token FCM del usuario
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_fcm_token(request):
    token = request.data.get("token")
    if not token:
        return Response({"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST)
    obj, _ = UserFCMToken.objects.update_or_create(
        user=request.user,
        defaults={"token": token}
    )
    serializer = UserFCMTokenSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Endpoint para enviar notificación push a un usuario
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_push_notification(request):
    user_id = request.data.get("user_id")
    title = request.data.get("title")
    body = request.data.get("body")
    data = request.data.get("data", {})  # Datos adicionales opcionales
    
    if not (user_id and title and body):
        return Response({"error": "user_id, title y body son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        fcm_token_obj = user.fcm_tokens.last()
        
        if not fcm_token_obj:
            return Response({"error": "Usuario no tiene token FCM registrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Usar el nuevo servicio FCM v1 en lugar de pyfcm
        result = send_fcm_notification(
            token=fcm_token_obj.token,
            title=title,
            body=body,
            data=data
        )
        
        # También guardamos la notificación interna
        Notification.objects.create(user=user, title=title, body=body)
        
        return Response({"success": True, "result": result}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


# Endpoint para listar notificaciones internas
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# Endpoint para marcar notificación como leída
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_notification_read(request):
    notification_id = request.data.get("notification_id")
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"success": True})
    except Notification.DoesNotExist:
        return Response({"error": "Notificación no encontrada"}, status=status.HTTP_404_NOT_FOUND)