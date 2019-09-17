from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models


def sample_user(email='teste@ciaoitalia.it', password='IlToro',):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email in successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TESTE.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creatiing a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@lala.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegana'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Tets the ingredient string representations"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Onion'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Tets the recipe string representations"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Kebab with mint sauce',
            time_minutes=30,
            price=30.50
        )

        self.assertEqual(str(recipe), recipe.title)
