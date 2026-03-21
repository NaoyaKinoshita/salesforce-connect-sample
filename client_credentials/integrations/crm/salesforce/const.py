class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


import os  # noqa: E402
import sys  # noqa: E402

from dotenv import find_dotenv, load_dotenv  # noqa: E402

from common.utils import strtobool  # noqa: E402

load_dotenv(find_dotenv())

sys.modules[__name__] = _const()

from . import const  # noqa: E402

const.SF_CLIENT_ID = os.environ["SF_CLIENT_ID"]
const.SF_CLIENT_SECRET = os.environ["SF_CLIENT_SECRET"]
const.SF_MY_DOMAIN = strtobool(os.getenv("SF_MY_DOMAIN", "false"))
const.SF_TOKEN_ENDPOINT = (
    f"{os.environ['SF_INSTANCE_URL']}/services/oauth2/token"
    if const.SF_MY_DOMAIN
    else f"https://{os.getenv('SF_DOMAIN', 'login')}.salesforce.com/services/oauth2/token"
)
