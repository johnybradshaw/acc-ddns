# DDNS on Akamai Connected Cloud

[![Docker](https://github.com/johnybradshaw/acc-ddns/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/johnybradshaw/acc-ddns/actions/workflows/docker-publish.yml)

This is a small Dynamic DNS Server (DDNS) that can be used for labs and demos. It will create DNS A records in a second Akamai Connected Cloud account pointing to a specific IP.

## Limitations

This has not been written as a production implementation of Dynamic DNS (DDNS) on the Akamai Connected Cloud and it is missing important security controls.

This code is provided as is, without warranty, and should not be used in a production scenario.

## How to use

You can run the docker image by providing the following environment variables:

```bash
SECRET_KEY=
LINODE_API_KEY=
DOMAIN_ID=
```

Run the container

```bash
docker run --name ddns_acc --env-file=.env -p 8000:80 ghcr.io/johnybradshaw/acc-ddns:latest
```

## API Endpoints

### Requests

The following is a properly formed request:

```bash
curl -X "POST" "http://127.0.0.1:9001/create" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "ip": "123.12.34.56",
  "username": "username",
  "hash": "d0cd7c6...067d"
}'
```

#### Creating the hash

A hash must be passed with each request to validate the message. It is formed of the body message seperated by a - and hashed with the secret set at both ends.

```bash
#pseudocode
sha256("${username}-${$ip}-${secret}")
```

### DDNS Record Create/Update

`POST` - `/create`

#### Content

```json
{
  "username": "username",
  "ip": "123.12.34.56",
  "hash": "d0cd...067d"
}
```

#### Response - 200

```json
{
  "response": {
    "created": "2023-12-06T12:49:44",
    "id": 1234567,
    "port": 0,
    "priority": 0,
    "protocol": null,
    "service": null,
    "tag": null,
    "target": "123.12.34.56",
    "ttl_sec": 30,
    "type": "A",
    "updated": "2023-12-06T12:49:44",
    "weight": 0
  }
}
```
