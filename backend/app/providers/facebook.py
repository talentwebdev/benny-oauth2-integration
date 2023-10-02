import requests

from app.providers.base import BaseProvider, SocialAuthUser, social_provider


@social_provider
class FacebookProvider(BaseProvider):
    """Facebook social authentication provider class."""

    id = 'facebook'
    name = 'Facebook'
    user_profile_url = "https://graph.facebook.com/v13.0/me"
    access_token_url = "https://graph.facebook.com/oauth/access_token"

    def get_token(self, code: str) -> str:
        """Parse code to access token string.

        Arguments:
            code(str): OAuth2 authentication code

        Return:
            str: Access token string
        """
        payload = {
            "client_id": self.APP_ID,
            "client_secret": self.APP_SECRET,
            "code": code,
            "redirect_uri": self.CALLBACK_URL,
        }

        response = requests.get(self.access_token_url, params=payload)
        data = response.json()
        self.access_token = data['access_token']
        return self.access_token

    def get_user_info(self) -> SocialAuthUser:
        """Get social user's info.

        Return:
            SocialAuthUser: User's info.
        """
        if not self.access_token:
            raise ValueError

        payload = {
            "access_token": self.access_token,
            "fields": "first_name,last_name,name",
        }

        response = requests.get(self.user_profile_url, params=payload)
        if response.status_code != 200:
            raise ValueError

        data = response.json()
        return data

    def get_oauth2_url(self) -> str:
        """Get Facebook outh2 authentication URL.

        Return:
            str: URL to authenticate oauth2
        """
        return f"https://www.facebook.com/v13.0/dialog/oauth?client_id={self.APP_ID}&response_type=code&display=popup&redirect_uri={self.CALLBACK_URL}&scope=public_profile email"
