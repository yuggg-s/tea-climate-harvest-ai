import gradio as gr
from ultralytics import YOLO
import pandas as pd
from utils.weather import calc_accum_temp
import os
import cv2
import numpy as np

# 权重降级逻辑
model_path = "models/best.pt"
if os.path.exists(model_path):
    model = YOLO(model_path)
    print(f"已加载自定义模型：{model_path}")
else:
    print("未找到自定义训练权重，自动加载yolov8n预训练模型用于演示（无法识别茶芽）")
    model = YOLO("yolov8n.pt")

def predict_image(img, csv_file):
    if img is None:
        return None, "请先上传茶园照片", "", ""
    try:
        # Gradio输入RGB → 转为BGR送入YOLO
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        result = model(img_bgr, conf=0.2)
    except Exception as e:
        return None, f"图像推理失败：{e}", "", ""
    boxes = result[0].boxes
    bud_count = len(boxes)

    # 积温计算
    acc_temp = None
    if csv_file is not None:
        try:
            df = pd.read_csv(csv_file)
            acc_temp = calc_accum_temp(df)
        except Exception as e:
            print(f"CSV读取异常：{e}")
            acc_temp = None

    # 拆分三块独立文本
    text_bud = f"检测到茶芽数量：{bud_count}"
    if acc_temp is not None:
        text_temp = f"有效积温：{acc_temp:.2f} ℃·d"
        if acc_temp < 120:
            advice = "积温不足，暂不适合采摘，继续等待。"
        elif 120 <= acc_temp <= 180:
            advice = "积温达标，适合采摘一芽一叶。"
        else:
            advice = "积温过高，芽叶偏老，尽快采摘。"
    else:
        text_temp = "未上传气象CSV，无积温数据"
        advice = "无法计算采摘窗口，请上传气象数据。"

    out_img = result[0].plot()
    # 修复颜色：BGR转RGB
    if len(out_img.shape) == 3 and out_img.shape[2] == 3:
        out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)
    # 强制转为uint8 numpy数组，解决Gradio颜色解析异常
    out_img = np.asarray(out_img, dtype=np.uint8)

    return out_img, text_bud, text_temp, advice

# ========== Blocks界面 ==========
with gr.Blocks(title="茶芽智眼 TeaEye") as demo:
    gr.Markdown("# 🍵 茶芽智眼 TeaEye")
    gr.Markdown("YOLOv8识别茶园一芽一叶 + 气象积温预测最佳采摘窗口 | AI4Climate项目")
    with gr.Row():
        img_in = gr.Image(type="numpy", label="上传茶园照片")
        csv_in = gr.File(label="上传气象csv文件", file_types=[".csv"])
    with gr.Row():
        img_out = gr.Image(label="检测结果图")
        with gr.Column():
            out_bud = gr.Textbox(label="芽头数量统计", lines=1)
            out_temp = gr.Textbox(label="有效积温", lines=1)
            out_advice = gr.Textbox(label="采摘建议", lines=2)
    btn = gr.Button("开始预测",variant="primary")
    gr.Markdown("""
> 使用提示：
> 1. 上传茶园**俯视实拍照片**，AI识别可采摘一芽一叶
> 2. 可选上传气象CSV，字段：date,temp_avg,temp_max,temp_min,humidity
""")
    btn.click(
        fn=predict_image,
        inputs=[img_in, csv_in],
        outputs=[img_out, out_bud, out_temp, out_advice]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)