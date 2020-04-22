# vega 接口

<font size="5">**vega_pointmap**</font><br /> 

**arctern.util.vega.vega_pointmap(width,height,bounding_box,point_size,point_color,opacity,coordinate_system)**

&#x2002; &#x2003; 根据给定的配置参数，构建描述渲染样式的 VegaPointMap 对象。

&#x2002; &#x2003; 参数

&#x2002; &#x2003; &#x2002; &#x2003; * width(int) -- 图片宽度，单位为像素个数
&#x2002; &#x2003; &#x2002; &#x2003; * height(int) -- 图片高度，单位为像素个数
&#x2002; &#x2003; &#x2002; &#x2003; * bounding_box(list) -- 图片对应的地理坐标区域，以 [x_min, y_min, x_max, y_max] 的形式表示一个矩形区域。图片左下角的像素坐标 (0, 0) 对应实际地理坐标 (x_min, y_min) ，图片右上角的像素坐标 (width, height) 对应实际地理坐标 (x_max, y_max)
&#x2002; &#x2003; &#x2002; &#x2003; * point_size(int) -- 可选参数，表示点的直径，默认值为 3
&#x2002; &#x2003; &#x2002; &#x2003; * point_color(str) -- 可选参数，表示点的颜色，使用十六进制的颜色(hex color)表示，默认值为"#115f9a"
&#x2002; &#x2003; &#x2002; &#x2003; * opacity(float) -- 可选参数，表示点的不透明度，范围为 0.0 ~ 1.0，默认值为 1.0
&#x2002; &#x2003; &#x2002; &#x2003; * coordinate_system(str) -- 可选参数，表示输入数据所属的地理坐标系统，默认值为"EPSG:3857"，当前支持的地理坐标系统请参照 <https://spatialreference.org/>

&#x2002; &#x2003; 返回值

&#x2002; &#x2003; &#x2002; &#x2003; 用于描述渲染样式的 VegaPointMap 对象。


&#x2002; &#x2003; 返回值类型
   
&#x2002; &#x2003; &#x2002; &#x2003; arctern.util.vega.pointmap.vega_pointmap.VegaPointMap


&#x2002; &#x2003; 示例:

  ```python
      >>> # 绘制宽为1024，高为896，点直径为3的，点颜色为蓝色的完全不透明点图
      >>> vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-8237467.21, 4972643.32, -8232560.36, 4980065.63])
      >>> 
      >>> # 绘制宽为1024，高为896，点直径为10的，点颜色为红色的半透明点图
      >>> vega = arctern.util.vega.vega_pointmap(1024, 896, bounding_box=[-73.998427, 40.730309, -73.954348, 40.780816], point_size=10, point_color="#FF0000", opacity=0.5, coordinate_system="EPSG:4326")
   ```
