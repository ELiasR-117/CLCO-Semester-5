import subprocess
from unittest import TestCase
import requests

class HelloWorldEndToEndTests(TestCase):
    def test_stack_deployment(self):
        """Stellt sicher, dass der Pulumi-Stack erfolgreich bereitgestellt wird."""
        result = subprocess.run(["pulumi", "up", "--yes", "--skip-preview"], capture_output=True, text=True)
        self.assertIn("Resources:", result.stdout)
        self.assertNotIn("error", result.stdout.lower())
        self.assertNotIn("failed", result.stdout.lower())

    def test_webapp_hello_world(self):
        """Überprüft, ob die WebApp 'Hello World' als HTML ausgibt."""
        # Holen der WebApp-URL aus den Pulumi-Outputs
        result = subprocess.run(["pulumi", "stack", "output", "webAppUrl"], capture_output=True, text=True)
        web_app_url = result.stdout.strip()

        # HTTP-GET-Anfrage an die WebApp senden
        response = requests.get(web_app_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World", response.text)  # Erwartet, dass die HTML-Seite "Hello World" enthält
