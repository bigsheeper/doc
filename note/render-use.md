# vega 接口

## vega_pointmap
```python
def vega_pointmap(width,
                  height,
                  bounding_box,
                  point_size,
                  point_color,
                  opacity,
                  coordinate_system)
```
- 函数功能: 设置用于渲染的输入数据的地理范围和地理坐标系统,目标图片的宽和高,以及点图中点的直径,颜色,不透明度

- 参数: 
```
width(int): 图片宽度,单位是像素
height(int): 图片高度,单位是像素
bounding_box(list): 渲染图片所表示的地理范围,参数以[x_min, y_min, x_max, y_max]的形式表示的一个矩形区域,图片左下角的像素坐标(0, 0)表示实际地理坐标(x_min, y_min),图片右上角的像素坐标(width, height)表示地理坐标(x_max, y_max)
point_size(int): 可选参数,表示点的直径, 默认值为3
point_color(str): 可选参数,表示点的颜色,使用十六进制的CSS颜色值表示,默认值为"#115f9a"
opacity(float): 可选参数,表示点的不透明度,默认值为1.0
coordinate_system(str): 可选参数,表示输入数据的坐标系统,默认值为"EPSG:3857",可选的坐标系统请参照<https://spatialreference.org/ref/epsg/>
```

- 返回值: 用于描述渲染样式的VegaPointMap对象
- 返回值类型: `arctern.util.vega.pointmap.vega_pointmap.VegaPointMap` TODO

- 示例: 
```python
#绘制宽为1024,高为896,点直径为3的,点颜色为蓝色的完全不透明点图
vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63])


#绘制宽为1024,高为896,点直径为10的,点颜色为红色的半透明点图
vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], point_size=10, point_color="#FF0000", opacity=0.5, coordinate_system="EPSG:4326")
```

## vega_weighted_pointmap
```python
def vega_weighted_pointmap(width,
                           height,
                           bounding_box,
                           color_gradient,
                           color_bound,
                           size_bound,
                           opacity,
                           coordinate_system)
```
- 函数功能: 设置用于渲染的输入数据的地理范围和地理坐标系统,目标图片的宽和高,以及点图中点的直径范围,颜色范围,透明度

- 参数: 
```
width(int): 图片宽度,单位是像素
height(int): 图片高度,单位是像素
bounding_box(list): 渲染图片所表示的地理范围,参数以[x_min, y_min, x_max, y_max]的形式表示一个矩形区域,图片z左下角的像素坐标(0, 0)表示实际地理坐标(x_min, y_min),图片右上角的像素坐标(width, height)表示地理坐标(x_max, y_max)
color_gradient(list): 点的颜色渐变范围,表示形式为["0000FF"]或["#0000FF", "FF0000"],["0000FF"]表示所有的点颜色相同, ["#0000FF", "FF0000"]表示点的颜色可变,点的颜色由输入的color_weight列的权重值决定
color_bound(list): 可选参数,表示控制颜色的权重值范围,表示形式为[1, 10],只有当color_gradient的list包含两个颜色值(比如["#0000FF", "#FF0000"])时需要设置,权重值等于1时点的颜色值为"#0000FF", 权重值等于10时点的颜色值为"#FF0000"
size_bound(list): 可选参数,表示控制点直径的权重值范围,表示形式为[10]或[1, 10],[10]表示所有点的直径都为10, [1, 10]表示点大小可变,权重值等于1时,点的直径为1,权重值等于10时,点的直径为10, 默认值为[3]
opacity(float): 可选参数,点的不透明度,默认值为1.0
coordinate_system(str): 可选参数,表示输入数据的坐标系统,默认值为"EPSG:3857",可选的坐标系统请参照https://spatialreference.org/ref/epsg/
```

- 返回值: 用于描述渲染样式的VegaWeightedPointMap对象
- 返回值类型: `arctern.util.vega.pointmap.vega_weighted_pointmap.VegaWeightedPointMap` TODO

- 示例: 
```python
#绘制宽为1024,高为896,点颜色相同,直径不同的权重点图
vega1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#87CEEB"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")


#绘制宽为1024,高为896,点颜色不同,直径相同的权重点图
vega2_1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], opacity=0.5, coordinate_system="EPSG:4326")

vega2_2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[10], coordinate_system="EPSG:4326")


#绘制宽为1024,高为896,点颜色和直径都不同的权重点图
vega3_1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], opacity=0.5, coordinate_system="EPSG:4326")

vega3_2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], coordinate_system="EPSG:4326")

vega3_3 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10])
```

## vega_heatmap
```python
def vega_heatmap(width,
                 height,
                 bounding_box,
                 map_zoom_level,
                 coordinate_system,
                 aggregation_type)
```

- 函数功能: 设置用于渲染的输入数据的地理范围,地理坐标系统,数据聚合操作类型,目标图片的宽和高,以及影响热力图中的热度辐射范围的map_zoom_level

- 参数: 
```
width(int): 图片宽度,单位是像素
height(int): 图片高度,单位是像素
bounding_box(list): 渲染图片所表示的地理范围,参数以[x_min, y_min, x_max, y_max]的形式表示一个矩形区域,图片z左下角的像素坐标(0, 0)表示实际地理坐标(x_min, y_min),图片右上角的像素坐标(width, height)表示地理坐标(x_max, y_max)
map_zoom_level(float): 地图放大比例,mapbox取值范围(1 ~ 15)
coordinate_system(str): 可选参数,表示输入数据的坐标系统,默认值为"EPSG:3857",可选的坐标系统请参照https://spatialreference.org/ref/epsg/
aggregation_type(str): 可选参数,数据聚合操作类型, 默认值为"max"
```

- 返回值: 用于描述渲染样式的VegaHeatMap对象
- 返回值类型: `arctern.util.vega.heatmap.vega_heatmap.VegaHeatMap` TODO

- 示例: 
```python
#绘制宽为1024,高为896的热力图
vega_1 = arctern.util.vega.vega_heatmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], map_zoom_level=10.0, coordinate_system="EPSG:4326")

vega_2 = arctern.util.vega.vega_heatmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63], map_zoom_level=10.0)
```

## vega_choroplethmap
```python
def vega_choroplethmap(width,
                       height,
                       bounding_box,
                       color_gradient,
                       color_bound,
                       opacity,
                       coordinate_system,
                       aggregation_type)
```
- 函数功能: 设置用于渲染的输入数据的地理范围,地理坐标系统,数据聚合操作类型,目标图片的宽和高,以及轮廓图的颜色范围,透明度

- 参数:
```
width(int): 图片宽度,单位是像素
height(int): 图片高度,单位是像素
bounding_box(list): 渲染图片所表示的地理范围,参数以[x_min, y_min, x_max, y_max]的形式表示一个矩形区域,图片z左下角的像素坐标(0, 0)表示实际地理坐标(x_min, y_min),图片右上角的像素坐标(width, height)表示地理坐标(x_max, y_max)
color_gradient(list): 点的颜色渐变范围,表示形式为["#0000FF", "FF0000"],点的颜色由输入的color_weight列的权重值决定
color_bound(list): 控制颜色的权重值范围,表示形式为[1, 10],如果color_gradient=["#0000FF", "#FF0000"],权重值等于1时点的颜色值为"#0000FF", 权重值等于10时点的颜色值为"#FF0000"
opacity(float): 可选参数,表示点的不透明度,默认值为1.0
coordinate_system(str): 可选参数,表示输入数据的坐标系统,默认值为"EPSG:3857",可选的坐标系统请参照https://spatialreference.org/ref/epsg/
aggregation_type(str): 可选参数,数据聚合操作类型, 默认值为"sum"
```

- 返回值: 用于描述渲染样式的VegaChoroplethMap对象

- 返回值类型: `arctern.util.vega.choroplethmap.vega_choroplethmap.VegaChoroplethMap` TODO

- 示例: 
```python
#绘制宽为1024,高为896,颜色值在蓝色和红色之间的轮廓图
vega_1 = arctern.util.vega.vega_choroplethmap(1900, 1410, bounding_box=[-73.994092, 40.753893, -73.977588, 40.759642], color_gradient=["#0000FF", "#FF0000"], color_bound=[2.5, 5], opacity=0.5, coordinate_system="EPSG:4326")

vega_2 = arctern.util.vega.vega_choroplethmap(1900, 1410, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63], color_gradient=["#0000FF", "#FF0000"], color_bound=[2.5, 5])
```



# pandas 接口

## pointmap
```python
def point_map(vega, points)
```
- 函数功能: 绘制点图

- 参数: 
```
vega: VegaPointMap对象
points: 包含一列points的Series,point的类型为WKB 
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#绘制点大小为3, 点颜色为#2DEF4A,点不透明度为0.5的点图
vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], point_size=3, point_color="#2DEF4A", opacity=0.5, coordinate_system="EPSG:4326")

res = arctern.point_map(vega, points)
```

## weighted_pointmap
```python
def weighted_point_map(vega, points, color_weights, size_weights)
```
- 函数功能: 绘制带权重的点图,图中点的大小和颜色不同

- 参数: 
```python
vega: VegaWeightedPointMap对象
points: 包含一列points的Series,point的类型为WKB
color_weights: 包含一列数值类型数据的Series
size_weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#color_gradient的list中只有一个元素,表示点的颜色都为#87CEEB, 此时可以不指定color_bound, size_bound=[1,10]表示size_weights series中最小值对应的点大小为1,最大值对应的点大小为10.
vega1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#87CEEB"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")

res1 = arctern.weighted_point_map(vega1, points, size_weights=arr_s)


#color_gradient和color_bound的list中同时包含两个元素,color_bound中的1和5分别对应color_weights series中的最小值和最大值,最小值代表的点的颜色为#0000FF,最大值代表的点的颜色为#FF0000, 点色大小为10
vega2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], opacity=1.0, coordinate_system="EPSG:4326")

res2 = arctern.weighted_point_map(vega2, points, color_weights=arr_c)


#color_gradient和color_bound的list中同时包含两个元素,color_bound中的1和5分别对应color_weights series中的最小值和最大值,其最小值代表的点的颜色为#0000FF,最大值代表的点的颜色为#FF0000,size_bound=[1,10]表示size_weights series中最小值对应的点大小为1,最大值对应的点大小为10.
vega3 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")

res3 = arctern.weighted_point_map(vega3, points, color_weights=arr_c, size_weights=arr_s)
```

## heatmap
```python
def heat_map(vega, points, weights)
```
- 函数功能: 绘制热力图

- 参数: 
```json
vega: VegaHeatMap对象
points: 包含一列point的Series,point的类型为WKB
weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#地图放大比例为10.0.输入数据的坐标系统为EPSG:4326
vega = arctern.util.vega.vega_heatmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], map_zoom_level=10.0, coordinate_system="EPSG:4326")

res = arctern.heat_map(vega, points, arr_c)
```

## choroplemap
```python
def choropleth_map(vega, region_boundaries, weights)
```
- 函数功能: 绘制轮廓图

- 参数:
```json
vega: VegaChoroplethMap对象
region_boundaries: 包含一列多边形的Series,多边形的类型为WKB
weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#color_gradient和color_bound的list同时包含两个元素,color_bound中的2.5和5分别对应weights series中的最小值和最大值,其最小值代表的多边形的颜色为#0000FF,最大值代表的多边形的颜色为#FF0000,
vega = arctern.util.vega.vega_choroplethmap(1900, 1410, bounding_box=[-73.994092, 40.753893, -73.977588, 40.759642], color_gradient=["#0000FF", "#FF0000"], color_bound=[2.5, 5], opacity=1.0, coordinate_system="EPSG:4326")

res = arctern.choropleth_map(vega, geos, weights)
```



# pyspark 接口

## pointmap
```python
def pointmap(vega, df)
```
- 函数功能: 绘制点图

- 参数: 
```json
vega: VegaPointMap的python对象
df: 包含一列points的dataframe,point的类型为WKB
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例:
```python
#和spark的画图结合同样和vega接口配合使用,等同于python画图的使用方式
#df是只有一列数据的dataframe, 该列数据的表示点坐标,类型为web格式的POINT("POINT(1 1)")
vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], point_size=3, point_color="#2DEF4A", opacity=0.5, coordinate_system="EPSG:4326")

res = arctern_pyspark.pointmap(vega, df)
```

## weighted_pointmap
```python
def weighted_pointmap(vega, df)
```
- 函数功能: 绘制带权重的点图,点的大小和颜色不同

- 参数: 
```json
vega: VegaWeightedPointMap的python对象
df: 包含两列或三列数据的dataframe,第一列都是WKB类型的points,第二列或第三列为数值类型的数据
```

- 返回值: base64 encoded png

- 返回值类型: `bytes`

- 示例: 
```python
#df1包含2列series,第一列Series表示点坐标,第二列为点大小的权重数据
vega1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#87CEEB"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")

res1 = arctern_pyspark.weighted_pointmap(vega1, df1)


#df2包含2列series,第一列Series表示点坐标,第二列为点颜色的权重数据
vega2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], opacity=1.0, coordinate_system="EPSG:4326")

res2 = arctern_pyspark.weighted_pointmap(vega1, df2)


#df3包含3列series,第一列Series表示点坐标,第二列为点颜色的权重数据,第三列为点大小的权重数据
vega3 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")

res3 = arctern_pyspark.weighted_pointmap(vega3, df3)
```

## heatmap
```python
def heatmap(vega: VegaHeatMap, df: DataFrame) -> base64 encoded png
```
- 函数功能: 绘制热力图

- 参数: 
```json
vega: VegaHeatMap的python对象
df: 包含两列数据的dataframe,第一列都是WKB类型的points,第二列为数值类型的数据
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#df包含2列series,第一列Series表示点坐标,第二列数据表示点热度
vega = arctern.util.vega.vega_heatmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], map_zoom_level=10.0, coordinate_system="EPSG:4326")

res = heatmap(vega, df)
```

## choroplethmap
```python
def choroplethmap(vega: VegaChoroplethMap, df: DataFrame) -> base64 encoded png
```
- 函数功能: 绘制轮廓图

- 参数: 
```
vega: VegaChoroplethMap的python对象
df: 包含两列数据的dataframe,第一列都是WKB类型的points,第二列为数值类型的数据
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
#df包含2列series,第一列Series表示多边形,第二列数据表示多边形的权值
vega = arctern.util.vega.vega_choroplethmap(1900, 1410, bounding_box=[-73.994092, 40.753893, -73.977588, 40.759642], color_gradient=["#0000FF", "#FF0000"], color_bound=[2.5, 5], opacity=1.0, coordinate_system="EPSG:4326")

res = choroplethmap(vega1, df)
```