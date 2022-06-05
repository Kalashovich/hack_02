from django.urls import path, include
from . import views
urlpatterns = [
    path('order/', views.CreateOrderView.as_view()),
    path('own/', views.UserOrderList.as_view()),
    path('<int:pk>/', views.UpdateOrderStatusView.as_view()),
]