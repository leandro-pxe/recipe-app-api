from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test the login is required to access the endpoint"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the privated ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='saci_perere@brazil.com',
            password='AcucaVaiTePegar'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving the ingredients list by authenticated users"""
        Ingredient.objects.create(user=self.user, name='Onion')
        Ingredient.objects.create(user=self.user, name='Garlic')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test the ingredients are limited to the logged user"""
        user2 = get_user_model().objects.create_user(
            'lala@lele.com'
            'balaclava'
        )

        Ingredient.objects.create(user=user2, name='Onion')
        ing_mine = Ingredient.objects.create(user=self.user, name='Garlic')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing_mine.name)

    # def test_create_ingredients_successful(self):
    #     payload = {'name': 'Rice'}
    #     res = self.client.post(INGREDIENTS_URL, payload)
    #
    #     exists = Ingredient.objects.filter(
    #         user=self.user,
    #         name=payload['name']
    #     ).exists()
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertTrue(exists)
    #
    # def test_create_ingredients_invalid(self):
    #     payload = {'name': ''}
    #
    #     res = self.client.post(INGREDIENTS_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
