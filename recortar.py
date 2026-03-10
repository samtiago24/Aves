from ultralytics import YOLO
from PIL import Image
import os
import numpy as np


def crop_birds_ultralytics(input_dir, output_dir='Capuchino_Tricolor_Recortado', conf=0.3):
    input_path = os.path.abspath(input_dir)
    if not os.path.exists(input_path):
        print(f"❌ Carpeta no encontrada: {input_path}")
        print("Carpetas aquí:", [d for d in os.listdir('.') if os.path.isdir(d)])
        return

    model = YOLO('yolov8n.pt')
    os.makedirs(output_dir, exist_ok=True)

    processed = 0
    for fname in os.listdir(input_path):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_path, fname)
            results = model(img_path, conf=conf, verbose=False)

            boxes_data = results[0].boxes
            if boxes_data is None or len(boxes_data) == 0:
                print(f"✗ {fname}: Sin objetos")
                continue

            boxes = boxes_data.xyxy.cpu().numpy()
            classes = boxes_data.cls.cpu().numpy()
            scores = boxes_data.conf.cpu().numpy()

            bird_mask = classes == 14
            if not np.any(bird_mask):
                print(f"✗ {fname}: No birds (classes: {classes.astype(int).tolist()})")
                continue

            bird_scores = scores[bird_mask]
            bird_idx = int(np.argmax(bird_scores))
            global_idx = int(np.where(bird_mask)[0][bird_idx])

            x1, y1, x2, y2 = boxes[global_idx]
            img = Image.open(img_path)

            w, h = x2 - x1, y2 - y1
            pad_w, pad_h = w * 0.2, h * 0.2
            crop_box = (
                max(0, x1 - pad_w),
                max(0, y1 - pad_h),
                min(img.width, x2 + pad_w),
                min(img.height, y2 + pad_h)
            )

            cropped = img.crop(crop_box).resize((512, 512))
            cropped = cropped.convert('RGB')  # ← Fix RGBA/PNG transparencia
            out_name = f"Capuchino_Tricolor_{processed:04d}_{fname.split('.')[0]}.jpg"
            cropped.save(os.path.join(output_dir, out_name), quality=95)
            print(f"✓ {fname}: score={bird_scores[bird_idx]:.2f}, size={w:.0f}x{h:.0f}px")
            processed += 1

    print(f"¡{processed} saltadores guardados en {output_dir}!")


# Uso
input_folder = "Capuchino_TricolorCsv"
crop_birds_ultralytics(input_folder)
