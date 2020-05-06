import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_choroplethmap

width = 1824
height = 1777

# # 读取 csv 文件并创建绘图数据
# df = pd.read_csv("/tmp/test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
# input1 = df[pd.notna(df['region_boundaries'])].groupby(['region_boundaries']).mean().reset_index()
# polygon = arctern.ST_GeomFromText(input1['region_boundaries'])

# # 绘制轮廓图，轮廓的填充颜色根据 input1['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化
# vega = vega_choroplethmap(width, height, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#115f9a","#d0f400"], color_bound=[5,18], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean")
# png = arctern.choropleth_map_layer(vega, polygon, input1['color_weights'])
# save_png(png, "/tmp/python_choroplethmap.png")








# from arctern.util.vega import vega_heatmap

# # 读取 csv 文件并创建绘图数据
# df = pd.read_csv("/tmp/test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
# region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
# d=pd.DataFrame(region).T
# region = region.append([d]*(df.shape[0] - 1))
# in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
# df['in_region']=in_region
# input1 = df[df.in_region == True].reset_index()

# points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# # 根据 input1['color_weights'] 绘制热力图
# vega = vega_heatmap(width, height, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=14.544283200495824, coordinate_system='EPSG:4326')
# png = arctern.heat_map_layer(vega, points, input1['color_weights'])
# save_png(png, "/tmp/python_heatmap.png") 






from arctern.util.vega import vega_icon

# 读取 csv 文件并创建绘图数据
df = pd.read_csv("/tmp/test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object}, nrows=10)
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
d=pd.DataFrame(region).T
region = region.append([d]*(df.shape[0] - 1))
in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].reset_index()

points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# 根据 input1['color_weights'] 绘制图标图
vega = vega_icon(width, height, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], icon_path='/tmp/taxi.png', coordinate_system='EPSG:4326')
png = arctern.icon_viz_layer(vega, points)
save_png(png, "/tmp/python_icon_viz.png")








# from arctern.util.vega import vega_pointmap

# # 读取 csv 文件并创建绘图数据
# df = pd.read_csv("/tmp/test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
# region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))']))
# d = pd.DataFrame(region).T
# region = region.append([d]*(df.shape[0] - 1))
# in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
# df['in_region']=in_region
# input1 = df[df.in_region == True].head(10000)

# points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# # 绘制点大小为3，点颜色为#2DEF4A，点不透明度为0.5的点图
# vega = vega_pointmap(width, height, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=10, point_color="#115f9a", opacity=1.0, coordinate_system="EPSG:4326")
# png = arctern.point_map_layer(vega, points)
# save_png(png, "/tmp/python_pointmap.png")










# from arctern.util.vega import vega_weighted_pointmap

# # 读取 csv 文件并创建绘图数据
# df = pd.read_csv("/tmp/test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
# region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))']))
# d=pd.DataFrame(region).T
# region = region.append([d]*(df.shape[0] - 1))
# in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
# df['in_region']=in_region
# input1 = df[df.in_region == True].head(20000).reset_index()
# input2 = df[df.in_region == True].head(2000).reset_index()

# points1 = arctern.ST_Point(input1['longitude'], input1['latitude'])
# points2 = arctern.ST_Point(input2['longitude'], input2['latitude'])

# # 绘制带权点图，点的大小为 10，点的颜色根据 input1['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化
# vega1 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[16], opacity=1.0, coordinate_system="EPSG:4326")
# png1 = arctern.weighted_point_map_layer(vega1, points1, color_weights=input1['color_weights'])
# save_png(png1, "/tmp/python_weighted_pointmap_0_1.png")  

# # 绘制带权点图，点的颜色为'#37A2DA'，点的大小根据 input2['size_weights'] 在 1 ~ 10 之间变化
# vega2 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
# png2 = arctern.weighted_point_map_layer(vega2, points2, size_weights=input2['size_weights'])
# save_png(png2, '/tmp/python_weighted_pointmap_1_0.png')  

# # 绘制带权点图，点的颜色根据 input2['color_weights'] 在 "#0000FF" ~ "#FF0000" 之间变化，点的大小根据 input2['size_weights'] 在 1 ~ 10 之间变化
# vega3 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
# png3 = arctern.weighted_point_map_layer(vega3, points2, color_weights=input2['color_weights'], size_weights=input2['size_weights'])
# save_png(png3, '/tmp/python_weighted_pointmap_1_1.png')