from unittest.mock import patch
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from app.providers.facebook import FacebookProvider

SOCIAL_MEDIA_SETTINGS = {
    "facebook": {
        "app_id": 'test',
        "app_secret": 'test-secret',
        "callback_url": 'http://localhost:5000/',
    }
}


def mocked_requests_get(*args, **kwargs):
    """Mock requests.get."""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == FacebookProvider.access_token_url:
        return MockResponse({'access_token': 'test-access-token'}, 200)
    elif args[0] == FacebookProvider.user_profile_url:
        return MockResponse(
            {
                'user_id': '123',
                'first_name': 'test'
            }, 200
        )


class FacebookConnectViewSetTestCase(TestCase):
    """Facebook social connect test case. """

    def setUp(self):
        self.client = APIClient()

    @override_settings(SOCIAL_MEDIA_SETTINGS=SOCIAL_MEDIA_SETTINGS)
    def test_get_auth_url(self):
        """Test to get oauth2 url for facebook."""
        api_url: str = reverse('facebook_social-auth-url')
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, f'https://www.facebook.com/v13.0/dialog/oauth?client_id={SOCIAL_MEDIA_SETTINGS["facebook"]["app_id"]}&response_type=code&display=popup&redirect_uri={SOCIAL_MEDIA_SETTINGS["facebook"]["callback_url"]}&scope=public_profile email')

    @override_settings(SOCIAL_MEDIA_SETTINGS=SOCIAL_MEDIA_SETTINGS)
    def test_auth(self):
        """Test to get user info for facebook."""
        api_url: str = reverse('facebook_social-auth')
        with patch('requests.get') as get_mock:
            get_mock.side_effect = mocked_requests_get
            response = self.client.post(api_url, {'code': 'test-code'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['first_name'], 'test')
