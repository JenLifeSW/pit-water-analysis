import json

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from pit_api.common.exceptions import BadRequest400Exception, UnAuthorized401Exception, NotFound404Exception
from pit_api.common.permissions import IsPostAble


class PublicAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except BadRequest400Exception as error:
            return self.handle_error_response(error, status.HTTP_400_BAD_REQUEST)
        except UnAuthorized401Exception as error:
            return self.handle_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except NotFound404Exception as error:
            return self.handle_error_response(error, status.HTTP_404_NOT_FOUND)

    def handle_error_response(self, error, status_code):
        error_body = json.loads(error.message)
        response = Response(error_body, status=status_code)
        renderer = JSONRenderer()
        renderer_context = self.get_renderer_context()
        response.accepted_renderer = renderer
        response.accepted_media_type = renderer.media_type
        response.renderer_context = renderer_context
        return response


@authentication_classes([JWTAuthentication])
@permission_classes([IsPostAble])
class BaseAPIView(PublicAPIView):
    pass
