import django
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter,ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from mysite import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})









