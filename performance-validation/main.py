import yaml
import sys
import time

from datetime import datetime, timezone
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from os import path

if len(sys.argv) < 3:
    print("Number of replicas is expected to be provided as the second argument.")
    print("Number of exections is expected to be provided as the third argument.")
    exit(1)

print(f"Number of replicas provided is {sys.argv[1]}")
print(f"Number of executions provided is {sys.argv[2]}")

number_replicas = int(sys.argv[1])
number_of_executions = int(sys.argv[2])

kubeconfig_path = path.join(path.dirname(__file__),"kubemark.yaml")
config.load_kube_config(config_file=kubeconfig_path)

with open(path.join(path.dirname(__file__),'replicaset_template.yaml')) as f:
    replica_set_yaml = yaml.safe_load(f)

replica_set_yaml['spec']['replicas'] = number_replicas
k8s_apps = client.AppsV1Api()
k8s_core = client.CoreV1Api()

# I know...
def delete_replica_set():
    try:
        k8s_apps.delete_namespaced_replica_set(name=replica_set_yaml['metadata']['name'], namespace=replica_set_yaml['metadata']['namespace'])
        print("Replica set deleted...")
    except ApiException as e:
        if e.status == 404:
            print("Replica set did not exist...")
        else:
            print("Exception when calling AppsV1Api->delete_namespaced_replica_set: %s\n" % e)
            raise

label_selector=""
match_labels=replica_set_yaml['spec']['selector']['matchLabels']

for v in match_labels:
    if label_selector != "":
        label_selector+=","
    
    label_selector+=f"{v}={match_labels[v]}"

results = []

for i in range(number_of_executions):

    delete_replica_set()

    pods_not_finished=True
    while (pods_not_finished):
        pods = k8s_core.list_namespaced_pod(label_selector=label_selector, namespace=replica_set_yaml['metadata']['namespace'])
        if len(pods.items) == 0:
            pods_not_finished=False
        else:
            time.sleep(1)
    
    replica_set = k8s_apps.create_namespaced_replica_set(body=replica_set_yaml, namespace=replica_set_yaml['metadata']['namespace'])

    is_ready = False
    while (not is_ready):
        replica_set_response = k8s_apps.read_namespaced_replica_set(name=replica_set.metadata.name, namespace=replica_set.metadata.namespace)
        is_ready=(replica_set_response.status.ready_replicas == replica_set_response.spec.replicas)
        end_time = datetime.now(timezone.utc)

    creation_timestamp = replica_set_response.metadata.creation_timestamp

    time_delta = (end_time - creation_timestamp)
    total_seconds = time_delta.total_seconds()

    results.append(total_seconds)

delete_replica_set()

print("total seconds:") 
print(f"average is: {sum(results) / len(results)}")
for v in results:
    print(str(v).replace(".", ","))

