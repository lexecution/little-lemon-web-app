from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from restaurant.models import Booking, Menu
from restaurant.serializers import MenuSerializer


class HomePageTest(TestCase):
    def test_home_page_renders_static_html(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'SPECIAL OFFER')
        self.assertContains(response, '/static/css/style.css')
        self.assertContains(response, '/static/img/logo.png')

    def test_root_redirects_to_home_page(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('home'))


class MenuViewTest(APITestCase):
    def setUp(self):
        self.pizza = Menu.objects.create(title='Pizza', price=200, inventory=10)
        self.cake = Menu.objects.create(title='Cake', price=150, inventory=10)
        self.pasta = Menu.objects.create(title='Pasta', price=200, inventory=10)

    def test_getall(self):
        response = self.client.get(reverse('menu-items'))
        items = Menu.objects.all()
        serializer = MenuSerializer(items, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_item(self):
        response = self.client.get(reverse('menu-item', kwargs={'pk': self.cake.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, MenuSerializer(self.cake).data)

    def test_anonymous_users_cannot_change_the_menu(self):
        payload = {'title': 'Burger', 'price': '75.60', 'inventory': 10}
        response = self.client.post(reverse('menu-items'), payload, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Menu.objects.count(), 3)

    def test_authenticated_user_can_create_update_and_delete(self):
        user = User.objects.create_user('chef', password='lemon-pass-123')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        created = self.client.post(
            reverse('menu-items'),
            {'title': 'Burger', 'price': '75.60', 'inventory': 10},
            format='json',
        )
        self.assertEqual(created.status_code, 201)
        url = reverse('menu-item', kwargs={'pk': created.data['id']})

        updated = self.client.put(
            url, {'title': 'Burger', 'price': '80.00', 'inventory': 5}, format='json'
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(Menu.objects.get(pk=created.data['id']).inventory, 5)

        deleted = self.client.delete(url)
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Menu.objects.filter(pk=created.data['id']).exists())


class BookingViewTest(APITestCase):
    payload = {
        'name': 'Adrian',
        'no_of_guests': 4,
        'booking_date': '2026-12-24T19:30:00Z',
    }

    def setUp(self):
        self.user = User.objects.create_user('guest', password='lemon-pass-123')
        self.token = Token.objects.create(user=self.user)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_booking_api_requires_authentication(self):
        url = reverse('booking-list')
        self.assertEqual(self.client.get(url).status_code, 401)
        self.assertEqual(self.client.post(url, self.payload, format='json').status_code, 401)

    def test_booking_crud_with_token(self):
        self.authenticate()
        list_url = reverse('booking-list')

        created = self.client.post(list_url, self.payload, format='json')
        self.assertEqual(created.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

        listing = self.client.get(list_url)
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.data), 1)

        detail_url = reverse('booking-detail', kwargs={'pk': created.data['id']})
        patched = self.client.patch(detail_url, {'no_of_guests': 6}, format='json')
        self.assertEqual(patched.status_code, 200)
        self.assertEqual(Booking.objects.get().no_of_guests, 6)

        self.assertEqual(self.client.delete(detail_url).status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

    def test_bearer_prefix_is_accepted_too(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')
        self.assertEqual(self.client.get(reverse('booking-list')).status_code, 200)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token not-a-real-token')
        self.assertEqual(self.client.get(reverse('booking-list')).status_code, 401)

    def test_invalid_booking_is_rejected(self):
        self.authenticate()
        bad = dict(self.payload, no_of_guests=0)
        response = self.client.post(reverse('booking-list'), bad, format='json')
        self.assertEqual(response.status_code, 400)


class AuthenticationTest(APITestCase):
    def test_register_login_and_logout_with_djoser(self):
        credentials = {'username': 'newuser', 'password': 'Str0ng-lemon-pass!'}

        register = self.client.post(
            '/auth/users/', dict(credentials, email='new@example.com'), format='json'
        )
        self.assertEqual(register.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        login = self.client.post('/auth/token/login/', credentials, format='json')
        self.assertEqual(login.status_code, 200)
        token = login.data['auth_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(self.client.get(reverse('booking-list')).status_code, 200)

        self.assertEqual(self.client.post('/auth/token/logout/').status_code, 204)
        self.assertEqual(self.client.get(reverse('booking-list')).status_code, 401)

    def test_obtain_auth_token_endpoint(self):
        User.objects.create_user('waiter', password='lemon-pass-123')
        response = self.client.post(
            reverse('api-token-auth'),
            {'username': 'waiter', 'password': 'lemon-pass-123'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_wrong_password_is_rejected(self):
        User.objects.create_user('waiter', password='lemon-pass-123')
        response = self.client.post(
            reverse('api-token-auth'),
            {'username': 'waiter', 'password': 'nope'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
