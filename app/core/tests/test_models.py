"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email in successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
        ]
        password = 'testpass123'

        for sample_email in sample_emails:
            caps_email = sample_email[0]
            normalized_email = sample_email[1]
            user = get_user_model().objects.create_user(caps_email, password)

            self.assertEqual(user.email, normalized_email)
            self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='',
                                                 password='testpass123')

    def test_new_super_use_with_email_successful(self):
        """Test if super user created successfully."""
        user = get_user_model().objects.create_superuser("test@example.com",
                                                         "testpass123")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal(5.10),
            description="Sample recipe description"
        )

        self.assertEqual(str(recipe), recipe.title)
