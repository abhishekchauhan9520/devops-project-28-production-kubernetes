# Project 28 — Production Kubernetes Application Platform

A production-style Kubernetes workload baseline demonstrating secure workload defaults, resilient rolling updates, health probes, autoscaling, disruption protection, ingress/TLS, and network policy.

## Architecture

```text
Internet
   |
   v
Ingress + TLS
   |
   v
ClusterIP Service
   |
   v
3+ Application Pods
   |---- readiness/liveness/startup probes
   |---- CPU/memory requests + limits
   |---- non-root / seccomp / dropped capabilities
   |
   +---- HPA (3-10)
   +---- PodDisruptionBudget (min 2)
   +---- NetworkPolicy
```

## Included

- RollingUpdate with `maxUnavailable: 0`
- 3 replicas with revision history
- Startup, readiness, and liveness probes
- CPU/memory requests and limits
- Non-root container
- Read-only root filesystem
- Dropped Linux capabilities
- `RuntimeDefault` seccomp
- Service-account token disabled
- Namespace Pod Security Admission labels at `restricted`
- Ingress with TLS configuration
- HPA with scale-down stabilization
- PodDisruptionBudget
- NetworkPolicy
- CI validation

## Deployment

This repository deliberately does not auto-deploy to a real cluster. Review and configure the image registry, ingress hostname/TLS secret, and cluster policies first.

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml
kubectl apply -f k8s/networkpolicy.yaml
kubectl apply -f k8s/ingress.yaml
kubectl -n production-demo rollout status deployment/production-app
```

## Production notes

The Ingress example assumes an NGINX Ingress controller and a pre-created TLS secret named `production-app-tls`. The sample NetworkPolicy is intentionally conservative but should be tightened around actual application dependencies before production use.
