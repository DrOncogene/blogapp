from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

# Create your tests here.

class BlogTests(TestCase):

  def setUp(self):
    self.user = get_user_model().objects.create_user(
      username = 'rash',
      email = 'rash@example.com',
      password = 'rasheed'
    )

    self.post = Post.objects.create(
      title= 'A good title',
      author= self.user,
      body= 'Nice body'
    )

  def test_string_representation(self):
    post = Post(title='A simple title')
    self.assertEqual(str(post), post.title)

  def test_post_content(self):
    self.assertEqual(f'{self.post.title}', 'A good title')
    self.assertEqual(f'{self.post.author}', 'rash')
    self.assertEqual(f'{self.post.body}', 'Nice body')

  def test_post_list_view(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Nice body')
    self.assertTemplateUsed(response, 'blogapp/home.html')

  def test_post_detail_view(self):
    response = self.client.get('/post/1/')
    no_response = self.client.get('/post/100000/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(no_response.status_code, 404)
    self.assertContains(response, 'A good title')
    self.assertTemplateUsed(response, 'blogapp/post_detail.html')