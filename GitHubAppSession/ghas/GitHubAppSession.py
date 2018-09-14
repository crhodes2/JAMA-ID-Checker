from datetime import datetime, timedelta
from jwt import encode as jwt_encode
from requests import Session

class GitHubAppSession(Session):
    """This class manages interacting with the GitHub api as a GitHub App.
    Using your app's id and private pem we craft a Json Web Token (jwt) to 
    request an access token that lets us work with the api.
    After this object has authenticated just use the request.Session package's
    methods to preform your requests.

    Should be used as a context manager.
    """
    def __init__(self, app_id, private_key, installation_id=None):
        super(GitHubAppSession, self).__init__()
        self.headers.update({'User-Agent': 'GitHub Application build with Python\'s Requests library'})
        self.headers.update({'Accept': 'application/vnd.github.machine-man-preview+json'})
        self.app_id = app_id
        self.pk = private_key
        self.jwt = None
        self.installation_id = installation_id
        # TODO: Handle token expiration in case there is some activity that takes longer than 1 hour.
        self.token_expires_at = None   

    def update_bearer(self, bearer_token):
        self.headers.update({'Authorization': 'Bearer {}'.format(bearer_token.decode('ascii'))})

    def update_auth(self, auth_token):
        self.headers.update({'Authorization': 'token {}'.format(auth_token)})

    def update_agent(self, agent_string):
        self.headers.update({'User-Agent': '{}'.format(agent_string)})

    def create_jwt(self):
        payload = {
            # Issued at time
            'iat': datetime.now().timestamp(),
            # JWT expiration time (10 minute maximum)
            'exp': (datetime.now() + timedelta(minutes=9)).timestamp(),
            # GitHub App's identifier
            'iss': self.app_id
        }
        return jwt_encode(payload, self.pk, algorithm='RS256')

    def request_token(self):
        resp = None
        if self.installation_id:
            resp = self.post("https://api.github.com/installations/{}/access_tokens".format(self.installation_id))
            if resp.status_code == 201:
                self.update_auth(resp.json().get('token'))
                self.token_expires_at = datetime.strptime(resp.json().get('expires_at'), '%Y-%m-%dT%H:%M:%SZ') 


    def __enter__(self):
        self.jwt = self.create_jwt()
        self.update_bearer(self.jwt)
        self.request_token()
        return self

    def __exit__(self, *args):
        self.close()