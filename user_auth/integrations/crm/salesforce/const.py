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

load_dotenv(find_dotenv())

sys.modules[__name__] = _const()

from . import const  # noqa: E402

const.SF_USERNAME = os.environ["SF_USERNAME"]
const.SF_PASSWORD = os.environ["SF_PASSWORD"]
const.SF_SECURITY_TOKEN = os.environ["SF_SECURITY_TOKEN"]
const.SF_DOMAIN = os.getenv("SF_DOMAIN", "login")
