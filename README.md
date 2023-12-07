# DDNS on Akamai Connected Cloud

[![Docker](https://github.com/johnybradshaw/acc-ddns/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/johnybradshaw/acc-ddns/actions/workflows/docker-publish.yml)

This is a small Dynamic DNS Server (DDNS) that can be used for labs and demos. It will create DNS A records in a second Akamai Connected Cloud account pointing to a specific IP.

## Limitations

This has not been written as a production implementation of Dynamic DNS (DDNS) on the Akamai Connected Cloud and it is missing important security controls.

This code is provided as is, without warranty, and should not be used in a production scenario.

## How to use

You can run the docker image by providing the following environment variables:

```bash
# .env
SECRET_KEY=
LINODE_API_KEY=
DOMAIN_ID=
# Lumigo configuration (Optional)
LUMIGO_TRACER_TOKEN=
OTEL_SERVICE_NAME=
AUTOWRAPT_BOOTSTRAP=
```

### Run the container

```bash
docker run --name ddns_acc \
  -e SECRET_KEY=VALUE \
  -e LINODE_API_KEY=VALUE \
  -e DOMAIN_ID=VALUE \
  -e LUMIGO_TRACER_TOKEN= \
  -e OTEL_SERVICE_NAME= \
  -e AUTOWRAPT_BOOTSTRAP= \
  -p 8000:8000 \
  --restart-always \
  -d \
  ghcr.io/johnybradshaw/acc-ddns:latest
```

## Logging

The application logs to `stdout` but can optionally be configured to emit traces to [Lumigo](https://platform.lumigo.io/) by updating the environment variables

### Log Example

#### Start up

```bash
[2023-12-07 14:33:06 +0000] [42622] [INFO] Initializing routes...
[2023-12-07 14:33:06 +0000] [42622] [INFO] Secret key: abCD**** [8]
[2023-12-07 14:33:06 +0000] [42622] [INFO] Linode API key: f222************************************************************ [64]
[2023-12-07 14:33:06 +0000] [42622] [INFO] Domain ID: 1274*** [7]
```

#### Valid Request

```bash
[2023-12-07 14:33:09 +0000] [42623] [INFO] [127.0.0.1] Request data: {'username': 'username', 'ip': '123.12.34.56'}
```

## API Endpoints

### Requests

The following is a properly formed request:

```bash
curl -X "POST" "http://127.0.0.1:8000/create" \
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
