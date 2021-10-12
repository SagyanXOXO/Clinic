import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application
from Interaction.routing import ws_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket' : AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})


