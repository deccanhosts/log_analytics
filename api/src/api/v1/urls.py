from django.conf.urls.defaults import *
from piston.resource import Resource
from src.api.v1.handlers.statsHandler import StatsHandler
from src.api.v1.settings import *

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

stats_handle = CsrfExemptResource( StatsHandler )

urlpatterns = patterns( '',
    url( r'^stats/$', stats_handle),
)

