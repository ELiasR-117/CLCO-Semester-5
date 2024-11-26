import pulumi
from pulumi_azure import core, appservice, storage

# 1. Erstelle eine Ressourcengruppe
resource_group = core.ResourceGroup('flask-app-rg')

# 2. Erstelle einen App Service Plan
app_service_plan = appservice.Plan(
    'flask-app-service-plan',
    resource_group_name=resource_group.name,
    sku={
        "tier": "Free",
        "size": "F1",
    },
)

# 3. Erstelle die Web-App
app = appservice.AppService(
    'flask-app',
    resource_group_name=resource_group.name,
    app_service_plan_id=app_service_plan.id,
    site_config={
        "app_settings": [
            {"name": "FLASK_ENV", "value": "development"},  # Flask-Umgebungsvariable
        ]
    },
    https_only=True, # https erzwingen
)

# 4. Erstelle ein Storage Account
storage_account = storage.Account(
    'flask-app-storage',
    resource_group_name=resource_group.name,
    account_tier='Standard',
    account_replication_type='LRS',
)

# 5. Erstelle einen Blob Container
blob_container = storage.Container(
    'flask-app-container',
    storage_account_name=storage_account.name,
)

# 6. Exportiere die URLs
pulumi.export('app_url', app.default_site_hostname.apply(lambda hostname: f"https://{hostname}"))
pulumi.export('blob_url', blob_container.url)
