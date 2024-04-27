# Evaluating-utilization-of-GPUs-in-Serverless-Function
This repository implements tools and analysis to measure NVIDIA GPUs utilization in serverless environments. 

# Methodology
This methodology is only applicable for Linux environments.
To utilize the Nvidia GPU, we need to install Nvidia Drivers and CUDA Toolkit (12.4). 
OpenFaaS, a popular severless framework, is utilized for deploying these functions within the choosen runtime environment. 
Minikube, a local Kubernetes implementation, is used to create a development environment that simulates a Kubernetes cluster. Within minikube, the necessary resources, including GPU support using Nvidia Container Toolkit are configured.
Nvtop, a monitoring tool for GPU by Nvidia is utilized for evaluating the GPU.

# Installation-Guide
## Prerequisites
These are the basic prerequisites to get started, for more information [Nvidia CUDA installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
You must have a CUDA capable GPU
```
lspci | grep -i nvidia
```
Verify you have a supported version of Linux
```
uname -m && cat /etc/*release
```
You should see output similar to the following, modified for your particular system
```
x86_64
Red Hat Enterprise Linux Workstation release 6.0 (Santiago)
```
Verify the System Has gcc Installed
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
Test Docker using 'Hello-World'
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
Verify you have access to the GPU using Nvidia Drivers
```
nvidia-smi
```
You should be able to see the Nvidia Driver version number and compatible CUDA Toolkit

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
Verify CUDA installation:
```
nvcc --version
```

## Install Nvidia Container Toolkit to enable GPU support in Docker
You could install the container toolkit using Apt, Zypper or Yum. For Zypper and Yum, and if you have a multinode cluster and using Containerd you could see [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

Installing with Apt
```
$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
Optionally, configure the repository to use experimental packages:
```
$ sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
Update the packages list from the repository and Install the Nvidia Container Toolkit packages
```
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit
```
Configure the container runtime by using the nvidia-ctk command:
```
$ sudo nvidia-ctk runtime configure --runtime=docker
```
The `nvidia-ctk` command modifies the `/etc/docker/daemon.json` file on the host. The file is updated so that Docker can use the NVIDIA Container Runtime.

Restart the Docker daemon:
```
$ sudo systemctl restart docker
```


## Installing Minikube
If you plan to evaluate GPU for a single node cluster use minikube, else you can use containerd
```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
### Using NVIDIA GPUs with Minikube
Now that you have configured container runtime you can start the Kubernetes cluster
Check if `bpf_jit_harden` is set to `0`
```
$ sudo sysctl net.core.bpf_jit_harden
```
If it's not `0` then run:
```
$ echo "net.core.bpf_jit_harden=0" | sudo tee -a /etc/sysctl.conf
$ sudo sysctl -p
```
Start Minikube:
```
$ minikube start --driver docker --container-runtime docker --gpus all
```

## Install Kubectl
```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
```
check whether you are able to execute the binary
```
$ echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```
You shoudl see a Output similar to the following:
`kubectl:OK`

### Installing OpenFaaS via Arkade
Installing OpenFaaS via Arkade it pretty simple. If you face any issues installing OpenFaaS you can head over to [OpenFaaS](https://docs.openfaas.com/cli/install/) Documentation
Get Arkade first
```
$ curl -SLsf https://get.arkade.dev/ | sudo sh
```
Make the kubectl binary executable
```
$ chmod +x kubectl
$ sudo mv kubectl /usr/local/bin
$ arkade install openfaas
```
Install the FaaS-CLI
```
$ curl -SLsf https://cli.openfaas.com | sudo sh
$ echo $(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
$ kubectl rollout status -n openfaas deploy/gateway
$ kubectl port-forward -n openfaas svc/gateway 8080:8080 &
```

# Creating and Deploying the Serverless functions
## Creating a Function
First pull the template repository
```
$ faas-cli template pull
```
Create a java function, Similarly you can replace the language and the function name with Dockerfile, Python, Go etc. and any suitable name that you would like for your function. 
```
$ faas-cli new --lang python pythonFunction
```
This will create a directory with the function name and also functionname.yml

## Build and Deploy the FaaS function
Build the Function. The built in URL is http://127.0.0.1 for OpenFaaS. 
```
$ faas-cli build -f functionname.yml -g $GATEWAY_URL
```
if you need any help building the function, you can take the help of FaaS-CLI by typing in 
```
$ faas-cli build --help
```
Edit the functionname.yml -- The defualt template will not gave any namespaces in it. Make sure to include namespaces
```
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080
functions:
  cupyfunction:
    lang: dockerfile
    handler: ./functionname
    image: <your_dockerhub_username>/functionname:latest
    <namespaces: openfaas-fn>
```
Deploy the function
This will deploy the function to your Docker hub repository
```
$ faas-cli up -f functionname.yml
```
You can enable prometheus for monitoring you cluster by using this command
```
$ faas-cli deploy -f functionname.yml --annotation prometheus.io.scrape=true --annotation prometheus.io.port=8081
```
Check the Prometheus Status will be changed to "True"
```
$ faas-cli describe functionname
```
Invoke the function
```
$ faas-cli invoke functionname
```
To ensure your container is running in the cluster. This will give all the containers running on the cluster. You should be able to see your function with your namespace
```
$ kubectl get pods -A
$ kubectl get services -A
```

# Monitoring the GPU
## Install NVTOP
```
$ sudo apt install nvtop
$ nvtop
```
If your function utilizes the GPU, then you should be able to see the spike in graph. 

