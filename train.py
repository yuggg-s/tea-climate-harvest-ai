"""
YOLOv8 茶芽检测训练脚本
从上次 20 轮的断点继续训练到 50 轮
"""

from ultralytics import YOLO


def train_model():
    # 加载上次训练保存的 last.pt（注意路径多了一层 runs/detect/）
    model = YOLO("runs/detect/runs/tea_bud/yolov8n_bud/weights/last.pt")

    results = model.train(
        data="datasets/data.yaml",
        epochs=50,                   # 目标总轮次（不是再跑 50，而是跑到 50）
        imgsz=416,
        batch=8,
        device="cpu",
        workers=2,
        patience=20,
        project="runs/tea_bud",
        name="yolov8n_bud",
        resume=True,                 # 关键：断点续训
        exist_ok=True,
    )

    print(f"\n训练完成，最佳模型路径：{results.save_dir}/weights/best.pt")


if __name__ == "__main__":
    train_model()

