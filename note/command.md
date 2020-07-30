# Commands

## Docker

### Image

search ubuntu

`sudo docker search ubuntu`

pull ubuntu:18.04

`sudo docker pull ubuntu:18.04`

load docker image from tar

`sudo docker load < xxx.tar`

check docker image list

`sudo docker images -a`

enter docker env

`sudo docker run -p 9999:8888 -it $IMAGE_ID /bin/bash`

docker remove image

`sudo docker image rm $IMAGE_ID`

docker commit :从容器创建一个新的镜像

`docker commit CONTAINER_ID IMAGE_NAME:TAG`

### Container

check running docker prosess

`sudo docker ps -a`

exit docker env

`sudo docker stop $CONTAINER_ID`

docker start container

`sudo docker container start $CONTAINER_ID`

docker enter container

`sudo docker exec -it $CONTAINER_ID /bin/bash`

docker remove container

`sudo docker container rm $CONTAINER_ID`

### Nvidia docker

install nvidia-docker

```bash
# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

run nvidia-docker

`sudo docker run --gpus all -p 9999:8888 -it $IMAGE_ID /bin/bash`

### Others

docker cp

`sudo docker cp SRC CONTAINER_ID:<PATH>`

run jupyter notebook in docker

```bash
# use ifconfig to check docker ip
apt install net-tools
ifconfig
# ip=docker_ip, port=docker_port
jupyter notebook --ip=172.17.0.2 --port=8888 --allow-root
# then open ip:port with web browser, ip=host_ip, port=hsot_port_maping_to_docker
```

get postgis image and create container

```bash
sudo docker run --name some-postgis -e POSTGRES_PASSWORD=mysecretpassword -d mdillon/postgis
# in docker, run postgis by:
# psql -U postgres
# select st_area('POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))'::geometry);
```

## Git

update from remote

`git pull $URL $BRANCH_NAME`

or

`git remote add upstream $URL`
`git pull upstream $BRANCH_NAME`

reset to specific version

`git reset --hard $COMMIT_ID`

delete remote branch

`git push origin --delete $BRANCH_NAME`

first pull all submodules

`git submodule update --init --recursive`

to update submodules

`git submodule update --recursive --remote`
or simply

`git pull --recurse-submodules`

remove modify, reset to HEAD

`git reset --hard HEAD`

pull remote branch from somebody else's repo

```bash
git remote add coworker git://path/to/coworkers/repo.git
git fetch coworker
git checkout --track coworker/foo
```

cherry pick commit from another branch

```bash
git checkout -b branch-0.3-x_to_push
git cherry-pick commit-id-from-old-branch
```

## Gdal

convert shp to tiff: -- [参考链接](https://gdal.org/programs/gdal_rasterize.html)

`gdal_rasterize -burn 0 -burn 0 -burn 255 -ot Byte -ts 512 512 -l shanghai shanghai.shp shanghai.tif`

convert shp to GPKG: -- [参考链接](https://gdal.org/programs/ogr2ogr.html)

`ogr2ogr -f GPKG shanghai.gpkg shanghai.shp`

convert GPKG to shp: -- [参考链接](https://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/)

`ogr2ogr -f "ESRI Shapefile" shanghai.shp shanghai.gpkg`

Clip input layer with a bounding box:

`ogr2ogr -spat -13.931 34.886 46.23 74.12 -f GPKG shanghai_clip.gpkg shanghai.gpkg`
`ogr2ogr -spat 0 0 50 70 -f "ESRI Shapefile" point_out_org.shp point_out.shp`

Output file format name. Starting with GDAL 2.3, if not specified, the format is guessed from the extension (previously was ESRI Shapefile).

`ogr2ogr -f GPKG output.gpkg input.shp`
`$ogr2ogr -f GeoJSON point.geojson point.shp`

About polygon -- [参考链接1](http://esri.github.io/geometry-api-java/doc/Polygon.html) -- [参考链接2](https://github.com/Esri/geometry-api-java/wiki)

## Kafka

override kafka conf, set max message bytes

`bin/kafka-configs.sh --zookeeper localhost:9092 --entity-type topics --entity-name connect-test --alter --add-config max.message.bytes=128000`

check topic conf, check max message bytes

`bin/kafka-configs.sh --zookeeper localhost:9092 --entity-type topics --entity-name connect-test --describe`

check message size of a topic

`bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic connect-test --time -1`
`bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --all-groups --describe`

produce massage from file

`bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test < test.txt`

## kubernetes

### minikube

start minikube
`minikube start --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers`

start service
`minikube service $service-name`

<https://minikube.sigs.k8s.io/docs/commands/>

### kubectl

<https://docs.docker.com/config/daemon/systemd/>

get all pods in all namespaces

`kubectl get pods --all-namespaces`

get cluster info

`kubectl cluster-info`

get pods

`kubectl get pods`

get pods infos

`kubectl describe pod <pod_name>`

get pods infos in specific namespace

`kubectl describe pod <podname> -n <namespace>`

deployment nginx

`kubectl apply -f https://k8s.io/examples/application/deployment.yaml`

get deployment
`kubectl get deployment`

get deployment info

`kubectl describe deployment <deployment-name>`

delete deployment

`kubectl delete deployment <deployment-name>`

## Other

use objdump to check function sign

`objdump libxxx.so -T | grep keyword`

install java 8

`sudo apt-get install openjdk-8-jdk`
