from django.shortcuts import render
from rest_framework import  generics, status, views
from rest_framework.response import  Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import  settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http  import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer,RequestPasswordResetEmailSerializer, SetNewPasswordAPIView
from .models import User
from .utils import Util
from .renderers import UserRenderer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data =user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        print(current_site)
        relativeLink = reverse('verify_email')
        absurl = "http://"+current_site +relativeLink+"?token="+str(token)
        email_body = 'H1 ' + user.username + ' use the link below to verify your email \n'+ absurl
        data = {'email_body':email_body, 'email_subject' : 'Verify your email','to_user': user.email}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param = openapi.Parameter('token', in_=openapi.IN_QUERY,type=openapi.TYPE_STRING, description='EmailVerification')

    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified =True
                user.save()
            return Response({'email':"succefully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as error:
            return Response({'error': "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as error:
            return Response({'error': "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView) :
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hello, \n use the link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'email_subject': 'Reset your password', 'to_user': user.email}
            Util.send_email(data)
        return Response({'success':'We have sent you a link for passwordReset'},status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:

            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success  ': 'true', 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as error:
            return Response({'error': 'Token is not valid'},
                            status=status.HTTP_401_UNAUTHORIZED_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordAPIView

    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'succes':True, 'message':"Password reset success"}, status=status.HTTP_200_OK)