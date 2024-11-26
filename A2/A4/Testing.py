import unittest
import pulumi_azure as azure
import pulumi
from pulumi_azure.bot import web_app
from pulumi_azure_native.web import app_service_plan


class TestAzureResources(unittest.TestCase):
    def test_app_service_plan_tier(self):
        plan = azure.appservice.Plan.get("example-appservice-plan", "example-appservice-plan", resource_group_name="example-rg")
        self.assertEqual(plan.sku.tier, "Free")

class TestWebAppIntegration(unittest.TestCase):
    def test_web_app_association(self):
        web_app = azure.appservice.WebApp.get("example-webapp", "example-webapp", resource_group_name="example-rg")
        self.assertEqual(web_app.app_service_plan_id, app_service_plan.id)
        
        
class TestEndToEnd(unittest.TestCase):
    def test_deployment(self, requests=None):
        web_app_url = pulumi.Output.all(web_app.default_site_hostname).apply(lambda x: x[0])
        response = requests.get(f"http://{web_app_url}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World", response.text)