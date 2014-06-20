
import base64

class Context(dict):

    def authorizer(self, scheme, resource, action):
        if scheme == "Basic":
            if self.basic:
                return self.basic
            else:
                raise Exception("Must call set_basic(email, password) first")
            
        elif scheme == "BitVault-Token":
            if self.api_token:
                return self.api_token
            else:
                raise Exception("Must call set_token(api_token) first")

    def set_basic(self, email, password):
        string = ':'.join([email, password])
        self.basic = base64.b64encode(string)

    def set_token(self, token):
        self.api_token = token

