__version = (1, 7, 3)

__version__ = version = '.'.join(map(str, __version))
__project__ = PROJECT = __name__

from .manager import JSONRPCResponseManager
from .dispatcher import Dispatcher
from .jsonrpc import JSONRPCResponse

dispatcher = Dispatcher()

# lint_ignore=W0611,W0401
