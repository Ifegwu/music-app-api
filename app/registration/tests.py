import json
from django.test import TestCase
from django.core import mail


class AuthTestCase(TestCase):

    def query(self, query: str = None):
        # Method to run all queries and mutations for tests.
        body = dict()
        body['query'] = query
        response = self.client.post(
            "/api/", json.dumps(body),
            content_type='application/json')
        json_response = json.loads(response.content.decode())
        return json_response

    def test_user_can_register_for_account(self):
        register_user_query = '''
        mutation {{
          createUser(username:"{username}" email: "{email}", password: "{password}"){{
            user {{
              email,
              username
            }}
            message
          }}
        }}

        '''
        response = self.query(register_user_query.format(
            username="testuser",
            email="user@testuser.com",
            password="password123"
        ))
        data = response.get('data')
        self.assertEqual(data["createUser"]["message"],
                         "Successfully created user, testuser")

    def test_send_email(self):
        mail.send_mail(
            'Account Activation', 'Click below button to confirm your email',
            'confirm_test@test.com', ['user@testuser.com'],
            fail_silently=False,
        )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Account Activation')