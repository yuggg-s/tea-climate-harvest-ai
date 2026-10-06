# datasets 数据集目录
YOLOv8目标检测训练数据集配置目录，用于训练识别「一芽一叶 tea_bud」

## 目录结构
- data.yaml：YOLO训练配置文件，定义数据集类别、路径参数


## 数据信息
- 类别：0: tea_bud（一芽一叶）
- 数据来源：Roboflow Universe 公开数据集 teaRob（1733张茶园实景图像，CC BY 4.0许可），后续可补充梅家坞本地实拍图像
- 标注工具：LabelImg，输出YOLO格式txt标注

> 仓库说明：
> 原始训练图片与标签文件体积较大，**本仓库不存放图片与标签原图**，仅保留训练配置文件 data.yaml。
> 模型权重 best.pt 已经由团队提前训练完成，存放于 `models/` 文件夹。

## 训练命令
```python
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
results = model.train(data="datasets/data.yaml", epochs=50， imgsz=640, batch=8)