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
- 函数功能: 设置用于渲染的输入数据的地理范围和地理坐标系统，目标图片的宽和高，以及点图中点的直径，颜色，不透明度

- 参数: 
```
width(int): 图片宽度，单位是像素
height(int): 图片高度，单位是像素
bounding_box(list): 渲染图片所表示的地理范围，参数以 [x_min, y_min, x_max, y_max] 的形式表示的一个矩形区域，图片左下角的像素坐标 (0, 0) 表示实际地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 表示地理坐标 (x_max, y_max) 
point_size(int): 可选参数，表示点的直径，默认值为3
point_color(str): 可选参数，表示点的颜色，使用十六进制的颜色值表示，默认值为"#115f9a"
opacity(float): 可选参数，表示点的不透明度，默认值为1.0
coordinate_system(str): 可选参数，表示输入数据的坐标系统，默认值为"EPSG:3857"，可选的坐标系统请参照 <https://spatialreference.org/ref/epsg/>
```

- 返回值: 用于描述渲染样式的 VegaPointMap 对象
- 返回值类型: `arctern.util.vega.pointmap.vega_pointmap.VegaPointMap` TODO

- 示例: 
```python
# 绘制宽为1024，高为896，点直径为3的，点颜色为蓝色的完全不透明点图
vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63])


# 绘制宽为1024，高为896，点直径为10的，点颜色为红色的半透明点图
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
- 函数功能: 设置用于渲染的输入数据的地理范围和地理坐标系统，目标图片的宽和高，以及点图中点的直径范围，颜色范围，透明度

- 参数: 
```
width(int): 图片宽度，单位是像素
height(int): 图片高度，单位是像素
bounding_box(list): 渲染图片所表示的地理范围，参数以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域，图片z左下角的像素坐标 (0, 0) 表示实际地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 表示地理坐标 (x_max, y_max) 
color_gradient(list): 点的颜色渐变范围，表示形式为 ["0000FF"] 或 ["#0000FF", "FF0000"] ， ["0000FF"] 表示所有的点颜色相同， ["#0000FF", "FF0000"] 表示点的颜色可变，点的颜色由输入的color_weight列的权重值决定
color_bound(list): 可选参数，表示控制颜色的权重值范围，表示形式为 [1, 10] ，只有当color_gradient的list中包含两个颜色值(比如 ["#0000FF", "#FF0000"] )时需要设置，权重值等于1时点的颜色值为"#0000FF"， 权重值等于10时点的颜色值为"#FF0000"
size_bound(list): 可选参数，表示控制点直径的权重值范围，表示形式为 [10] 或 [1, 10] ， [10] 表示所有点的直径都为10， [1, 10] 表示点大小可变，权重值等于1时，点的直径为1，权重值等于10时，点的直径为10，默认值为[3]
opacity(float): 可选参数，点的不透明度，默认值为1.0
coordinate_system(str): 可选参数，表示输入数据的坐标系统，默认值为"EPSG:3857"，可选的坐标系统请参照 <https://spatialreference.org/ref/epsg/>
```

- 返回值: 用于描述渲染样式的 VegaWeightedPointMap 对象
- 返回值类型: `arctern.util.vega.pointmap.vega_weighted_pointmap.VegaWeightedPointMap` TODO

- 示例: 
```python
# 绘制宽为1024，高为896，点颜色相同，直径不同的权重点图
vega1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#87CEEB"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")


# 绘制宽为1024，高为896，点颜色不同，直径相同的权重点图
vega2_1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], opacity=0.5, coordinate_system="EPSG:4326")

vega2_2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[10], coordinate_system="EPSG:4326")


# 绘制宽为1024，高为896，点颜色和直径都不同的权重点图
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

- 函数功能: 设置用于渲染的输入数据的地理范围，地理坐标系统，数据聚合操作类型，目标图片的宽和高，以及影响热力图中的热度辐射范围的地图放大比例

- 参数: 
```
width(int): 图片宽度，单位是像素
height(int): 图片高度，单位是像素
bounding_box(list): 渲染图片所表示的地理范围，参数以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域，图片z左下角的像素坐标 (0, 0) 表示实际地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 表示地理坐标 (x_max, y_max) 
map_zoom_level(float): 地图放大比例，mapbox 取值范围 (1 ~ 15) 
coordinate_system(str): 可选参数，表示输入数据的坐标系统，默认值为"EPSG:3857"，可选的坐标系统请参照 <https://spatialreference.org/ref/epsg/>
aggregation_type(str): 可选参数，数据聚合操作类型，默认值为"max"
```

- 返回值: 用于描述渲染样式的 VegaHeatMap 对象
- 返回值类型: `arctern.util.vega.heatmap.vega_heatmap.VegaHeatMap` TODO

- 示例: 
```python
# 绘制宽为1024，高为896的热力图
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
- 函数功能: 设置用于渲染的输入数据的地理范围，地理坐标系统，数据聚合操作类型，目标图片的宽和高，以及轮廓图的颜色范围，透明度

- 参数:
```
width(int): 图片宽度，单位是像素
height(int): 图片高度，单位是像素
bounding_box(list): 渲染图片所表示的地理范围，参数以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域，图片z左下角的像素坐标 (0, 0) 表示实际地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 表示地理坐标 (x_max, y_max) 
color_gradient(list): 点的颜色渐变范围，表示形式为 ["#0000FF", "FF0000"] ，点的颜色由输入的 color_weight 列的权重值决定
color_bound(list): 控制颜色的权重值范围，表示形式为 [1, 10] ，如果 color_gradient=["#0000FF", "#FF0000"] ，权重值等于1时点的颜色值为"#0000FF"， 权重值等于10时点的颜色值为"#FF0000"
opacity(float): 可选参数，表示点的不透明度，默认值为1.0
coordinate_system(str): 可选参数，表示输入数据的坐标系统，默认值为"EPSG:3857"，可选的坐标系统请参照 <https://spatialreference.org/ref/epsg/>
aggregation_type(str): 可选参数，数据聚合操作类型，默认值为"sum"
```

- 返回值: 用于描述渲染样式的 VegaChoroplethMap 对象

- 返回值类型: `arctern.util.vega.choroplethmap.vega_choroplethmap.VegaChoroplethMap` TODO

- 示例: 
```python
# 绘制宽为1024，高为896，颜色值在蓝色和红色之间的轮廓图
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
vega: VegaPointMap 对象
points: 包含一列points的Series，point的类型为wkb
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_pointmap

# 读取csv文件
df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})

# 创建包含points的dataframe
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))']))
d = pd.DataFrame(region).T
region = region.append([d]*df.shape[0])
in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].head(10000)

points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# 绘制点大小为3，点颜色为#2DEF4A，点不透明度为0.5的点图
vega = vega_pointmap(1903, 1777, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=3, point_color="#2DEF4A", opacity=0.5, coordinate_system="EPSG:4326")
png = arctern.point_map(vega, points)
save_png(png, "/tmp/python_pointmap.png")
```

## weighted_pointmap
```python
def weighted_point_map(vega, points, color_weights, size_weights)
```
- 函数功能: 绘制带权重的点图，图中点的大小和颜色不同

- 参数: 
```python
vega: VegaWeightedPointMap 对象
points: 包含一列points的Series，point的类型为WKB
color_weights: 包含一列数值类型数据的Series
size_weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_weighted_pointmap

# 读取csv文件
df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})

# 创建包含points的dataframe
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))']))
d=pd.DataFrame(region).T
region = region.append([d]*df.shape[0])
in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].head(20000).reset_index()
input2 = df[df.in_region == True].head(2000).reset_index()

points1 = arctern.ST_Point(input1['longitude'], input1['latitude'])
points2 = arctern.ST_Point(input2['longitude'], input2['latitude'])

# color_gradient 的 list 中只有一个元素，表示点的颜色都为#87CEEB，此时可以不指定 color_bound
# size_bound=[1,10] 表示 size_weights series 中最小值对应的点大小为 1 ，最大值对应的点大小为 10
vega1 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[1,10], opacity=1.0, coordinate_system="EPSG:4326")
png1 = arctern.weighted_point_map(vega1, points1, color_weights=input1['color_weights'])
save_png(png1, "/tmp/python_weighted_pointmap1.png")  

# color_bound 和 color_gradient 的 list 同时包含两个元素，color_bound 中的 1 和 5 分别对应 color_weights series 中的最小值和最大值，最小值代表的点的颜色为#0000FF，最大值代表的点的颜色为#FF0000
# size_bound=[10] 表示点大小为 10
vega2 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[10], opacity=1.0, coordinate_system="EPSG:4326")
png2 = arctern.weighted_point_map(vega2, points2, size_weights=input2['size_weights'])
save_png(png2, '/tmp/python_weighted_pointmap2.png')  

# color_bound 和 color_gradient 的 list 同时包含两个元素，color_bound 中的 1 和 5 分别对应 color_weights series 中的最小值和最大值，其最小值代表的点的颜色为#0000FF，最大值代表的点的颜色为#FF0000
# size_bound=[1,10] 表示 size_weights series 中最小值对应的点大小为 1 ，最大值对应的点大小为 10
vega3 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#0000FF", "#FF0000"], color_bound=[1,5], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")
png3 = arctern.weighted_point_map(vega3, points2, color_weights=input2['color_weights'], size_weights=input2['size_weights'])
save_png(png3, '/tmp/python_weighted_pointmap3.png')
```

## heatmap
```python
def heat_map(vega, points, weights)
```
- 函数功能: 绘制热力图

- 参数: 
```json
vega: VegaHeatMap 对象
points: 包含一列point的Series，point的类型为wkb
weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_heatmap

# 读取csv文件
df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})

# 创建包含points的dataframe
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
d=pd.DataFrame(region).T
region = region.append([d]*df.shape[0])
in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].reset_index()

points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# 地图放大比例为10.0，输入数据的坐标系统为EPSG:4326
vega = vega_heatmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=10.0, coordinate_system='EPSG:4326')
png = arctern.heat_map(vega, points, input1['color_weights'])
save_png(png, "/tmp/python_heatmap.png")   
```

## choroplemap
```python
def choropleth_map(vega, region_boundaries, weights)
```
- 函数功能: 绘制轮廓图

- 参数:
```json
vega: VegaChoroplethMap 对象
region_boundaries: 包含一列多边形的Series，多边形的类型为WKB
weights: 包含一列数值类型数据的Series
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_choroplethmap

# 读取csv文件
df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})

# 创建包含polygon的dataframe
input1 = df[pd.notna(df['region_boundaries'])].groupby(['region_boundaries']).mean().reset_index()
polygon = arctern.ST_GeomFromText(input1['region_boundaries'])

# color_gradient 和 color_bound 的 list 同时包含两个元素，color_bound 中的 2.5 和 5 分别对应 weights series 中的最小值和最大值，其最小值代表的多边形的颜色为#0000FF，最大值代表的多边形的颜色为#FF0000
vega = vega_choroplethmap(1922, 1663, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#0000FF","#FF0000"], color_bound=[2.5, 5], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean") 
png = arctern.choropleth_map(vega, polygon, input1['color_weights'])
save_png(png, "/tmp/python_choroplethmap.png")
```



# pyspark 接口

## pointmap
```python
def pointmap(vega, df)
```
- 函数功能: 绘制点图

- 参数: 
```json
vega: VegaPointMap 对象
df: 包含一列points的dataframe，point的类型为wkb
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例:
```python
from arctern.util import save_png
from arctern.util.vega import vega_pointmap

from arctern_pyspark import register_funcs
from arctern_pyspark import pointmap

from pyspark.sql import SparkSession

def draw_point_map(spark):
    table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
        "file:///tmp/test_data.csv").cache()
    table_df.createOrReplaceTempView("test_table")

    register_funcs(spark)

    # 和 spark 的画图结合同样和 vega 接口配合使用，等同于python画图的使用方式
    # df 是只有一列数据的 pyspark dataframe, 该列数据的表示点坐标，类型为 wkb 格式的 point
    df = spark.sql("SELECT ST_Point (longitude, latitude) AS point FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))'))) LIMIT 10000")
    vega = vega_pointmap(1903, 1777, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=10, point_color="#37A2DA", opacity=1.0, coordinate_system="EPSG:4326")
    res = pointmap(vega, df)
    save_png(res, '/tmp/pointmap.png')

    spark.sql("show tables").show()
    spark.catalog.dropGlobalTempView("test_table")

if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_point_map(spark_session)

    spark_session.stop()
```

## weighted_pointmap
```python
def weighted_pointmap(vega, df)
```
- 函数功能: 绘制带权重的点图，点的大小和颜色不同

- 参数: 
```json
vega: VegaWeightedPointMap 对象
df: 包含两列或三列数据的dataframe，第一列都是wkb类型的points，第二列或第三列为数值类型的数据
```

- 返回值: base64 encoded png

- 返回值类型: `bytes`

- 示例: 
```python
from arctern.util import save_png
from arctern.util.vega import vega_weighted_pointmap

from arctern_pyspark import register_funcs
from arctern_pyspark import weighted_pointmap

from pyspark.sql import SparkSession

def draw_weighted_point_map(spark):
    table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "longitude double, latitude double, color_weights double, size_weights double,region_boundaries string").load(
        "file:///tmp/test_data.csv").cache()
    table_df.createOrReplaceTempView("test_table")

    register_funcs(spark)

    # df1 包含 2 列 series ，第一列为wkb类型的points，第二列为点颜色大小的权重数据
    df1 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 20000")
    vega1 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[16], opacity=1.0, coordinate_system="EPSG:4326")
    res1 = weighted_pointmap(vega1, df1)
    save_png(res1, '/tmp/weighted_pointmap_1_0.png')

    # df2 包含 2 列 series ，第一列为wkb类型的points，第二列为点大小的权重数据
    df2 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
    vega2 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
    res2 = weighted_pointmap(vega2, df2)
    save_png(res2, '/tmp/weighted_pointmap_0_1.png')

    # df3 包含 3 列 series ，第一列为wkb类型的points，第二列为点颜色的权重数据，第三列为点大小的权重数据
    df3 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights, size_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
    vega3 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
    res3 = weighted_pointmap(vega3, df3)
    save_png(res3, '/tmp/weighted_pointmap_1_1.png')

    spark.sql("show tables").show()
    spark.catalog.dropGlobalTempView("test_table")

if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_weighted_point_map(spark_session)

    spark_session.stop()
```

## heatmap
```python
def heatmap(vega: VegaHeatMap, df: DataFrame) -> base64 encoded png
```
- 函数功能: 绘制热力图

- 参数: 
```json
vega: VegaHeatMap 对象
df: 包含两列数据的 dataframe ，第一列都是wkb类型的points，第二列为数值类型的数据
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
from arctern.util import save_png
from arctern.util.vega import vega_heatmap

from arctern_pyspark import register_funcs
from arctern_pyspark import heatmap

from pyspark.sql import SparkSession

def draw_heat_map(spark):
    table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
        "file:///tmp/test_data.csv").cache()
    table_df.createOrReplaceTempView("test_table")

    register_funcs(spark)

    # df 包含 2 列 series ，第一列为wkb类型的points，第二列数据表示点热度
    df = spark.sql("select ST_Point(longitude, latitude) as point, color_weights from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))'))")
    vega = vega_heatmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=14.544283200495824, coordinate_system='EPSG:4326')
    res = heatmap(vega, df)
    save_png(res, '/tmp/heatmap.png')

    spark.sql("show tables").show()
    spark.catalog.dropGlobalTempView("test_table")

if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_heat_map(spark_session)

    spark_session.stop()
```

## choroplethmap
```python
def choroplethmap(vega: VegaChoroplethMap, df: DataFrame) -> base64 encoded png
```
- 函数功能: 绘制轮廓图

- 参数: 
```
vega: VegaChoroplethMap 对象
df: 包含两列数据的dataframe，第一列都是wkb类型的points，第二列为数值类型的数据
```

- 返回值: base64 encoded png
- 返回值类型: `bytes`

- 示例: 
```python
from arctern.util import save_png
from arctern.util.vega import vega_choroplethmap

from arctern_pyspark import register_funcs
from arctern_pyspark import choroplethmap

from pyspark.sql import SparkSession

def draw_choropleth_map(spark):
    table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
        "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
        "file:///tmp/test_data.csv").cache()
    table_df.createOrReplaceTempView("test_table")

    register_funcs(spark)
    # df 包含 2 列 series ，wkb类型的polygons，第二列数据表示多边形的权值
    df = spark.sql("SELECT ST_GeomFromText(region_boundaries) AS wkb, color_weights AS color FROM test_table WHERE ((region_boundaries !=''))")

    vega = vega_choroplethmap(1922, 1663, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#115f9a","#d0f400"], color_bound=[5,18], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean") 
    res = choroplethmap(vega, df)
    save_png(res, '/tmp/choroplethmap1.png')

    spark.sql("show tables").show()
    spark.catalog.dropGlobalTempView("test_table")


if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Testmap") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    draw_choropleth_map(spark_session)

    spark_session.stop()
```