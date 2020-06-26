# E2E Scheduler performance validation

## K8S Configuration

Using kubemark to set up the environment, setting the number of nodes to 100. Using kubernetes
repository on tag `1.18.4`.

External Cluster: GKE 1.17

Number of K8S Nodes: 100

This validation should be executed in the master node that runs the kubemark components. Use the
kubemark internal kubeconfig.
