from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a test post body.',
            status='draft'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.body, 'This is a test post body.')
        self.assertEqual(self.post.status, 'draft')
        self.assertEqual(self.post.author.username, 'testuser')

    def test_get_absolute_url(self):
        expected_url = f"/posts/{self.post.publish.year}/{self.post.publish.month:02}/{self.post.publish.day:02}/{self.post.slug}/"
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_default_status(self):
        new_post = Post.objects.create(
            title='Another Post',
            slug='another-post',
            author=self.user,
            body='Another test post body.'
        )
        self.assertEqual(new_post.status, 'draft')

    def test_post_ordering(self):
        post2 = Post.objects.create(
            title='Second Post',
            slug='second-post',
            author=self.user,
            body='Second test post body.',
            publish=timezone.now() + timezone.timedelta(days=1)
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)  # post2 должно быть первым из-за сортировки '-publish'
        self.assertEqual(posts[1], self.post)
