from django.test import TestCase, Client
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse


# class AdminSiteTests(TestCase):

#   def setUp(self):
#     self.client = Client()
#     self.admin_user = User.objects.create_superuser(
#       email='test@gmail.com',
#       password='austin12345'
#     )
#     self.client.force_login(self.admin_user)
#     self.user = User.objects.create_user(
#       email='test@gmail.com',
#       password='austin12345',
#       name = 'We test user full name'
#     )

#   def test_users_listed(self):
#     """Test that users are listed on user page"""
#     url = reverse('admin:core_user_changelist')
#     res = self.client.get(url)

#     self.assertContain(res, self.user.name)
#     self.assertContain(res, self.user.email)


#   def test_user_change_page(self):
#     """ Test that the user edit page works"""
#     url = reverse('admin:core_user_change', args=[self.user.id])
#     res = self.client.get(url)

#     self.assertEqual(res.status_code, 200)



    # def test_create_user_page(self):
    #   """ Test that the create user page works"""
    #   url = reverse('admin:core_user_add')
    #   res = self.client.get(url)

    #   self.assertEqual(res.status_code, 200)

