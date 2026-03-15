class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sys.modules[__name__] = _const()

from . import const

const.SF_CLIENT_ID = os.environ["SF_CLIENT_ID"]
const.SF_USERNAME = os.environ["SF_USERNAME"]
const.SF_PRIVATE_KEY_FILE = os.environ["SF_PRIVATE_KEY_FILE"]
const.SF_DOMAIN = os.getenv("SF_DOMAIN", "login")
const.SF_TOKEN_ENDPOINT = (
    f"https://{const.SF_DOMAIN}.salesforce.com/services/oauth2/token"
)
const.SF_AUDIENCE = f"https://{const.SF_DOMAIN}.salesforce.com"
