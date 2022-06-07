"""main_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Main project",
      default_version='v1',
      description="This is test main project",
      terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="akkauntsky@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/orders/', include('order.urls')),
    path('api/v1/ratings/', include('rating.urls')),
    path('api/v1/order/', include('basket.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls:

#urlpatterns = [
    # path('register/', views.RegistrationApiView.as_view()),
    # path('activate/<uuid:activation_code>/', views.ActivationView.as_view()),
    # path('login/', views.LoginApiView.as_view()),
    #
    # path('logout/', views.LogoutAPIView.as_view()),
    # path('refresh/', TokenRefreshView.as_view()),
    #
    # path('change-password/', views.NewPasswordView.as_view()),
    # path('reset-password/', views.ResetPasswordView.as_view()),
# ]
# urlpatterns = [
#     path('order/', views.CreateOrderView.as_view()),
#     path('own/', views.UserOrderList.as_view()),
#     path('<int:pk>/', views.UpdateOrderStatusView.as_view()),
# ]
