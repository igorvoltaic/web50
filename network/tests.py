from django.test import TestCase

from .models import Post, User


class PostTestCase(TestCase):

    def setUp(self):

        #create users
        foo = User.objects.create_user(username="foo", email="foo@exmaple.com", password="123")
        bar = User.objects.create_user(username="bar", email="bar@exmaple.com", password="123")

        # create posts
        p1 = Post.objects.create(user=foo, body="hello world")
        p2 = Post.objects.create(user=bar, body="test post")


    def test_likes_count(self):
        p1 = Post.objects.get(pk=1)
        foo = User.objects.get(pk=1)
        p1.liked_by.add(foo)
        p1.save()
        self.assertEqual(p1.liked_by.count(), 1)

    def test_likes_none(self):
        p2 = Post.objects.get(pk=2)
        self.assertEqual(p2.liked_by.count(), 0)

    def test_followers_count(self):
        foo = User.objects.get(username="foo")
        bar = User.objects.get(username="bar")
        foo.followers.add(bar)
        foo.save()
        self.assertEqual(foo.followers.count(), 1)

    def test_valid_follow(self):
        foo = User.objects.get(username="foo")
        bar = User.objects.get(username="bar")
        self.assertFalse(foo.valid_follow(foo))

