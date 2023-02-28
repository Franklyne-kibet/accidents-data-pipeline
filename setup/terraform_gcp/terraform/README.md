## Terraform Overview

### Files

- `main.tf`
- `variables.tf`
- `.tfstate`
  
### Declarations

- `terraform`: configure basic Terraform settings to provision your infrastructure
  - `required_version`: minimum Terraform version to apply to your configuration
  - `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
    - `local`: stores state file locally as terraform.tfstate
  - `required_providers`: specifies the providers required by the current module

- `provider`:
  - adds a set of resource types and/or data sources that Terraform can manage
  - The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
- `resource`
  - blocks to define components of your infrastructure
  - Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
- `variable` & `locals`
  - runtime arguments and constants

### Execution steps

1. `terraform init`:
   - Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control
2. `terraform plan`:
   - Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`:
   - Asks for approval to the proposed plan, and applies changes to cloud
4. `terraform destroy`:
   - Removes your stack from the Cloud

### Execution

``` shell
# Refresh service-account's auth-token for this session

gcloud auth application-default login

# Initialize state file (.tfstate)

terraform init

# Check changes to new infra plan

terraform plan -var="project=<your-gcp-project-id>
```

``` shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

``` shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

### References

<https://learn.hashicorp.com/collections/terraform/gcp-get-started>
