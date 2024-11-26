import pulumi
import pulumi.runtime
from unittest import TestCase

# Pulumi-Mocks für Integrationstests
class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args):
        return [f"{args.name}_id", args.inputs]

    def call(self, args):
        return {}

pulumi.runtime.set_mocks(MyMocks())

class HelloWorldIntegrationTests(TestCase):
    def test_webapp_blob_connection(self):
        """Testet, ob die WebApp auf den korrekten Blob Storage zeigt."""
        from main import webApp, storageAccount, blobContainer, codeBlob
        expected_url = (
            f"https://{storageAccount.name}.blob.core.windows.net/"
            f"{blobContainer.name}/{codeBlob.blob_name}"
        )
        app_settings = {setting["name"]: setting["value"] for setting in webApp.site_config.app_settings}
        self.assertEqual(app_settings.get("WEBSITE_RUN_FROM_PACKAGE"), expected_url)

    def test_webapp_runtime(self):
        """Testet, ob die WebApp mit der richtigen Python-Laufzeit konfiguriert ist."""
        from main import webApp
        self.assertEqual(webApp.site_config.linuxFxVersion, "PYTHON|3.8")
