import json
import os
import subprocess

# Pacote que você deseja instalar
pacote = ["mediapipe-model-maker", "keras<3.0.0", "tensorflow"]

# Comando para instalar o pacote usando pip
comando = ["pip", "install"] + pacote

# Executar o comando usando subprocess
try:
    subprocess.check_call(comando)
    print(f"{pacote} instalado com sucesso!")
except subprocess.CalledProcessError:
    print(
        f"Não foi possível instalar {pacote}. Fudeu")


import tensorflow as tf
from mediapipe_model_maker import object_detector
assert tf.__version__.startswith('2')



train_dataset_path = "./train"
validation_dataset_path = "./valid"

with open(os.path.join(train_dataset_path, "labels.json"), "r") as f:
    labels_json = json.load(f)
for category_item in labels_json["categories"]:
    print(f"{category_item['id']}: {category_item['name']}")

train_data = object_detector.Dataset.from_coco_folder(
    train_dataset_path, cache_dir="/tmp/od_data/train")
validation_data = object_detector.Dataset.from_coco_folder(
    validation_dataset_path, cache_dir="/tmp/od_data/validation")
print("train_data size: ", train_data.size)
print("validation_data size: ", validation_data.size)

spec = object_detector.SupportedModels.MOBILENET_MULTI_AVG
hparams = object_detector.HParams(export_dir='exported_model')
options = object_detector.ObjectDetectorOptions(
    supported_model=spec,
    hparams=hparams
)

model = object_detector.ObjectDetector.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options)


loss, coco_metrics = model.evaluate(validation_data, batch_size=4)
print(f"Validation loss: {loss}")
print(f"Validation coco metrics: {coco_metrics}")

model.export_model()
