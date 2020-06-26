# E2E Scheduler performance validation

## K8S Configuration

Using kubemark to set up the environment, setting the number of nodes to 100. Using kubernetes
repository on tag `1.18.4`.

External Cluster: GKE 1.17

Number of K8S Nodes: 100

This validation should be executed in the master node that runs the kubemark components. Use the
kubemark internal kubeconfig or just configure the external kubeconfig pointing to the internal
IP:

```yaml
apiVersion: v1
clusters:
- cluster:
    insecure-skip-tls-verify: true
    server: https://<INTERNAL_IP>
  name: kubemark-control-plane-perf_default-kubemark
contexts:
```

Do that to reduce latency.

