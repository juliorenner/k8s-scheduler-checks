# E2E Scheduler performance validation

## K8S Configuration

Using kubemark to set up the environment, setting the number of nodes to 100. Using kubernetes
repository on tag `1.18.4`.

External Cluster: GKE 1.17

Number of K8S Nodes: 100

This validation should be executed in the master node that runs the kubemark components to
reduce latency impacts. Use the kubemark internal kubeconfig or just configure the external
kubeconfig pointing to the internal IP:

```yaml
apiVersion: v1
clusters:
- cluster:
    insecure-skip-tls-verify: true
    server: https://<INTERNAL_IP>
  name: kubemark-control-plane-perf_default-kubemark
contexts:
```

To have an idea about the difference:

Pinging from inside the node to its internal IP:

```sh
root@default-kubemark-master:/# ping 10.40.0.2
PING 10.40.0.2 (10.40.0.2) 56(84) bytes of data.
64 bytes from 10.40.0.2: icmp_seq=1 ttl=64 time=0.037 ms
64 bytes from 10.40.0.2: icmp_seq=2 ttl=64 time=0.046 ms
64 bytes from 10.40.0.2: icmp_seq=3 ttl=64 time=0.056 ms
64 bytes from 10.40.0.2: icmp_seq=4 ttl=64 time=0.063 ms
64 bytes from 10.40.0.2: icmp_seq=5 ttl=64 time=0.046 ms
64 bytes from 10.40.0.2: icmp_seq=6 ttl=64 time=0.055 ms
64 bytes from 10.40.0.2: icmp_seq=7 ttl=64 time=0.045 ms
64 bytes from 10.40.0.2: icmp_seq=8 ttl=64 time=0.047 ms
64 bytes from 10.40.0.2: icmp_seq=9 ttl=64 time=0.049 ms
```

Pinging from outside the node to its external IP:

```sh
ping <EXTERNAL_IP>
PING <EXTERNAL_IP> (<EXTERNAL_IP>): 56 data bytes
64 bytes from <EXTERNAL_IP>: icmp_seq=0 ttl=53 time=163.288 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=1 ttl=53 time=162.860 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=2 ttl=53 time=163.207 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=3 ttl=53 time=163.251 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=4 ttl=53 time=163.304 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=5 ttl=53 time=163.053 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=6 ttl=53 time=163.210 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=7 ttl=53 time=162.906 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=8 ttl=53 time=163.034 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=9 ttl=53 time=163.170 ms
64 bytes from <EXTERNAL_IP>: icmp_seq=10 ttl=53 time=162.788 ms
```
