###**1. spatial datatype support**
|DATATYPE|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|point|1|1|
|multi-point|1|1|
|polygon|1|1|
|multi-polygon|1|1|
|surface|0|1|
|multi-surface|0|1|
|linestring|1|1|
|multi-linestring|1|1|
|curve|0|1|
|multi-curve|0|1|
|GeometryCollection|1|1|
<br/>

###**2. file format support**
|File Format|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|CSV|1|1|
|TSV|1|0|
|WKT|1|1|
|WKB|1|1|
|EWKT|0|1|
|EWKB|0|1|
|GeoJSON|1|1|
|NASA NetCDF/HDF|1|0|
|Shapefile|1|1|
<br/>

###**3. spatial query support**
|Spatial Query|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|range|1|1|
|range join|1|1|
|distance join|1|1|
|K Nearest Neighbor|1|1|
<br/>

###**4. high resolution map support**
|Map Type|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|Scatter plot|1|0|
|heat map|1|0|
|choropleth map|1|0|
<br/>

###**5. language support**
|Language|Supported GeoSpark modules|PostGIS|
|:-:|:-:|:-:|
|scala|RDD, SQL, Viz, Zeppelin|1|
|java|RDD, SQL, Viz|1|
|SQL|SQL, Viz, Zeppelin|1|
|python|SQL|1|
|R|SQL|1|
<br/>

###**6. spatial functions**
|functions|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|conversion|0|1|
|management|1|1|
|retrieval|1|1|
|comparison|1|1|
|generation|1|1|
<br/>

###**7. spatial index**
|index|GeoSpark|PostGIS|
|:-:|:-:|:-:|
|R-Tree|1|1|
|Quad-Tree|1|0|
<br/>