from datetime import date

from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


def index(request):
    """Home page: serves the static HTML template."""
    return render(request, 'index.html', {'current_year': date.today().year})


class MenuItemsView(generics.ListCreateAPIView):
    """GET lists all menu items, POST creates a new one."""

    # Anyone can read the menu; changing it requires a token.
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    """GET retrieves, PUT/PATCH updates and DELETE removes one menu item."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Table booking API: full CRUD, restricted to authenticated users."""

    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
