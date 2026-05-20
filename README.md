# 🦜 Aves — Dataset de Imágenes para Clasificación de Especies

Repositorio de construcción de dataset de imágenes de aves, orientado al entrenamiento de modelos de clasificación con aprendizaje profundo. Las imágenes son obtenidas desde iNaturalist vía CSV, y luego procesadas con **YOLOv8** para detectar y recortar únicamente al ave de cada fotografía.

---

## 📁 Estructura del Repositorio

```
Aves/
├── procesar_aves.py              # Script para descargar imágenes desde CSV de iNaturalist
├── recortar.py                   # Script para detectar y recortar aves con YOLOv8
├── yolov8n.pt                    # Modelo YOLOv8 nano preentrenado (COCO)
├── Avefría teroCSV/              # Carpeta de especie: Avefría tero
├── Baltimore Oriole/             # Carpeta de especie: Baltimore Oriole
├── Bienteveo Común/              # Carpeta de especie: Bienteveo Común
├── Canario conorado/             # Carpeta de especie: Canario coronado
├── Colibrí Cola Canela/          # Carpeta de especie: Colibrí Cola Canela
├── Fiofío Silbón/                # Carpeta de especie: Fiofío Silbón
├── Garza dedos dorados/          # Carpeta de especie: Garza dedos dorados
├── Jacana/                       # Carpeta de especie: Jacana
├── Luis Pico Grueso/             # Carpeta de especie: Luis Pico Grueso
├── Papamoscas rayado chico/      # Carpeta de especie: Papamoscas rayado chico
├── Saltador Gris/                # Carpeta de especie: Saltador Gris
├── Saltador garganta ocre/       # Carpeta de especie: Saltador garganta ocre
├── Tangara Azulgrís/             # Carpeta de especie: Tangara Azulgrís
├── Torcaza Colorada/             # Carpeta de especie: Torcaza Colorada
├── Vireo Ojos Rojos/             # Carpeta de especie: Vireo Ojos Rojos
└── Zorzal sabia/                 # Carpeta de especie: Zorzal sabia (Zorzal Savia)
```

Cada carpeta de especie contiene las imágenes ya recortadas y normalizadas a **224×224 px**, listas para ser usadas como dataset de entrenamiento.

---

## ⚙️ Requisitos

Antes de ejecutar cualquier script, instala las dependencias necesarias:

```bash
pip install pandas requests ultralytics Pillow numpy
```

| Librería       | Uso                                                   |
|----------------|-------------------------------------------------------|
| `pandas`       | Lectura de archivos CSV de iNaturalist                |
| `requests`     | Descarga de imágenes desde URLs                       |
| `ultralytics`  | Modelo YOLOv8 para detección de aves                  |
| `Pillow`       | Manipulación y recorte de imágenes                    |
| `numpy`        | Operaciones sobre bounding boxes                      |

> **Python recomendado:** 3.9 o superior.

---

## 🔄 Flujo de Trabajo

El proceso para construir el dataset de cada especie sigue dos pasos:

```
[CSV de iNaturalist]
        │
        ▼
 procesar_aves.py          ← Descarga imágenes originales
        │
        ▼
[Carpeta con imágenes crudas]
        │
        ▼
   recortar.py             ← Detecta y recorta el ave con YOLOv8
        │
        ▼
[Carpeta *_recortado/ con imágenes 224×224 px]
```

---

## 📥 Paso 1: Descargar Imágenes (`procesar_aves.py`)

Este script lee un archivo CSV exportado desde [iNaturalist](https://www.inaturalist.org/) y descarga las imágenes en resolución original.

### Configuración

Abre `procesar_aves.py` y ajusta los parámetros al inicio de la función:

```python
download_inat_from_csv(
    csv_path='Jacana.csv',    # Ruta al CSV de iNaturalist
    output_dir='JacanaCsv',   # Carpeta de salida para las imágenes
    max_images=500            # Número máximo de imágenes a descargar
)
```

### Ejecución

```bash
python procesar_aves.py
```

### ¿Qué hace internamente?

1. Carga el CSV con `pandas` y extrae la columna `image_url`.
2. Reemplaza la resolución `medium` por `original` en cada URL.
3. Descarga hasta `max_images` imágenes únicas con `requests`.
4. Guarda cada imagen como `NombreEspecie_001.jpg`, `NombreEspecie_002.jpg`, etc.
5. Respeta un delay de 100 ms entre peticiones para no sobrecargar la API de iNaturalist.

### Salida esperada

```
✓ 1/500: Jacana_000.jpg
✓ 2/500: Jacana_001.jpg
...
¡487 fotos en JacanaCsv!
```

> **Nota:** El CSV debe provenir de iNaturalist y contener la columna `image_url`. Puedes exportarlo desde la sección *Exportar* de cualquier observación o lista de especies en iNaturalist.

---

## ✂️ Paso 2: Detectar y Recortar Aves (`recortar.py`)

Este script usa el modelo **YOLOv8 nano** (`yolov8n.pt`) para detectar la clase `bird` (clase 14 de COCO) en cada imagen descargada, y recorta únicamente el área del ave con un margen del 20%.

### Configuración

Al final de `recortar.py`, ajusta las rutas:

```python
input_folder = "JacanaCsv"        # Carpeta con imágenes crudas (salida del Paso 1)
crop_birds_ultralytics(
    input_dir=input_folder,
    output_dir='Jacana_recortado', # Carpeta de salida con recortes
    conf=0.3                       # Umbral de confianza de detección (0.0 - 1.0)
)
```

### Ejecución

```bash
python recortar.py
```

### ¿Qué hace internamente?

1. Carga el modelo YOLOv8 nano desde `yolov8n.pt`.
2. Por cada imagen `.jpg`, `.jpeg` o `.png` en la carpeta de entrada:
   - Ejecuta inferencia con el umbral de confianza dado.
   - Filtra únicamente detecciones de clase **14 (bird)**.
   - Selecciona el bounding box con mayor score de confianza.
   - Aplica un **padding del 20%** alrededor del recuadro para no cortar el ave.
   - Recorta y redimensiona a **224×224 px**.
   - Convierte la imagen a RGB (compatible con PNG con transparencia).
   - Guarda el resultado como `NombreEspecie_0001_original.jpg`.
3. Imprime estadísticas por imagen (score, tamaño del bbox).

### Salida esperada

```
✓ Jacana_000.jpg: score=0.87, size=312x289px
✓ Jacana_001.jpg: score=0.74, size=198x201px
✗ Jacana_002.jpg: No birds (classes: [0, 2])
...
¡423 Jacana guardados en Jacana_recortado!
```

> **Tip:** Si obtienes muchos `✗ No birds`, intenta bajar el umbral `conf` a `0.2`. Si obtienes recortes erróneos, súbelo a `0.5` o más.

---

## 🐦 Especies del Dataset

El repositorio contiene imágenes para **16 especies** de aves:

| Nombre común               | Nombre científico (referencia)        |
|----------------------------|---------------------------------------|
| Avefría tero               | *Vanellus chilensis*                  |
| Baltimore Oriole           | *Icterus galbula*                     |
| Bienteveo Común            | *Pitangus sulphuratus*                |
| Canario coronado           | *Sicalis flaveola*                    |
| Colibrí Cola Canela        | *Amazilia tzacatl*                    |
| Fiofío Silbón              | *Elaenia albiceps*                    |
| Garza dedos dorados        | *Egretta thula / Bubulcus ibis*       |
| Jacana                     | *Jacana jacana*                       |
| Luis Pico Grueso           | *Megarynchus pitangua*                |
| Papamoscas rayado chico    | *Myioborus miniatus*                  |
| Saltador Gris              | *Saltator coerulescens*               |
| Saltador garganta ocre     | *Saltator aurantiirostris*            |
| Tangara Azulgrís           | *Thraupis episcopus*                  |
| Torcaza Colorada           | *Patagioenas cayennensis*             |
| Vireo Ojos Rojos           | *Vireo olivaceus*                     |
| Zorzal sabia               | *Turdus amaurochalinus*               |

---

## 🧠 Uso del Dataset para Entrenamiento

Una vez generadas las imágenes procesadas para cada especie, el dataset puede ser usado directamente en frameworks de deep learning:

### Con PyTorch / torchvision

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(root='Aves/', transform=transform)
loader  = DataLoader(dataset, batch_size=32, shuffle=True)
```

### Con TensorFlow / Keras

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train = datagen.flow_from_directory(
    'Aves/',
    target_size=(224, 224),
    batch_size=32,
    subset='training'
)
```

> La estructura de carpetas por especie es compatible con `ImageFolder` (PyTorch) y `flow_from_directory` (Keras) de forma nativa.

---

## 🛠️ Adaptar los Scripts a Otra Especie

Para agregar una nueva especie al dataset, sigue estos pasos:

1. **Exporta el CSV** de la especie desde iNaturalist.
2. En `procesar_aves.py`, cambia:
   ```python
   csv_path   = 'NuevaEspecie.csv'
   output_dir = 'NuevaEspecieCsv'
   ```
3. Ejecuta `procesar_aves.py`.
4. En `recortar.py`, cambia:
   ```python
   input_folder = 'NuevaEspecieCsv'
   output_dir   = 'NuevaEspecie_recortado'
   ```
5. Ejecuta `recortar.py`.
6. Mueve la carpeta `NuevaEspecie_recortado/` a la carpeta raíz del repositorio con el nombre de la especie.

---

## 📌 Notas Importantes

- El modelo `yolov8n.pt` detecta aves como **clase 14** del dataset COCO. Está incluido directamente en el repositorio (~6.5 MB).
- Las imágenes finales son guardadas en **JPEG con calidad 95**, formato estándar para datasets de visión por computadora.
- Si una imagen no contiene un ave detectable, es **descartada automáticamente** y no se incluye en la carpeta de salida.
- El script respeta los límites de la API de iNaturalist con un delay entre descargas (`time.sleep(0.1)`).

---

## 📄 Licencia

Este repositorio es de uso académico e investigativo. Las imágenes provienen de iNaturalist y están sujetas a las licencias Creative Commons de cada observación. Consulta los términos de uso de [iNaturalist](https://www.inaturalist.org/pages/terms) antes de distribuir el dataset.
