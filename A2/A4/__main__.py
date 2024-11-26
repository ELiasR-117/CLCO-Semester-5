import pulumi
import pulumi_azure as azure
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi import asset

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("resource_group")

# Create an Azure resource (Storage Account)
account = storage.StorageAccount(
    "sa",
    resource_group_name=resource_group.name,
    sku={
        "name": storage.SkuName.STANDARD_LRS,
    },
    kind=storage.Kind.STORAGE_V2,
)

# Export the primary key of the Storage Account
primary_key = (
    pulumi.Output.all(resource_group.name, account.name)
    .apply(
        lambda args: storage.list_storage_account_keys(
            resource_group_name=args[0], account_name=args[1]
        )
    )
    .apply(lambda accountKeys: accountKeys.keys[0].value)
)

app_service_plan = azure.appservice.Plan("example-appservice-plan",
    resource_group_name=resource_group.name,
    kind="App",
    sku=azure.appservice.PlanSkuArgs(tier="Free", size="F1"))

web_app = azure.appservice.WebApp("example-webapp",
    resource_group_name=resource_group.name,
    app_service_plan_id=app_service_plan.id)

app_insights = azure.insights.ApplicationInsights("example-appinsights",
    resource_group_name=resource_group.name,
    application_type="Web")



app_dir = "./app"
app_archive = asset.FileArchive(app_dir)

##app_deployment = azure.appservice.AppService("example-webapp-deployment",
    ##resource_group_name=resource_group.name,
    ##app_service_plan_id=app_service_plan.id,
    ##app_zip=app_archive)


pulumi.export("webAppUrl", web_app.default_site_hostname)

pulumi.export("primary_storage_key", primary_key)

