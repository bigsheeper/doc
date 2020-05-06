# vega 接口

<font size="5">**vega_pointmap**</font><br /> 

**arctern.util.vega.vega_pointmap(width,height,bounding_box,point_size,point_color,
opacity,coordinate_system)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述点图渲染样式的 VegaPointMap 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应地理坐标 (x_max, y_max)。

&#x2002; &#x2003; &#x2002; &#x2003; * point_size(int) -- 可选参数，表示点的直径，默认值为 3。

&#x2002; &#x2003; &#x2002; &#x2003; * point_color(str) -- 可选参数，表示点的颜色，使用十六进制的颜色编码(Hex Color Code)表示，默认值为"#115f9a"。

&#x2002; &#x2003; &#x2002; &#x2003; * opacity(float) -- 可选参数，表示点的不透明度，范围为 0.0 ~ 1.0，默认值为 1.0。

&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.pointmap.vega_pointmap.VegaPointMap


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaPointMap 对象。


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896的点图，点直径为3的，颜色为蓝色，不透明度为1.0
      >>> vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63])
      >>> 
      >>> # 绘制宽为1024，高为896的点图，点直径为3的，颜色为蓝色，不透明度为0.5
      >>> vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], point_size=10, point_color="#FF0000", opacity=0.5, coordinate_system="EPSG:4326")
   ```


<font size="5">**vega_weighted_pointmap**</font><br /> 

**arctern.util.vega.vega_weighted_pointmap(width,height,bounding_box,color_gradient,
color_bound,size_bound,opacity,coordinate_system)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述带权点图渲染样式的 VegaWeightedPointMap 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应地理坐标 (x_max, y_max)。

&#x2002; &#x2003; &#x2002; &#x2003; * color_gradient(list) -- 点的颜色渐变范围，表示形式为 ["hex_color"] 或 ["hex_color1", "hex_color2"]。当形式为["hex_color"] 时所有点的颜色相同。当形式为["hex_color1", "hex_color2"] 时点的颜色由输入数据中一列的值（权重）决定，且颜色在 "hex_color1" ~ "hex_color2" 之间变化。

&#x2002; &#x2003; &#x2002; &#x2003; * color_bound(list) -- 可选参数，用于描述权重与颜色的对应关系，仅当color_gradient中包含两个颜色值时需要设置，表示形式为 [color_min, color_max]。权重值小于等于 color_min 时点的颜色为"hex_color1"， 权重值大于等于 color_max 时点的颜色为"hex_color2"。

&#x2002; &#x2003; &#x2002; &#x2003; * size_bound(list) -- 可选参数，用于描述点的直径范围，表示形式为 [diameter] 或 [diameter_min, diameter_max]，默认值为[3]。[diameter] 形式表示所有点的直径都为 diameter; [diameter_min, diameter_max] 形式表示点的直径由输入数据中一列的值（权重）决定，且在 diameter_min ~ diameter_max 之间变化; 权重值小于等于 diameter_min 时点的直径为 diameter_min，权重值大于等于 diameter_max 时点的直径为 diameter_max; 权重值在 diameter_min ~ diameter_max 之间时点的直径与权重值相等。

&#x2002; &#x2003; &#x2002; &#x2003; * opacity(float) -- 可选参数，表示点的不透明度，范围为 0.0 ~ 1.0，默认值为 1.0。

&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.pointmap.vega_weighted_pointmap.VegaWeightedPointMap


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaWeightedPointMap 对象。


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896的带权点图，点的颜色相同，直径不同
      >>> vega1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#87CEEB"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")
      >>> 
      >>> # 绘制宽为1024，高为896的带权点图，点的颜色不同，直径相同
      >>> vega2_1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], opacity=0.5, coordinate_system="EPSG:4326")
      >>> vega2_2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[10], coordinate_system="EPSG:4326")
      >>> 
      >>> # 绘制宽为1024，高为896的带权点图，点的颜色和直径都不同
      >>> vega3_1 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], opacity=0.5, coordinate_system="EPSG:4326")
      >>> vega3_2 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816],color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10], coordinate_system="EPSG:4326")
      >>> vega3_3 = arctern.util.vega.vega_weighted_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[1, 10])
   ```


<font size="5">**vega_heatmap**</font><br /> 

**arctern.util.vega.vega_heatmap(width,height,bounding_box,map_zoom_level,
coordinate_system,aggregation_type)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述热力图渲染样式的 VegaHeatMap 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应地理坐标 (x_max, y_max)。

&#x2002; &#x2003; &#x2002; &#x2003; * map_zoom_level(float) -- 热力的辐射范围，与mapbox的地图放大比例相对应，取值范围为 1.0 ~ 15.0。

&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>。

&#x2002; &#x2003; &#x2002; &#x2003; * aggregation_type(str) -- 可选参数，表示输入数据到图片像素热力的聚合方式，默认值为"max"。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.heatmap.vega_heatmap.VegaHeatMap


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaHeatMap 对象。


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896的热力图
      >>> vega = arctern.util.vega.vega_heatmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], map_zoom_level=10.0, coordinate_system="EPSG:4326")
   ```


<font size="5">**vega_choroplethmap**</font><br /> 

**arctern.util.vega.vega_choroplethmap(width,height,bounding_box,color_gradient,
color_bound,opacity,coordinate_system,aggregation_type)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述轮廓图渲染样式的 VegaChoroplethMap 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应地理坐标 (x_max, y_max)。

&#x2002; &#x2003; &#x2002; &#x2003; * color_gradient(list) -- 轮廓的颜色渐变范围，表示形式为 ["hex_color"] 或 ["hex_color1", "hex_color2"]。当形式为["hex_color"] 时所有轮廓的颜色相同。当形式为["hex_color1", "hex_color2"] 时轮廓的颜色由输入数据中一列的值（权重）决定，且颜色在 "hex_color1" ~ "hex_color2" 之间变化。

&#x2002; &#x2003; &#x2002; &#x2003; * color_bound(list) -- 可选参数，用于描述权重与颜色的对应关系，仅当color_gradient中包含两个颜色值时需要设置，表示形式为 [color_min, color_max]。权重值小于等于 color_min 时点的颜色为"hex_color1"， 权重值大于等于 color_max 时点的颜色为"hex_color2"。

&#x2002; &#x2003; &#x2002; &#x2003; * opacity(float) -- 可选参数，表示轮廓的不透明度，范围为 0.0 ~ 1.0，默认值为 1.0。

&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>。

&#x2002; &#x2003; &#x2002; &#x2003; * aggregation_type(str) -- 可选参数，表示输入数据到轮廓权重的聚合方式，默认值为"sum"。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.choroplethmap.vega_choroplethmap.VegaChoroplethMap


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaChoroplethMap 对象。


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896的轮廓图，颜色范围在蓝色和红色之间
      >>> vega = arctern.util.vega.vega_choroplethmap(1024, 896, bounding_box=[-73.994092, 40.753893, -73.977588, 40.759642], color_gradient=["#0000FF", "#FF0000"], color_bound=[2.5, 5], opacity=0.5, coordinate_system="EPSG:4326")
   ```


<font size="5">**vega_icon**</font><br /> 

**arctern.util.vega.vega_icon(width,height,bounding_box,icon_path,coordinate_system)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述图标图渲染样式的 VegaIcon 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数。

&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应地理坐标 (x_max, y_max)。

&#x2002; &#x2003; &#x2002; &#x2003; * icon_path(str) -- 图标png文件的绝对路径 | 图标png文件的绝对路径。在集群模式下，该图片需要被存储在集群所用的文件系统中。

&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.icon.vega_icon.VegaIcon


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaIcon 对象。


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896的图标图
      >>> vega = arctern.util.vega.vega_icon(1024, 896, bounding_box=[-73.994092, 40.753893, -73.977588, 40.759642], icon_path='path_to_icon_example.png', coordinate_system="EPSG:4326")
   ```




















# pandas 接口

<font size="5">**point_map_layer**</font><br /> 

**arctern.point_map_layer(vega, points)**

&#x2002; &#x2003; 绘制点图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaPointMap) -- VegaPointMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(Series(dtype: object)) -- 所需绘制的点，格式为WKB。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> import pandas as pd
      >>> import numpy as np
      >>> import arctern
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_pointmap
      >>> 
      >>> # 读取 csv 文件并创建绘图数据
      >>> df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
      >>> region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))']))
      >>> d = pd.DataFrame(region).T
      >>> region = region.append([d]*df.shape[0])
      >>> in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
      >>> df['in_region']=in_region
      >>> input1 = df[df.in_region == True].head(10000)
      >>> 
      >>> points = arctern.ST_Point(input1['longitude'], input1['latitude'])
      >>> 
      >>> # 绘制点大小为3，点颜色为#2DEF4A，点不透明度为0.5的点图
      >>> vega = vega_pointmap(1903, 1777, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=3, point_color="#2DEF4A", opacity=0.5, coordinate_system="EPSG:4326")
      >>> png = arctern.point_map_layer(vega, points)
      >>> save_png(png, "/tmp/python_pointmap.png")
   ```


<font size="5">**weighted_point_map_layer**</font><br /> 

**arctern.weighted_point_map_layer(vega, points, color_weights, size_weights)**

&#x2002; &#x2003; 绘制带权重的点图，权重用于决定点的大小和颜色。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaWeightedPointMap) -- VegaWeightedPointMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(Series(dtype: object)) -- 所需绘制的点，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * color_weights(Series(dtype: float64|int64)) -- 可选参数，点的颜色权重。

&#x2002; &#x2003; &#x2002; &#x2003; * size_weights(Series(dtype: float64|int64)) -- 可选参数，点的大小权重。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> import pandas as pd
      >>> import numpy as np
      >>> import arctern
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_weighted_pointmap
      >>> 
      >>> # 读取 csv 文件并创建绘图数据
      >>> df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
      >>> region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))']))
      >>> d=pd.DataFrame(region).T
      >>> region = region.append([d]*df.shape[0])
      >>> in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
      >>> df['in_region']=in_region
      >>> input1 = df[df.in_region == True].head(20000).reset_index()
      >>> input2 = df[df.in_region == True].head(2000).reset_index()
      >>> 
      >>> points1 = arctern.ST_Point(input1['longitude'], input1['latitude'])
      >>> points2 = arctern.ST_Point(input2['longitude'], input2['latitude'])
      >>> 
      >>> # 绘制带权点图，点的大小为 10，点的颜色根据 input1['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化
      >>> vega1 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#0000FF", "#FF0000"], color_bound=[1, 5], size_bound=[10], opacity=1.0, coordinate_system="EPSG:4326")
      >>> png1 = arctern.weighted_point_map_layer(vega1, points1, color_weights=input1['color_weights'])
      >>> save_png(png1, "/tmp/python_weighted_pointmap1.png")  
      >>> 
      >>> # 绘制带权点图，点的颜色为'#37A2DA'，点的大小根据 input2['size_weights'] 在 1 ~ 10 之间变化
      >>> vega2 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")
      >>> png2 = arctern.weighted_point_map_layer(vega2, points2, size_weights=input2['size_weights'])
      >>> save_png(png2, '/tmp/python_weighted_pointmap2.png')  
      >>> 
      >>> # 绘制带权点图，点的颜色根据 input2['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化，点的大小根据 input2['size_weights'] 在 1 ~ 10 之间变化
      >>> vega3 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#0000FF", "#FF0000"], color_bound=[1,5], size_bound=[1, 10], opacity=1.0, coordinate_system="EPSG:4326")
      >>> png3 = arctern.weighted_point_map_layer(vega3, points2, color_weights=input2['color_weights'], size_weights=input2['size_weights'])
      >>> save_png(png3, '/tmp/python_weighted_pointmap3.png')
   ```


<font size="5">**heat_map_layer**</font><br /> 

**arctern.heat_map_layer(vega, points, weights)**

&#x2002; &#x2003; 根据点的位置和热力值绘制热力图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaHeatMap) -- VegaHeatMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(Series(dtype: object)) -- 点的位置，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * weights(Series(dtype: float64|int64)) -- 热力值。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> import pandas as pd
      >>> import numpy as np
      >>> import arctern
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_heatmap
      >>> 
      >>> # 读取 csv 文件并创建绘图数据
      >>> df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
      >>> region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
      >>> d=pd.DataFrame(region).T
      >>> region = region.append([d]*df.shape[0])
      >>> in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
      >>> df['in_region']=in_region
      >>> input1 = df[df.in_region == True].reset_index()
      >>> 
      >>> points = arctern.ST_Point(input1['longitude'], input1['latitude'])
      >>> 
      >>> # 根据 input1['color_weights'] 绘制热力图
      >>> vega = vega_heatmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=10.0, coordinate_system='EPSG:4326')
      >>> png = arctern.heat_map_layer(vega, points, input1['color_weights'])
      >>> save_png(png, "/tmp/python_heatmap.png") 
   ```


<font size="5">**choropleth_map_layer**</font><br /> 

**arctern.choropleth_map_layer(vega, region_boundaries, weights)**

&#x2002; &#x2003; 绘制轮廓图，权重用于决定轮廓的填充颜色。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaChoroplethMap) -- VegaChoroplethMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(Series(dtype: object)) -- 所需绘制的多边形轮廓，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * weights(Series(dtype: float64|int64)) -- 轮廓的颜色权重。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> import pandas as pd
      >>> import numpy as np
      >>> import arctern
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_choroplethmap
      >>> 
      >>> # 读取 csv 文件并创建绘图数据
      >>> df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
      >>> input1 = df[pd.notna(df['region_boundaries'])].groupby(['region_boundaries']).mean().reset_index()
      >>> polygon = arctern.ST_GeomFromText(input1['region_boundaries'])
      >>> 
      >>> # 绘制轮廓图，轮廓的填充颜色根据 input1['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化
      >>> vega = vega_choroplethmap(1922, 1663, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#0000FF","#FF0000"], color_bound=[2.5, 5], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean") 
      >>> png = arctern.choropleth_map_layer(vega, polygon, input1['color_weights'])
      >>> save_png(png, "/tmp/python_choroplethmap.png")
   ```


<font size="5">**icon_viz_layer**</font><br /> 

**arctern.icon_viz_layer(vega, points)**

&#x2002; &#x2003; 根据坐标位置绘制图标图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaIcon) -- VegaIcon 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(Series(dtype: object)) -- 坐标位置，格式为WKB。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> import pandas as pd
      >>> import numpy as np
      >>> import arctern
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_icon
      >>> 
      >>> # 读取 csv 文件并创建绘图数据
      >>> df = pd.read_csv("test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
      >>> region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
      >>> d=pd.DataFrame(region).T
      >>> region = region.append([d]*df.shape[0])
      >>> in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
      >>> df['in_region']=in_region
      >>> input1 = df[df.in_region == True].reset_index()
      >>> 
      >>> points = arctern.ST_Point(input1['longitude'], input1['latitude'])
      >>> 
      >>> # 根据 input1['color_weights'] 绘制图标图
      >>> vega = vega_icon(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], icon_path='path_to_icon_example.png', coordinate_system='EPSG:4326')
      >>> png = arctern.icon_viz_layer(vega, points)
      >>> save_png(png, "/tmp/python_icon_viz.png")
   ```




















# spark 接口

<font size="5">**pointmap**</font><br /> 

**arctern_pyspark.pointmap(vega, points)**

&#x2002; &#x2003; 绘制点图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaPointMap) -- VegaPointMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(WKB) -- 所需绘制的点，格式为WKB。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_pointmap
      >>> from arctern_pyspark import register_funcs
      >>> from arctern_pyspark import pointmap
      >>> from pyspark.sql import SparkSession
      >>> 
      >>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
      >>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
      >>> 
      >>> table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
      >>>     "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
      >>>     "file:///tmp/test_data.csv").cache()
      >>> table_df.createOrReplaceTempView("test_table")
      >>> 
      >>> register_funcs(spark)
      >>> 
      >>> # df 是包含 1 列数据的 pyspark.Dataframe, 该列为 WKB 类型的points
      >>> # 绘制点大小为10，点颜色为#37A2DA，点不透明度为1.0的点图
      >>> df = spark.sql("SELECT ST_Point (longitude, latitude) AS point FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))'))) LIMIT 10000")
      >>> vega = vega_pointmap(1903, 1777, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=10, point_color="#37A2DA", opacity=1.0, coordinate_system="EPSG:4326")
      >>> res = pointmap(vega, df)
      >>> save_png(res, '/tmp/pointmap.png')
      >>> 
      >>> spark.sql("show tables").show()
      >>> spark.catalog.dropGlobalTempView("test_table")
   ```


<font size="5">**weighted_pointmap**</font><br /> 

**arctern_pyspark.weighted_pointmap(vega, points, color_weights, size_weights)**

&#x2002; &#x2003; 绘制带权重的点图，权重用于决定点的大小和颜色。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaWeightedPointMap) -- VegaWeightedPointMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(WKB) -- 所需绘制的点，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * color_weights(int|float) -- 可选参数，点的颜色权重。

&#x2002; &#x2003; &#x2002; &#x2003; * size_weights(int|float) -- 可选参数，点的大小权重。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_weighted_pointmap
      >>> from arctern_pyspark import register_funcs
      >>> from arctern_pyspark import weighted_pointmap
      >>> from pyspark.sql import SparkSession
      >>> 
      >>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
      >>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
      >>> 
      >>> table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
      >>>     "longitude double, latitude double, color_weights double, size_weights double,region_boundaries string").load(
      >>>     "file:///tmp/test_data.csv").cache()
      >>> table_df.createOrReplaceTempView("test_table")
      >>> 
      >>> register_funcs(spark)
      >>> 
      >>> # df1 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点颜色的权重数据
      >>> # 绘制带权点图，点的颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化，点的大小为 16   
      >>> df1 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 20000")
      >>> vega1 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[16], opacity=1.0, coordinate_system="EPSG:4326")
      >>> res1 = weighted_pointmap(vega1, df1)
      >>> save_png(res1, '/tmp/weighted_pointmap_1_0.png')
      >>> 
      >>> # df2 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点大小的权重数据
      >>> # 绘制带权点图，点的颜色为'#37A2DA'，点的大小根据 size_weights 在 15 ~ 50 之间变化      
      >>> df2 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, size_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
      >>> vega2 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
      >>> res2 = weighted_pointmap(vega2, df2)
      >>> save_png(res2, '/tmp/weighted_pointmap_0_1.png')
      >>> 
      >>> # df3 是包含 3 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点颜色的权重数据，第三列为点大小的权重数据
      >>> # 绘制带权点图，点的颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化，点的大小根据 size_weights 在 15 ~ 50 之间变化      
      >>> df3 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights, size_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
      >>> vega3 = vega_weighted_pointmap(1740, 1767, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
      >>> res3 = weighted_pointmap(vega3, df3)
      >>> save_png(res3, '/tmp/weighted_pointmap_1_1.png')
      >>> 
      >>> spark.sql("show tables").show()
      >>> spark.catalog.dropGlobalTempView("test_table")
   ```


<font size="5">**heatmap**</font><br /> 

**arctern_pyspark.heatmap(vega, points, weights)**

&#x2002; &#x2003; 根据点的位置和热力值绘制热力图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaHeatMap) -- VegaHeatMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(WKB) -- 点的位置，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * weights(int|float) -- 热力值。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_heatmap
      >>> from arctern_pyspark import register_funcs
      >>> from arctern_pyspark import heatmap
      >>> from pyspark.sql import SparkSession
      >>> 
      >>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
      >>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
      >>> 
      >>> table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
      >>>     "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
      >>>     "file:///tmp/test_data.csv").cache()
      >>> table_df.createOrReplaceTempView("test_table")
      >>> 
      >>> register_funcs(spark)
      >>> 
      >>> # df 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为热力值
      >>> # 根据 color_weights 绘制热力图      
      >>> df = spark.sql("select ST_Point(longitude, latitude) as point, color_weights from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))'))")
      >>> vega = vega_heatmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=14.544283200495824, coordinate_system='EPSG:4326')
      >>> res = heatmap(vega, df)
      >>> save_png(res, '/tmp/heatmap.png')
      >>> 
      >>> spark.sql("show tables").show()
      >>> spark.catalog.dropGlobalTempView("test_table")
   ```


<font size="5">**choroplemap**</font><br /> 

**arctern_pyspark.choroplemap(vega, region_boundaries, weights)**

&#x2002; &#x2003; 绘制轮廓图，权重用于决定轮廓的填充颜色。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaChoroplethMap) -- VegaChoroplethMap 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * region_boundaries(WKB) -- 所需绘制的多边形轮廓，格式为WKB。

&#x2002; &#x2003; &#x2002; &#x2003; * weights(int|float) -- 轮廓的颜色权重。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_choroplethmap
      >>> from arctern_pyspark import register_funcs
      >>> from arctern_pyspark import choroplethmap
      >>> from pyspark.sql import SparkSession
      >>> 
      >>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
      >>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
      >>> 
      >>> table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
      >>>     "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
      >>>     "file:///tmp/test_data.csv").cache()
      >>> table_df.createOrReplaceTempView("test_table")
      >>> 
      >>> register_funcs(spark)
      >>> # df 是包含 2 列数据的 pyspark.Dataframe， 第一列为 WKB 类型的polygons，第二列为轮廓填充颜色的权重
      >>> # 绘制轮廓图，轮廓的填充颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化
      >>> df = spark.sql("SELECT ST_GeomFromText(region_boundaries) AS wkb, color_weights AS color FROM test_table WHERE ((region_boundaries !=''))")
      >>> vega = vega_choroplethmap(1922, 1663, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#115f9a","#d0f400"], color_bound=[5,18], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean") 
      >>> res = choroplethmap(vega, df)
      >>> save_png(res, '/tmp/choroplethmap1.png')
      >>> 
      >>> spark.sql("show tables").show()
      >>> spark.catalog.dropGlobalTempView("test_table")
   ```


<font size="5">**icon_viz**</font><br /> 

**arctern_pyspark.icon_viz(vega, points)**

&#x2002; &#x2003; 根据坐标位置绘制图标图。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * vega(VegaIcon) -- VegaIcon 对象。

&#x2002; &#x2003; &#x2002; &#x2003; * points(WKB) -- 坐标位置，格式为WKB。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; bytes


&#x2002; &#x2003; 返回

&#x2002; &#x2003; &#x2002; &#x2003; base64编码的png图片。


&#x2002; &#x2003; 示例:

  ```python
      >>> from arctern.util import save_png
      >>> from arctern.util.vega import vega_icon
      >>> from arctern_pyspark import register_funcs
      >>> from arctern_pyspark import icon_viz
      >>> from pyspark.sql import SparkSession
      >>> 
      >>> spark_session = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
      >>> spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
      >>> 
      >>> table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
      >>>     "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
      >>>     "file:///tmp/test_data.csv").cache()
      >>> table_df.createOrReplaceTempView("test_table")
      >>> 
      >>> register_funcs(spark)
      >>> 
      >>> # df 是包含 1 列数据的 pyspark.Dataframe，该列为 WKB 类型的points
      >>> # 根据 point 数据绘制图标图
      >>> df = spark.sql("select ST_Point(longitude, latitude) as point from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))'))")
      >>> vega = vega_icon(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], icon_path='path_to_icon_example.png', coordinate_system='EPSG:4326')
      >>> res = icon_viz(vega, df)
      >>> save_png(res, '/tmp/icon_viz.png')
      >>> 
      >>> spark.sql("show tables").show()
      >>> spark.catalog.dropGlobalTempView("test_table")
   ```