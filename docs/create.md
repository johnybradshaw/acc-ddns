# `POST` /create

**

## Request

+ Headers:
    No specific headers needed.

+ Url Params:
    No specific query parameters needed.

+ Body:

```json
{
    "username": "username",
    "ip": "123.12.34.56",
    "hash": "d0cd7c6fc3064382cd68e235e98c2793a2c34880b546bafaf8928f4eb24c067d"
}
```

***


## Response

+ Status: **200**

+ Body:

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
        "target": "172.232.58.199",
        "ttl_sec": 30,
        "type": "A",
        "updated": "2023-12-06T12:49:44",
        "weight": 0
    }
}
```
