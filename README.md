# vnx-kubespray

VNX scenario that deploys a production-ready three-node Kubernetes cluster using [kubespray](https://kubespray.io/#/) utilities.

![kubespray](tutorial_kubespray/docs/kubespray-logo.png)

By default Calico network plugin is used.

## Scenario topology

![VNX tutorial_kubespray scenario](tutorial_kubespray/docs/scenario.png)

K8s nodes are deployed as KVM virtual machines whereas r1 and h1 are LXC containers. They all run Ubuntu LTS 18.04.

## Requirements

- Baremetal Linux OS (_Tested on Ubuntu LTS 18.04_)
- VNX software -> [VNX Installation Recipe](https://web.dit.upm.es/vnxwiki/index.php/Vnx-install)
- Internet connection
- Hardware requirments: minimum 4GB RAM and 4 CPU cores

**IMPORTANT NOTE:** This VNX scenario **cannot be deployed on a VirtualBox VM** since the virtualized nodes in the scenario are KVM-based virtual machines.

## Setup

Install Ansible among other utilities needed by kubespray

```bash
cd tutorial_kubespray/ansible/kubespray
sudo pip3 install -r requirements.txt
```

## Getting Started

First of all deploy VNX scenario:

```bash
cd tutorial_kubespray
sudo vnx -f tutorial_kubespray.xml -v --create
```

Then run ansible playbook to setup a Kubernetes cluster on the three virtual machines:

```bash
cd tutorial_kubespray/ansible
ansible-playbook playbooks/site.yml
```

The execution of ansible playbook will take 10 minutes roughly. Once this playbook has finished successfully, we will have a Kubernetes cluster ready to play with.

## Interacting with the cluster

### Node Management

VNX creates a point-to-point link for management access and dynamically builds an SSH config file for the scenario. Such file can be found at `$HOME/.ssh/config.d/vnx/tutorial_kubespray`. As a result, our Kubernetes nodes and the remaining network elements can be easily accessed as follows:

```bash
# Master node
ssh k8s-master

# Worker nodes
ssh k8s-worker1
ssh k8s-worker2

## Router
ssh r1

## End-user
ssh h1
```

This is how Ansible would access the nodes in the scenario.

### Kubectl usage

Kubespray installs `kubectl` client for us in the master node. Kube config file used by the client is stored in `/root/.kube/config`. This is a copy of `/etc/kubernetes/admin.conf` file.

Alternatively, kubespray could install the `kubectl` and/or copy the config file in the host machine for remote interaction with Kubernetes API. This feature has been tested out yet.

### Helm client

Helm client is installed in the master node.

## Network Management

> *TODO*: We  use Calico as k8s network plugin. BGP peering is configured from each k8s node to router r1, who runs BIRD daemon providing BGP route reflector_functions to the k8s cluster. By using Calicos BGP feature, our router r1 can dynamically learn pod and service IPs from Kubernetes. As a result, external hosts such as h1 can easily access k8s services without having to manage routing in the network.

## Cleanup

To destroy the VNX scenario, run the following command:

```bash
cd tutorial_kubespray
sudo vnx -f tutorial_kubespray.xml -v --destroy
```
