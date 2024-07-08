from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        try:
            token = AccessToken(raw_token)
            if token.get('token_type') != 'access':
                raise InvalidToken('Token type is not access.')
            return token
        except TokenError as e:
            raise InvalidToken({
                'detail': 'Given token not valid for any token type',
                'messages': str(e),
            })

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
