from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from app.providers.base import BaseProvider
from app.providers.facebook import FacebookProvider


# Create your views here.
class SocialConnectMixin:
    """API to connect social account to user"""

    provider = None

    def connect(self, request):
        """Connect social accounts"""
        code = request.data.get("code")

        if not code:
            raise ValueError

        if not self.provider:
            raise ValueError

        provider: BaseProvider = self.provider()
        provider.get_token(code)
        return provider.get_user_info()


class FacebookConnectViewSet(SocialConnectMixin, viewsets.ViewSet):
    """ViewSet to connect Facebook oauth2."""

    provider = FacebookProvider

    @action(detail=False, methods=['get'])
    def auth_url(self, request):
        """Return OAuth2 URL for Facebook."""
        provider = self.provider()
        return Response(provider.get_oauth2_url())

    @action(detail=False, methods=['post'])
    def auth(self, request):
        """Authenticate and get user info."""
        return Response(self.connect(request))


router = DefaultRouter()
router.register(r'api/social/facebook', FacebookConnectViewSet, basename='facebook_social')
urlpatterns = router.urls
