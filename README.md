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
### You must have a CUDA capable GPU
`lspci | grep -i nvidia`
### Verify you have a supported version of Linux
`uname -m && cat /etc/*release`
##### You should see output similar to the following, modified for your particular system
```
x86_64
Red Hat Enterprise Linux Workstation release 6.0 (Santiago)
```
### Verify the System Has gcc Installed
`gcc --version`

