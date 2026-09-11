"""
URL configuration for ping_me_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from account.views import AccountViewSet
from ping_me_api.views import custom_404, custom_500
from server.views import ChannelViewSet, ServerCategoryViewSet, ServerViewSet
from webchat.views import MessageViewSet

# Register API endpoints with the router
router = DefaultRouter()
router.register(r"api/servers", ServerViewSet, basename="servers")
router.register(r"api/categories", ServerCategoryViewSet, basename="categories")
router.register(r"api/channels", ChannelViewSet, basename="channels")
router.register(r"api/messages", MessageViewSet, basename="messages")
router.register(r"api/account", AccountViewSet, basename="account")


#: The list of URL patterns for the project.
#:
#: Includes admin, API docs, JWT authentication, and all registered API endpoints.
urlpatterns = [
    # Django admin panel
    path("admin/", admin.site.urls),
    # OpenAPI schema and Swagger UI
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/schema/ui/", SpectacularSwaggerView.as_view()),
    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls

# custom error handlers

handler404 = 'ping_me_api.views.custom_404'
handler500 = 'ping_me_api.views.custom_500'