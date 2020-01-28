
class PrivatePostApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@gmail.com',
            'austin12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_post(self):
        """Test retrieving list of posts"""
        # sample_post(user=self.user)
        # sample_post(user=self.user)

        res = self.client.get(POST_URL)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    















