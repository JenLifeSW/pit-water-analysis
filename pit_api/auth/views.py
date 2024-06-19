from datetime import timedelta

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from pit_api.auth.models import Role, EmailVerification
from pit_api.auth.serializers import RegistrationSerializer, LoginSerializer, EmailVerificationSerializer
from pit_api.common.exceptions import BadRequest400Exception, UnAuthorized401Exception
from pit_api.common.views import PublicAPIView
from pit_api.users.models import User
from pit_api.users.serializers import UserInfoSerializer


class RegistrationAPIView(PublicAPIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        nickname = request.data.get("nickname")
        role_id = request.data.get("role_id")

        if not username or not password:
            raise BadRequest400Exception({"message": "아이디 또는 비밀번호가 입력되지 않았습니다."})

        if not nickname or nickname is None:
            nickname = "사용자"

        try:
            role = Role.objects.get(pk=role_id)
        except:
            role = Role.objects.get(pk=0)

        host_user = JWTAuthentication().authenticate(request)
        if host_user is not None:
            user = host_user[0]
            user_role_limit = user.role.id
            if role.id >= user_role_limit:
                raise UnAuthorized401Exception({"message": "새로운 유저의 권한은 현재 유저의 권한보다 높을 수 없습니다."})
        if host_user is None and role.id != 0:
            raise UnAuthorized401Exception({"message": "새로운 유저의 권한은 현재 유저의 권한보다 높을 수 없습니다."})

        created_at = timezone.now()
        user_data = {
            "username": username,
            "password": password,
            "nickname": nickname,
            "role": role.id,
            "created_at": created_at
        }

        serializer = RegistrationSerializer(data=user_data)

        if not serializer.is_valid():
            raise BadRequest400Exception(serializer.get_error_body())
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginAPIView(PublicAPIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            user = authenticate(username=username, password=password)
            if not user:
                raise BadRequest400Exception({"message": "아이디 또는 비밀번호를 확인하세요."})

            token = TokenObtainPairSerializer().get_token(user)

            serializer = UserInfoSerializer(user)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response["Authorization"] = f"Bearer {token}/{token.access_token}"
            return response

        raise BadRequest400Exception({"message": "아이디 또는 비밀번호를 입력하세요."})


class RefreshTokenAPIView(PublicAPIView):
    def post(self, request):
        refresh_token = request.headers.get("Authorization").split(" ")[1]
        if not refresh_token:
            raise BadRequest400Exception({"message": "잘못된 요청입니다."})

        try:
            token = RefreshToken(refresh_token)
            response = Response(status=status.HTTP_204_NO_CONTENT)
            response["Authorization"] = f"Bearer {token.access_token}"
            return response
        except Exception as e:
            raise BadRequest400Exception({"message": f"토큰 갱신 실패: {str(e)}"})


class SendVerificationEmail(PublicAPIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            raise BadRequest400Exception({"message": "이메일을 입력하세요."})

        if User.objects.filter(email=email).exists():
            raise BadRequest400Exception({"message": "이미 사용중인 이메일입니다."})

        # user = User.objects.get(email=email)
        EmailVerification.objects.filter(email=email, is_used=False).delete()

        verification = EmailVerification.objects.create(
            # user=user,
            email=email,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        send_mail(
            "PIT 메일 인증 번호",
            f"메일 인증용 코드는 {verification.code} 입니다.",
            "noreply@jen-life.com",
            [email],
            fail_silently=False,
        )
        code_token = verification.code_token
        response = Response({"codeToken": code_token}, status=status.HTTP_200_OK)

        return response


class VerifyEmail(PublicAPIView):
    def post(self, request):
        email = request.data.get("email")
        verification_code = request.data.get("verificationCode")
        code_token = request.data.get("codeToken")

        try:
            verification = EmailVerification.objects.get(code_token=code_token)
        except EmailVerification.DoesNotExist:
            raise BadRequest400Exception({"message": "잘못된 요청입니다."})

        if email != verification.email:
            raise BadRequest400Exception({"message": "잘못된 요청입니다."})

        if verification_code != verification.code:
            raise BadRequest400Exception({"message": "인증코드가 옳바르지 않습니다."})

        serializer = EmailVerificationSerializer(instance=verification)
        verification_token = serializer.create_verification_token()
        response = Response({"verificationToken": verification_token}, status=status.HTTP_200_OK)

        return response
