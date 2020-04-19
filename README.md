# tfstated
Lightweight Terraform state server, intended for use with Terraform [HTTP backend](https://www.terraform.io/docs/backends/types/http.html)

## Docker
A Docker container for tfstated is available from Docker Hub
```shell
docker run -d --name tfstated \
  -e TFSTATED_USERNAME=terraform \
  -e TFSTATED_PASSWORD=terraform \
  -e TFSTATED_DATA_DIR=/tfstate \
  -p 8000:8000 -v /data:/tfstate \
  ivoronin/tfstated:latest
```

## Example terraform config
```terraform
terraform {
  backend "http" {
    address        = "http://127.0.0.1:8000/state"
    lock_address   = "http://127.0.0.1:8000/state"
    unlock_address = "http://127.0.0.1:8000/state"
    username       = "terraform"
    password       = "terraform"
  }
}
```
