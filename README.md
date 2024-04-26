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
These steps should help you install Docker. For further infor
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

