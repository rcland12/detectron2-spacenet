# Example by Russell Land, Justin Hall, and Michael Fox
# https://github.com/rl02898/detectron2-spacenet
# Imports
import os
import json
import yaml
import torch
import random
import cv2 as cv
import detectron2
import numpy as np

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.structures import BoxMode
from detectron2.engine import DefaultTrainer
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import ColorMode
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog


# Dataset registration function
def get_dataset_dicts(img_dir):
    json_file = os.path.join(img_dir, "via_region_data.json")
    with open(json_file) as f:
        imgs_anns = json.load(f)
    
    dataset_dicts = []
    for idx, annots in enumerate(imgs_anns.values()):
        record = {}
        
        filename = os.path.join(img_dir, annots["filename"])
        height, width = cv.imread(filename).shape[:2]
        
        record["file_name"] = filename
        record["image_id"] = idx
        record["height"] = height
        record["width"] = width
      
        annotations = annots["regions"]
        objs = []
        for _, anno in annotations.items():
            assert not anno["region_attributes"]
            anno = anno["shape_attributes"]
            px = anno["all_points_x"]
            py = anno["all_points_y"]
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]
            obj = {"bbox": [np.min(px),
                            np.min(py),
                            np.max(px),
                            np.max(py)
                           ],
                   "bbox_mode": BoxMode.XYXY_ABS,
                   "segmentation": [poly],
                   "category_id": anno["category"]
                  }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
    return dataset_dicts


# Register your dataset
classes = ["building"]
colors = [(249, 180, 45)]

for d in ["train", "val"]:
    DatasetCatalog.register(d, lambda d=d: get_dataset_dicts(os.path.join("Spacenet", d)))
    MetadataCatalog.get(d).thing_classes = classes
    MetadataCatalog.get(d).thing_colors = colors
metadata = MetadataCatalog.get("train")


# Create configurations
# Initialize configs
cfg = get_cfg()
# Load in pre-built model from Detectron2.MODEL_ZOO
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("train",)
cfg.DATALOADER.NUM_WORKERS = 4
# Start with pre-trained model, usually performs better
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")
# Images per batch
cfg.SOLVER.IMS_PER_BATCH = 16
# Starting learning rate
cfg.SOLVER.BASE_LR = 0.0005
# Batch size per image
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 32
# Define number of classes (1 for "building")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(classes)
# Where your results are stored
cfg.OUTPUT_DIR = "Spacenet/output"

# Save your configurations for multi-GPU use
with open("Spacenet/SpacenetD2cfg.yaml", "w") as file:
    yaml.dump(cfg, file)


# Train your model
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()