from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    # Static HTML home page
    path('', views.index, name='home'),
    # Menu API
    path('menu/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-item'),
    # Table booking API (token protected)
    path('booking/', include(router.urls)),
    # Token authentication
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
