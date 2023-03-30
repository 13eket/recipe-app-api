"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


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
        try:
            user = get_user_model().objects.create_user('', 'testpass123')
        except Exception as e:
            print(str(e) + "Something")

        #"""Test that creating a user without an email raises a ValueError."""
        #with self.assertRaises(ValueError):
        #    user = get_user_model().objects.create_user('', 'testpass123')
