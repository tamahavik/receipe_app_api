from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
    
        email = "test@gmail.com"
        password = "123456Aa"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalize"""
        email = "havik.priyatama@GMAIL.com"
        user = get_user_model().objects.create_user(email, '12312312')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """create new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '1234')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'asdas@gmail.com', 
            '123123'
        ) 
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)