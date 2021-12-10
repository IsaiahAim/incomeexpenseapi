from .test_setup import  TestSetUp


class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'], self.user_data['email'])

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        self.client.post(self.login_url)
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 201)




