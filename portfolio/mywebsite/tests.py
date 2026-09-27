from django.core import mail
from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class SendMessageTests(TestCase):
	def test_post_sends_message_with_reply_to(self):
		response = self.client.post(reverse('send_message'), {
			'name': 'Test Sender',
			'email': 'sender@example.com',
			'subject': 'Portfolio contact',
			'message': 'Hello',
		})

		self.assertRedirects(response, '/#contact', fetch_redirect_response=False)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].reply_to, ['sender@example.com'])
		self.assertIn('Hello', mail.outbox[0].body)
		self.assertIn('Test Sender', mail.outbox[0].body)
		self.assertEqual(
			[str(message) for message in get_messages(response.wsgi_request)],
			['Your message has been sent. Thank you!'],
		)

	def test_invalid_email_does_not_send_message(self):
		response = self.client.post(reverse('send_message'), {
			'name': 'Test Sender',
			'email': 'not-an-email',
			'subject': 'Portfolio contact',
			'message': 'Hello',
		})

		self.assertRedirects(response, '/#contact', fetch_redirect_response=False)
		self.assertEqual(len(mail.outbox), 0)
		self.assertEqual(
			[str(message) for message in get_messages(response.wsgi_request)],
			['Please enter a valid email address.'],
		)

	def test_smtp_error_shows_failure_instead_of_success(self):
		with patch('mywebsite.views.EmailMessage.send', side_effect=OSError('SMTP unavailable')):
			response = self.client.post(reverse('send_message'), {
				'name': 'Test Sender',
				'email': 'sender@example.com',
				'subject': 'Portfolio contact',
				'message': 'Hello',
			})

		self.assertRedirects(response, '/#contact', fetch_redirect_response=False)
		self.assertEqual(
			[str(message) for message in get_messages(response.wsgi_request)],
			['Your message could not be sent. Please try again later.'],
		)

	def test_get_is_not_allowed(self):
		response = self.client.get(reverse('send_message'))

		self.assertEqual(response.status_code, 405)
