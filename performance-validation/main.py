import yaml
import sys

from datetime import datetime, timezone
from kubernetes import client, config
from os import path

if len(sys.argv) < 2:
    print("Number of replicas is expected to be provided as the second argument.")
    exit(1)

print(f"Number of replicas provided is {sys.argv[1]}")

number_replicas = int(sys.argv[1])

kubeconfig_path = path.join(path.dirname(__file__),"kubemark.yaml")
config.load_kube_config(config_file=kubeconfig_path)

with open(path.join(path.dirname(__file__),'replicaset_template.yaml')) as f:
    replica_set_yaml = yaml.safe_load(f)

replica_set_yaml['spec']['replicas'] = number_replicas
k8s_apps = client.AppsV1Api()
replica_set = k8s_apps.create_namespaced_replica_set(body=replica_set_yaml, namespace="default")

is_ready = False
while (not is_ready):
    response = k8s_apps.read_namespaced_replica_set(name=replica_set.metadata.name, namespace=replica_set.metadata.namespace)
    is_ready=(response.status.ready_replicas == response.spec.replicas)
    end_time = datetime.now(timezone.utc)

creation_timestamp = response.metadata.creation_timestamp

time_delta = (end_time - creation_timestamp)
total_seconds = time_delta.total_seconds()

print(f"total seconds: {total_seconds}")

k8s_apps.delete_namespaced_replica_set(name=response.metadata.name, namespace=response.metadata.namespace)
