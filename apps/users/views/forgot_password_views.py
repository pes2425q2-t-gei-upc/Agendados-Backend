from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from apps.users.services.send_email_maileroo import send_email_maileroo

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user:
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = request.build_absolute_uri(
            f'/reset-password/{uidb64}/{token}/'
        )

        send_email_maileroo(
            email,
            'Restablece tu contraseña',
            f'Haz click en este enlace para cambiar tu contraseña: {reset_url}',
        )
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
