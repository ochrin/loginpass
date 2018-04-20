from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend


class Twitter(OAuthBackend):
    OAUTH_TYPE = '1.0'
    OAUTH_NAME = 'twitter'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.twitter.com/1.1/',
        'request_token_url': 'https://api.twitter.com/oauth/request_token',
        'access_token_url': 'https://api.twitter.com/oauth/access_token',
        'authorize_url': 'https://api.twitter.com/oauth/authenticate',
    }

    def profile(self):
        url = 'account/verify_credentials.json'
        params = {
            'skip_status': True,
            'include_email': True
        }
        resp = self.get(url, params=params)
        data = resp.json()
        params = {
            'sub': data['id_str'],
            'name': data['name'],
            'email': data.get('email'),
            'locale': data.get('lang'),
            'picture': data.get('profile_image_url_https'),
            'preferred_username': data.get('screen_name'),
        }
        username = params['preferred_username']
        if username:
            params['profile'] = 'https://twitter.com/{}'.format(username)
        return UserInfo(params)