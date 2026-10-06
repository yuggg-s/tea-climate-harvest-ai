from ultralytics import YOLO

def train():
    model = YOLO("yolov8n.pt")   # 加载 COCO 预训练权重，再在茶芽数据集上微调
    # 数据集配置文件路径
    results = model.train(
        data="datasets/data.yaml",
        epochs=100,
        imgsz=640,
        batch=8,
        name="tea_bud_train"
    )
    return results

if __name__ == "__main__":
    train()