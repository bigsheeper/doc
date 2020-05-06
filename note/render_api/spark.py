from arctern.util import save_png
from arctern.util.vega import vega_choroplethmap
from arctern_pyspark import register_funcs
from arctern_pyspark import choroplethmap
from pyspark.sql import SparkSession

width = 1824
height = 1777

spark = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

register_funcs(spark)

table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema(
    "longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load(
    "file:///tmp/test_data.csv").cache()
table_df.createOrReplaceTempView("test_table")

# df 是包含 2 列数据的 pyspark.Dataframe， 第一列为 WKB 类型的polygons，第二列为轮廓填充颜色的权重
# 绘制轮廓图，轮廓的填充颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化
df = spark.sql("SELECT ST_GeomFromText(region_boundaries) AS wkb, color_weights AS color FROM test_table WHERE ((region_boundaries !=''))")
vega = vega_choroplethmap(width, height, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], color_gradient=["#115f9a","#d0f400"], color_bound=[5,18], opacity=1.0, coordinate_system='EPSG:4326', aggregation_type="mean") 
res = choroplethmap(vega, df)
save_png(res, '/tmp/choroplethmap.png')

spark.sql("show tables").show()
spark.catalog.dropGlobalTempView("test_table")




from arctern.util.vega import vega_heatmap
from arctern_pyspark import heatmap

# df 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为热力值
# 根据 color_weights 绘制热力图      
df = spark.sql("select ST_Point(longitude, latitude) as point, color_weights from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))'))")
vega = vega_heatmap(width, height, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], map_zoom_level=14.544283200495824, coordinate_system='EPSG:4326')
res = heatmap(vega, df)
save_png(res, '/tmp/heatmap.png')

spark.sql("show tables").show()
spark.catalog.dropGlobalTempView("test_table")



from arctern.util.vega import vega_icon
from arctern_pyspark import icon_viz

# df 是包含 1 列数据的 pyspark.Dataframe，该列为 WKB 类型的points
# 根据 point 数据绘制图标图
df = spark.sql("select ST_Point(longitude, latitude) as point from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))')) limit 10")
vega = vega_icon(width, height, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], icon_path='/tmp/taxi.png', coordinate_system='EPSG:4326')
res = icon_viz(vega, df)
save_png(res, '/tmp/icon_viz.png')

spark.sql("show tables").show()
spark.catalog.dropGlobalTempView("test_table")



# from arctern.util.vega import vega_pointmap
# from arctern_pyspark import pointmap

# # df 是包含 1 列数据的 pyspark.Dataframe, 该列为 WKB 类型的points
# # 绘制点大小为10，点颜色为#37A2DA，点不透明度为1.0的点图
# df = spark.sql("SELECT ST_Point (longitude, latitude) AS point FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-74.01398981737215 40.71353244267465, -74.01398981737215 40.74480271529791, -73.96979949831308 40.74480271529791, -73.96979949831308 40.71353244267465, -74.01398981737215 40.71353244267465))'))) LIMIT 10000")
# vega = vega_pointmap(width, height, bounding_box=[-74.01398981737215,40.71353244267465,-73.96979949831308,40.74480271529791], point_size=10, point_color="#37A2DA", opacity=1.0, coordinate_system="EPSG:4326")
# res = pointmap(vega, df)
# save_png(res, '/tmp/pointmap.png')

# spark.sql("show tables").show()
# spark.catalog.dropGlobalTempView("test_table")



# from arctern.util.vega import vega_weighted_pointmap
# from arctern_pyspark import weighted_pointmap

# # df1 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点颜色的权重数据
# # 绘制带权点图，点的颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化，点的大小为 16
# df1 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 20000")
# vega1 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[16], opacity=1.0, coordinate_system="EPSG:4326")
# res1 = weighted_pointmap(vega1, df1)
# save_png(res1, '/tmp/weighted_pointmap_1_0.png')

# # df2 是包含 2 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点大小的权重数据
# # 绘制带权点图，点的颜色为'#37A2DA'，点的大小根据 size_weights 在 15 ~ 50 之间变化
# df2 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, size_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
# vega2 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#37A2DA"], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
# res2 = weighted_pointmap(vega2, df2)
# save_png(res2, '/tmp/weighted_pointmap_0_1.png')

# # df3 是包含 3 列数据的 pyspark.Dataframe，第一列为 WKB 类型的points，第二列为点颜色的权重数据，第三列为点大小的权重数据
# # 绘制带权点图，点的颜色根据 color_weights 在 "#115f9a" ~ "#d0f400" 之间变化，点的大小根据 size_weights 在 15 ~ 50 之间变化
# df3 = spark.sql("SELECT ST_Point (longitude, latitude) AS point, color_weights, size_weights FROM test_table WHERE (ST_Within (ST_Point (longitude, latitude), ST_GeomFromText('POLYGON ((-73.99668712186558 40.72972339069935, -73.99668712186558 40.7345193345495, -73.99045479584949 40.7345193345495, -73.99045479584949 40.72972339069935, -73.99668712186558 40.72972339069935))'))) LIMIT 2000")
# vega3 = vega_weighted_pointmap(width, height, bounding_box=[-73.99668712186558,40.72972339069935,-73.99045479584949,40.7345193345495], color_gradient=["#115f9a", "#d0f400"], color_bound=[2.5,15], size_bound=[15, 50], opacity=1.0, coordinate_system="EPSG:4326")
# res3 = weighted_pointmap(vega3, df3)
# save_png(res3, '/tmp/weighted_pointmap_1_1.png')

# spark.sql("show tables").show()
# spark.catalog.dropGlobalTempView("test_table")
