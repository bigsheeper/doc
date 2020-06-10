# Commands


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


## Gdal

###### convert shp to tiff: -- [参考链接](https://gdal.org/programs/gdal_rasterize.html)
`gdal_rasterize -burn 0 -burn 0 -burn 255 -ot Byte -ts 512 512 -l shanghai shanghai.shp shanghai.tif`

###### convert shp to GPKG: -- [参考链接](https://gdal.org/programs/ogr2ogr.html)
`ogr2ogr -f GPKG shanghai.gpkg shanghai.shp`

###### convert GPKG to shp: -- [参考链接](https://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/)
`ogr2ogr -f "ESRI Shapefile" shanghai.shp shanghai.gpkg`

###### Clip input layer with a bounding box:
`ogr2ogr -spat -13.931 34.886 46.23 74.12 -f GPKG shanghai_clip.gpkg shanghai.gpkg`
`ogr2ogr -spat 0 0 50 70 -f "ESRI Shapefile" point_out_org.shp point_out.shp`

###### Output file format name. Starting with GDAL 2.3, if not specified, the format is guessed from the extension (previously was ESRI Shapefile).
`ogr2ogr -f GPKG output.gpkg input.shp`
`$ogr2ogr -f GeoJSON point.geojson point.shp`

###### About polygon -- [参考链接1](http://esri.github.io/geometry-api-java/doc/Polygon.html) -- [参考链接2](https://github.com/Esri/geometry-api-java/wiki)


## Kafka

###### override kafka conf, set max message bytes
`bin/kafka-configs.sh --zookeeper localhost:9092 --entity-type topics --entity-name connect-test --alter --add-config max.message.bytes=128000`

###### check topic conf, check max message bytes
`bin/kafka-configs.sh --zookeeper localhost:9092 --entity-type topics --entity-name connect-test --describe
`

###### check message size of a topic
`bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic connect-test --time -1`
`bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --all-groups --describe`

###### produce massage from file
`bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test < test.txt`

## Others

###### use objdump to check function sign
`objdump libxxx.so -T | grep keyword`

###### install java 8
`sudo apt-get install openjdk-8-jdk`
