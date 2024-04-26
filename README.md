# Evaluating-utilization-of-GPUs-in-Serverless-Function
This repository implements tools and analysis to measure NVIDIA GPUs utilization in serverless environments. 

# Methodology
This methodology is only applicable for Linux environments.
To utilize the Nvidia GPU, we need to install Nvidia Drivers and CUDA Toolkit (12.4 - Latest). 
OpenFaaS, a popular severless framework, is utilized for deploying these functions within the choosen runtime environment. 
Minikube, a local Kubernetes implementation, is used to create a development environment that simulates a Kubernetes cluster. Within minikube, the necessary resources, including GPU support using Nvidia Container Toolkit are configured.
Nvtop, a monitoring tool for GPU by Nvidia is utilized for evaluating the GPU.

# Installation-Guide
## Prerequisites
These are the basic prerequisites to get started, for more information [Nvidia CUDA installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
### You must have a CUDA capable GPU
```
lspci | grep -i nvidia
```
### Verify you have a supported version of Linux
```
uname -m && cat /etc/*release
```
##### You should see output similar to the following, modified for your particular system
```
x86_64
Red Hat Enterprise Linux Workstation release 6.0 (Santiago)
```
### Verify the System Has gcc Installed
```
gcc --version
```
## Installing Docker
These steps should help you install Docker. For further information visit [Docker](https://docs.docker.com/engine/install/ubuntu/)
```
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl
$ sudo install -m 0755 -d /etc/apt/keyrings
$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
$ sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### Test Docker using 'Hello-World'
```
sudo docker run hello-world
```

## Installing Nvidia Drivers
If your GPU is compatible with 550 Drivers, you could execute the following commands. You could look up what driver is best for the GPU [here](https://www.nvidia.com/Download/index.aspx?lang=en-us)
```
$ sudo apt-get update
$ sudo apt-get install -y linux-headers-$(uname -r) gcc make
$ wget https://us.download.nvidia.com/XFree86/Linux-x86_64/550.54.15/NVIDIA-Linux-x86_64-550.54.15.run
$ sudo chmod +x NVIDIA-Linux-x86_64-550.54.15.run
$ sudo ./NVIDIA-Linux-x86_64-550.54.15.run --silent --dkms
```

## Installing CUDA Toolkit(12.4)
The OS, Architecture and Distribution details are below, For other Distributions you can go [here](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local)
Operating System : Linux 
Architecture : x86_64
Distribution : Ubuntu 
Version : 22.04
Installer type : deb(local)
```
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
$ sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda-repo-ubuntu2204-12-4-local_12.4.1-550.54.15-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu2204-12-4-local_12.4.1-550.54.15-1_amd64.deb
$ sudo cp /var/cuda-repo-ubuntu2204-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
$ sudo apt-get update
$ sudo apt-get -y install cuda-toolkit-12-4
```
### Installing CUDA Drivers
```
$ sudo apt-get install -y cuda-drivers
$ sudo apt-get install -y nvidia-driver-550-open
$ sudo apt-get install -y cuda-drivers-550
```
## Install Nvidia Container Toolkit to enable GPU support in Docker


## Installing Minikube
If you plan to evaluate GPU for a single node cluster use minikube, else you can use containerd
```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
### Using NVIDIA GPUs with Minikube
Check if `bpf_jit_harden` is set to `0`
```
$ sudo sysctl net.core.bpf_jit_harden
```
If it's not `0` then run:
```
$ echo "net.core.bpf_jit_harden=0" | sudo tee -a /etc/sysctl.conf
$ sudo sysctl -p
```
Configure Docker:
```
$ sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
```
Start Minikube:
```
minikube start --driver docker --container-runtime docker --gpus all
```

## Install Kubectl
```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
```
#### check whether you are able to execute the binary
```
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```
###### You shoudl see a Output similar to the following:
`kubectl:OK`






