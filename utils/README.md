# utils 工具模块目录
存放项目业务逻辑工具脚本

## 文件清单
- weather.py：气象积温计算模块
    读取气象CSV文件，读取 temp_avg（日平均气温），计算生长积温总和。

## CSV文件要求
CSV表头必须包含：
`date,temp_avg,temp_max,temp_min,humidity`

## 函数说明

```python
def calc_accum_temp(df, base_temp=10.0):
    """
    输入 pandas 读取后的 CSV 数据表，返回累计有效积温（°C·d）。
    
    茶树芽头萌动起点温度约 10°C，低于此温度不计入有效积温。
    有效积温 = Σ max(0, 日均温 - 10)
    """