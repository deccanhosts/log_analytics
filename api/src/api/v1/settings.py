from piston.utils import Mimer
from src.utils import pbutils
Mimer.register(pbutils.loadPb, ('application/octet-stream'))
from src.utils import customLogger
apiLogger = customLogger.getApiLogger('api_trace.log')

