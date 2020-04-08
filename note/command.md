##Docker
######load docker image from tar
`sudo docker load < xxx.tar`
######check docker image list
`sudo docker images -a`
######check running docker prosess
`sudo docker ps -a`
######enter docker env
`sudo docker run -it $IMAGE_ID /bin/bash`
######exit docker env
`sudo docker stop $CONTAINER_ID`

##Git
######update from remote
`git pull $URL $BRANCH_NAME`
or
`git remote add upstream $URL`
`git pull upstream $BRANCH_NAME`
######reset to specific version
`git reset --hard $COMMIT_ID`
######delete remote branch
`git push origin --delete $BRANCH_NAME`

##Others
######use objdump to check function sign
`objdump libxxx.so -T | grep keyword`