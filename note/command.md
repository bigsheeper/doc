## Docker
###### search ubuntu
`sudo docker search ubuntu`
###### pull ubuntu:18.04
`sudo docker pull ubuntu:18.04`
###### load docker image from tar
`sudo docker load < xxx.tar`
###### check docker image list
`sudo docker images -a`
###### check running docker prosess
`sudo docker ps -a`
###### enter docker env
`sudo docker run -it $IMAGE_ID /bin/bash`
###### exit docker env
`sudo docker stop $CONTAINER_ID`
###### docker remove container
`sudo docker container rm`
###### docker cp
`sudo docker cp SRC CONTAINER_ID:<PATH>`
###### docker commit :从容器创建一个新的镜像
`docker commit CONTAINER_ID IMAGE_NAME:TAG`

## Git
###### update from remote
`git pull $URL $BRANCH_NAME`
or
`git remote add upstream $URL`
`git pull upstream $BRANCH_NAME`
###### reset to specific version
`git reset --hard $COMMIT_ID`
###### delete remote branch
`git push origin --delete $BRANCH_NAME`
###### first pull all submodules
`git submodule update --init --recursive`
###### to update submodules
`git submodule update --recursive --remote`
or simply
`git pull --recurse-submodules`
###### remove modify, reset to HEAD
`git reset --hard HEAD`
###### pull remote branch from somebody else's repo
```
git remote add coworker git://path/to/coworkers/repo.git
git fetch coworker
git checkout --track coworker/foo
```

## Others
###### use objdump to check function sign
`objdump libxxx.so -T | grep keyword`
###### install java 8
`sudo apt-get install openjdk-8-jdk`
