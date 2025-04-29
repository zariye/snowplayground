provider "snowflake" {
  user = var.username
  password = var.password
  account_name  = var.account
  organization_name = var.organization
  role     = "ACCOUNTADMIN"
}

resource "snowflake_warehouse" "compute" {
  name           = "COMPUTE"
  warehouse_size = "XSMALL"
  auto_suspend   = 60
  auto_resume    = true
}

resource "snowflake_database" "stockdata" {
  name = "STOCKDATA"
}

resource "snowflake_schema" "public" {
  database = snowflake_database.stockdata.name
  name     = "PUBLIC"
}
