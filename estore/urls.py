"""estore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
# from api.views import ReviewDeleteView
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="estore",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router=DefaultRouter()
router.register("product",views.ProductView,basename="product")
router.register("cart",views.CartsView,basename="cart")
# router.register("review",views.ReviewDeleteView,basename="review")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/',obtain_auth_token),
    path("review/<int:pk>/",views.ReviewDeleteView.as_view()),
    path("jwt/token/",TokenObtainPairView.as_view()),
    path("jwt/token/refresh/",TokenRefreshView.as_view()),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]+router.urls
