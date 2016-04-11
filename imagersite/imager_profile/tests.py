"""Test ImagerProfile model."""
from __future__ import unicode_literals
from django.conf import settings
from django.test import TestCase
from django.db.models import QuerySet, Manager
from .models import ImagerProfile
import factory

USER_TEST_BATCH_SIZE = 40


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model in tests."""

    class Meta:
        """Establish User model as the product of this factory."""

        model = settings.AUTH_USER_MODEL

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.LazyAttribute(
        lambda obj: ''.join((obj.first_name, obj.last_name)))


class OneUserCase(TestCase):
    """Inheritable base case setting up one User."""

    def setUp(self):
        """Set up User models for testing."""
        self.user = UserFactory.create()
        self.user.set_password('secret')


class DeletedUserCase(OneUserCase):
    """Inheritable base case setting up one User, then deleting it."""

    def setUp(self):
        """Set up User models for testing."""
        super(DeletedUserCase, self).setUp()
        self.user.delete()

    def test_no_profile_pk_after_delete(self):
        """Test that profile is deleted with User, losing its primary key."""
        self.assertIsNone(self.user.profile.pk)

    def test_profile_is_active_false(self):
        """Test that profile of deleted User is not active."""
        self.assertFalse(self.user.profile.is_active)

    def test_active_count(self):
        """Test that counting the active manager returns expected int."""
        self.assertFalse(ImagerProfile.active.count())


# Add tests manipulating profile attributes
class BasicUserProfileCase(OneUserCase):
    """Simple test case for Photos."""

    def test_user_has_profile(self):
        """Test that newly created User does have a profile attached."""
        self.assertTrue(self.user.profile)

    def test_profile_pk(self):
        """Test that newly created User's profile has a primary key."""
        self.assertIsInstance(self.user.profile.pk, int)
        self.assertTrue(self.user.profile.pk)

    def test_profile_is_active(self):
        """Test that profile of new User is active."""
        self.assertTrue(self.user.profile.is_active)

    def test_profile_is_active_false_2(self):
        """Test that profile of deactivated User is not active."""
        self.user.is_active = False
        self.assertFalse(self.user.profile.is_active)

    def test_profile_active_manager(self):
        """Test that active attr is a Manager class."""
        self.assertIsInstance(ImagerProfile.active, Manager)

    def test_profile_active_query(self):
        """Test that active manager can give a QuerySet."""
        self.assertIsInstance(ImagerProfile.active.all(), QuerySet)

    def test_active_count(self):
        """Test that counting the active manager returns expected int."""
        self.assertEqual(ImagerProfile.active.count(), 1)


class ManyUsersCase(TestCase):
    """Test cases where many Users are registered."""

    def setUp(self):
        """Add many Users to the test."""
        self.user_batch = UserFactory.create_batch(USER_TEST_BATCH_SIZE)
