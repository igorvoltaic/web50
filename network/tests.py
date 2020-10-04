from django.test import TestCase
from django.test import Client

from .models import Post, User


class PostTestCase(TestCase):

    def setUp(self):

        # create users
        foo = User.objects.create_user(username="foo", email="foo@exmaple.com",
                                       password="123")
        bar = User.objects.create_user(username="bar", email="bar@exmaple.com",
                                       password="123")

        # create posts
        p1 = Post.objects.create(user=foo, body="hello world")
        p2 = Post.objects.create(user=bar, body="test post")

    def test_fetch_posts(self):
        c = Client()
        r = c.get("/posts")
        self.assertEqual(200, r.status_code)

        # posts go in reverse order. latest first
        self.assertIn("test", r.json()[0]['body'])
        self.assertIn("world", r.json()[1]['body'])

        r = c.put("/posts")
        self.assertEqual(400, r.status_code)

    def test_likes_count(self):
        p1 = Post.objects.get(pk=1)
        p2 = Post.objects.get(pk=2)
        foo = User.objects.get(pk=1)

        p1.liked_by.add(foo)
        p1.save()
        self.assertEqual(p1.liked_by.count(), 1)
        self.assertEqual(p2.liked_by.count(), 0)

    def test_followers_count(self):
        foo = User.objects.get(username="foo")
        bar = User.objects.get(username="bar")

        foo.followers.add(bar)
        foo.save()
        self.assertEqual(foo.followers.count(), 1)
        self.assertEqual(foo.follow.count(), 0)
        self.assertEqual(bar.followers.count(), 0)
        self.assertEqual(bar.follow.count(), 1)

    def test_valid_follow(self):
        foo = User.objects.get(username="foo")
        self.assertFalse(foo.valid_follow(foo))

    def test_post_like_unlike(self):
        foo = User.objects.get(pk=1)
        post = Post.objects.get(pk=1)
        c = Client()

        r = c.put(f"/posts/{post.id}")
        self.assertEqual(r.status_code, 400)
        r = c.post(f"/posts/{post.id}")
        self.assertEqual(r.status_code, 400)

        c.login(username='foo', password='123')

        r = c.put(f"/posts/{foo.id}", '{ "like": "true" }')
        self.assertEqual(r.status_code, 204)
        r = c.put(f"/posts/{foo.id}", '{ "unlike": "true" }')
        self.assertEqual(r.status_code, 204)


class UserTestCase(TestCase):

    def setUp(self):

        # create users
        foo = User.objects.create_user(username="foo", email="foo@exmaple.com",
                                       password="123")
        baz = User.objects.create_user(username="baz", email="baz@exmaple.com",
                                       password="123")
        boo = User.objects.create_user(username="boo", email="boo@exmaple.com",
                                       password="123")

        # create posts
        # p1 = Post.objects.create(user=foo, body="hello world")
        # p2 = Post.objects.create(user=bar, body="test post")

        # follow
        foo.followers.add(baz)
        foo.followers.add(boo)

    def test_profile(self):
        foo = User.objects.get(pk=1)
        c = Client()
        r = c.get(f"/profile/{foo.id}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["followers_names"], ["baz", "boo"])
        self.assertEqual(r.json()["followers_count"], 2)
        self.assertEqual(r.json()["follow_count"], 0)
        self.assertEqual(r.json()["follow_names"], [])
        r = c.get("/profile/404")
        self.assertEqual(r.status_code, 404)

    def test_follow_unfollow(self):
        foo = User.objects.get(pk=1)
        c = Client()
        r = c.put(f"/profile/{foo.id}")
        self.assertEqual(r.status_code, 400)
        c.login(username='baz', password='123')
        r = c.put(f"/profile/{foo.id}")
        self.assertIn("removed", r.json()['message'])
        r = c.put(f"/profile/{foo.id}")
        self.assertIn("added", r.json()['message'])


