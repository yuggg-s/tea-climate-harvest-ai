# models 文件夹
存放YOLOv8目标检测模型权重文件

## 文件说明
- best.pt：YOLOv8训练完成后的茶芽检测模型，用于识别图片中的一芽一叶（tea_bud）
- yolov8n.pt ：YOLOv8n预训练权重
## 使用说明
1. 将训练完成的 best.pt 放入本目录；
2. app.py会自动读取该权重，用于茶园图像推理；
3. 若暂无训练模型，系统自动切换使用yolov8n.pt预训练权重做原型演示。

