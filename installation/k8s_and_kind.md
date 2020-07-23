# Installation of K8s & Kind on Ubuntu

## install kubectl

```bash
snap install kubectl --classic
kubectl version --client
```

or

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

## install kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.8.1/kind-linux-amd64
chmod +x ./kind
mv ./kind /some-dir-in-your-PATH/kind
```

## install helm

```bash
sudo snap install helm --classic
```

## install minikube and VirtualBox Hypervisor

### install minikube

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
mv minikube /some-dir-in-your-PATH/minikube
```

### install VirtualBox

```bash
sudo apt install virtualbox virtualbox-ext-pack
```

## Reference

<https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/get-started#%E4%BD%BF%E7%94%A8-kind-%E5%88%9B%E5%BB%BA-kubernetes-%E9%9B%86%E7%BE%A4>

<https://phoenixnap.com/kb/install-minikube-on-ubuntu>
