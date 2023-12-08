# Kubernetes Installation

The Dynamic DNS on Akamai Connected Cloud application can be deployed to Kubernetes or [LKE](https://www.linode.com/products/kubernetes/) with the yaml files in this directory. It is configured to use an Issuer rather than a Cluster-Issuer (however that can be changed).

## Configuration

Update `secrets.yaml` with base64 encoded secrets, e.g. `echo -n "Your_DomainID" | base64`

```yaml
  LINODE_API_KEY: ""
  DOMAIN_ID: ""
  SECRET_KEY: ""
```

Update `ingress.yaml` by replacing `<<YOUR_DOMAIN>>` with your TLD:

```yaml
  - hosts:
    - ddns.<<YOUR_DOMAIN>>
    secretName: ddns-acc-cert
  rules:
  - host: ddns.<<YOUR_DOMAIN>>
```

Note: You can replace `ddns.` above if you wish to change or remove the sub-domain associated with the service.

## Install Pre-requisites

### Metrics-Server

```bash
helm install --set 'args={--kubelet-insecure-tls}' --namespace metrics-server --create-namespace  metrics-server metrics-server/metrics-server
```

### NGINX

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx
```

### Cert-Manager

```bash
helm install cert-manager cert-manager \
--repo https://charts.jetstack.io \
--create-namespace --namespace cert-manager \
--set installCRDs=true
```

## Install DDNS

```bash
kubectl apply -f namespace.yaml \
-f secrets.yaml \
-f ingressClass.yaml \
-f ingress.yaml \
-f deployment.yaml \
-f hpa.yaml \
-f service.yaml \
-f issuer.yaml
```
