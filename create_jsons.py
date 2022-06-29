import os
import json
import geojson
import pandas as pd
from tqdm import tqdm
from osgeo import gdal
from sklearn.model_selection import train_test_split

# custom functions
from utils.functions import grab_certain_file, detectron_json



RANDOM_SEED = 560
rio_train = "Spacenet/AOI_1_Rio_Train/RGB-PanSharpen"
rio_geojson = "Spacenet/AOI_1_Rio_Train/geojson"
vegas_train = "Spacenet/AOI_2_Vegas_Train/RGB-PanSharpen"
paris_train = "Spacenet/AOI_3_Paris_Train/RGB-PanSharpen"
shanghai_train = "Spacenet/AOI_4_Shanghai_Train/RGB-PanSharpen"
khartoum_train = "Spacenet/AOI_5_Khartoum_Train/RGB-PanSharpen"



# Create JSONs for Detectron2
# Rio de Janeiro
# Special case, so no function
rio_images = grab_certain_file(".tif", rio_train)
train, val = train_test_split(rio_images, test_size=0.2, random_state=RANDOM_SEED)
train_dict = {}

# Training set
for file in tqdm(train, desc="Creating JSONs for Detectron2 on 1_Rio_train", ncols=150, bar_format="{l_bar}{bar:10}{r_bar}"):
    file_path = os.path.join(rio_train, file)
    img_id = file.split(".tif")[0]
    img_id = img_id.split("img")[1]
    geojson_path = os.path.join(rio_geojson, f"Geo_AOI_1_RIO_img{img_id}.geojson")
    
    with open(geojson_path) as f:
        gj = geojson.load(f)
    
    regions = {}
    num_buildings = len(gj["features"])
    if num_buildings > 0:
        gdal_image = gdal.Open(file_path)
        pixel_width, pixel_height = gdal_image.GetGeoTransform()[1], gdal_image.GetGeoTransform()[5]
        originX, originY = gdal_image.GetGeoTransform()[0], gdal_image.GetGeoTransform()[3]
        
        for i in range(num_buildings):
            points = gj["features"][i]["geometry"]["coordinates"][0]
            if len(points) == 1:
                points = points[0]
            
            all_points_x, all_points_y = [], []
            for j in range(len(points)):
                all_points_x.append(int(round((points[j][0] - originX) / pixel_width)))
                all_points_y.append(int(round((points[j][1] - originY) / pixel_height)))
            
            regions[str(i)] = {"shape_attributes":
                                   {"name": "polygon",
                                    "all_points_x": all_points_x,
                                    "all_points_y": all_points_y,
                                    "category": 0
                                   },
                               "region_attributes": {}
                              }
    
    dictionary = {"file_ref": '',
                  "size": os.path.getsize(file_path),
                  "filename": file.replace(".tif", ".png"),
                  "base64_img_data": '',
                  "file_attributes": {},
                  "regions": regions
                 }
    
    train_dict[file.replace(".tif", ".png")] = dictionary
    
with open("Spacenet/train/AOI_1_Rio_region_data.json", "w") as f:
    json.dump(train_dict, f)


# Validation set
val_dict = {}

for file in tqdm(val, desc="Creating JSONs for Detectron2 on 1_Rio_val", ncols=150, bar_format="{l_bar}{bar:10}{r_bar}"):
    file_path = os.path.join(rio_train, file)
    img_id = file.split(".tif")[0]
    img_id = img_id.split("img")[1]
    geojson_path = os.path.join(rio_geojson, f"Geo_AOI_1_RIO_img{img_id}.geojson")
    
    with open(geojson_path) as f:
        gj = geojson.load(f)
    
    regions = {}
    num_buildings = len(gj["features"])
    if num_buildings > 0:
        gdal_image = gdal.Open(file_path)
        pixel_width, pixel_height = gdal_image.GetGeoTransform()[1], gdal_image.GetGeoTransform()[5]
        originX, originY = gdal_image.GetGeoTransform()[0], gdal_image.GetGeoTransform()[3]
        
        for i in range(num_buildings):
            points = gj["features"][i]["geometry"]["coordinates"][0]
            if len(points) == 1:
                points = points[0]
            
            all_points_x, all_points_y = [], []
            for j in range(len(points)):
                all_points_x.append(int(round((points[j][0] - originX) / pixel_width)))
                all_points_y.append(int(round((points[j][1] - originY) / pixel_height)))
            
            regions[str(i)] = {"shape_attributes":
                                   {"name": "polygon",
                                    "all_points_x": all_points_x,
                                    "all_points_y": all_points_y,
                                    "category": 0
                                   },
                               "region_attributes": {}
                              }
    
    dictionary = {"file_ref": '',
                  "size": os.path.getsize(file_path),
                  "filename": file.replace(".tif", ".png"),
                  "base64_img_data": '',
                  "file_attributes": {},
                  "regions": regions
                 }
    
    val_dict[file.replace(".tif", ".png")] = dictionary

with open("Spacenet/val/AOI_1_Rio_region_data.json", "w") as f:
    json.dump(val_dict, f)



# Vegas
vegas_images = grab_certain_file(".tif", vegas_train)
train, val = train_test_split(vegas_images, test_size=0.2, random_state=RANDOM_SEED)
df = pd.read_csv("Spacenet/AOI_2_Vegas_Train/summaryData/AOI_2_Vegas_Train_Building_Solutions.csv")

detectron_json(train, vegas_train, df, "2_Vegas", "train")
detectron_json(val, vegas_train, df, "2_Vegas", "val")



# Paris
paris_images = grab_certain_file(".tif", paris_train)
train, val = train_test_split(paris_images, test_size=0.2, random_state=RANDOM_SEED)
df = pd.read_csv("Spacenet/AOI_3_Paris_Train/summaryData/AOI_3_Paris_Train_Building_Solutions.csv")

detectron_json(train, paris_train, df, "3_Paris", "train")
detectron_json(val, paris_train, df, "3_Paris", "val")



# Shanghai
shanghai_images = grab_certain_file(".tif", shanghai_train)
train, val = train_test_split(shanghai_images, test_size=0.2, random_state=RANDOM_SEED)
df = pd.read_csv("Spacenet/AOI_4_Shanghai_Train/summaryData/AOI_4_Shanghai_Train_Building_Solutions.csv")

detectron_json(train, shanghai_train, df, "4_Shanghai", "train")
detectron_json(val, shanghai_train, df, "4_Shanghai", "val")



# Khartoum
khartoum_images = grab_certain_file(".tif", khartoum_train)
train, val = train_test_split(khartoum_images, test_size=0.2, random_state=RANDOM_SEED)
df = pd.read_csv("Spacenet/AOI_5_Khartoum_Train/summaryData/AOI_5_Khartoum_Train_Building_Solutions.csv")

detectron_json(train, khartoum_train, df, "5_Khartoum", "train")
detectron_json(val, khartoum_train, df, "5_Khartoum", "val")




# Create JSON for entire training dataset
jsons = ["Spacenet/train/AOI_1_Rio_region_data.json",
         "Spacenet/train/AOI_2_Vegas_region_data.json",
         "Spacenet/train/AOI_3_Paris_region_data.json",
         "Spacenet/train/AOI_4_Shanghai_region_data.json",
         "Spacenet/train/AOI_5_Khartoum_region_data.json"
        ]

result = {}
for file in jsons:
    with open(file, "r") as f:
        loaded = json.load(f)
    for key, value in loaded.items():
        result[key] = value

with open("Spacenet/train/via_region_data.json", "w") as file:
    json.dump(result, file)



# Create JSON for entire validation dataset
jsons = ["Spacenet/val/AOI_1_Rio_region_data.json",
         "Spacenet/val/AOI_2_Vegas_region_data.json",
         "Spacenet/val/AOI_3_Paris_region_data.json",
         "Spacenet/val/AOI_4_Shanghai_region_data.json",
         "Spacenet/val/AOI_5_Khartoum_region_data.json"
        ]

result = {}
for file in jsons:
    with open(file, "r") as f:
        loaded = json.load(f)
    for key, value in loaded.items():
        result[key] = value

with open("Spacenet/val/via_region_data.json", "w") as file:
    json.dump(result, file)

print("Done creating JSONs")