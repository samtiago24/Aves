import pandas as pd
import requests
import os
import time  # Rate limit

def download_inat_from_csv(csv_path, output_dir='JacanaCsv', max_images=500):
    df = pd.read_csv(csv_path)
    urls = df['image_url'].dropna().str.replace('medium', 'original').unique()[:max_images]
    os.makedirs(output_dir, exist_ok=True)
    
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                fname = f"Jacana_{i:03d}.jpg"
                with open(os.path.join(output_dir, fname), 'wb') as f:
                    f.write(resp.content)
                print(f"✓ {i+1}/{len(urls)}: {fname}")
            time.sleep(0.1)  # Respeta límites
        except Exception as e:
            print(f"✗ {i+1}: {e}")
    
    print(f"¡{len(os.listdir(output_dir))} fotos en {output_dir}!")

if __name__ == "__main__":
    csv_path = r"Jacana.csv"  # Sin ruta completa, mismo folder
    download_inat_from_csv(csv_path, max_images=500)  # ¡Cambiado a 500!
