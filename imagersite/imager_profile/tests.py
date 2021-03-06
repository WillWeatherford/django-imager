"""Test ImagerProfile model."""
from __future__ import unicode_literals
from django.conf import settings
from django.test import TestCase
from django.db.models import QuerySet, Manager
from .models import ImagerProfile
import random
import factory

USER_BATCH_SIZE = 40


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model in tests."""

    class Meta:
        """Establish User model as the product of this factory."""

        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.LazyAttribute(
        lambda obj: ''.join((obj.first_name, obj.last_name)))
    password = factory.PostGenerationMethodCall('set_password', 'secret')


class BuiltUserCase(TestCase):
    """Single user not saved to database, testing conditions in handlers.py."""

    def setUp(self):
        """Set up user stub."""
        self.user = UserFactory.build()

    def test_user_not_saved(self):
        """Make sure set up user has not been saved yet."""
        self.assertIsNone(self.user.id)

    def test_init_imager_profile(self):
        """Make sure set up user has not been saved yet."""
        profile = ImagerProfile(user=self.user)
        self.assertIs(profile, self.user.profile)


class OneUserCase(TestCase):
    """Inheritable base case setting up one User."""

    def setUp(self):
        """Set up User models for testing."""
        self.user = UserFactory.create()


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

    def test_active_not_contains(self):
        """Test that counting the active manager returns expected int."""
        self.assertNotIn(self.user, ImagerProfile.active.all())


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
        self.user_batch = UserFactory.create_batch(USER_BATCH_SIZE)

    def test_active_count(self):
        """Make sure that the active user count is the expected size."""
        self.assertEqual(ImagerProfile.active.count(), USER_BATCH_SIZE)

    def test_many_deleted(self):
        """Test that active.count is modified when deleting multiple users."""
        for user in random.sample(self.user_batch, USER_BATCH_SIZE // 2):
            user.delete()
        self.assertEqual(ImagerProfile.active.count(), USER_BATCH_SIZE // 2)

    def test_no_friends(self):
        """Make sure that all users start with no friends."""
        for user in self.user_batch:
            self.assertFalse(user.profile.friends.count())

    def test_friend_relationship(self):
        """Check that friends ManyToMany relationship is symmetrical."""
        user1, user2 = random.sample(self.user_batch, 2)
        user1.profile.add_friend(user2)
        self.assertTrue(user1.profile.friends.count())
        self.assertTrue(user2.profile.friends.count())

    def test_many_friends_relationship(self):
        """Check that many users can be friends with each other."""
        half = USER_BATCH_SIZE // 2
        batch1, batch2 = self.user_batch[:half], self.user_batch[half:]
        for user1 in batch1:
            for user2 in batch2:
                user1.profile.add_friend(user2)
        for user in self.user_batch:
            self.assertEqual(user.profile.friends.count(),
                             USER_BATCH_SIZE // 2)
