import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from osgeo import gdal


def grab_certain_file(file_ext, folder_path):
    return [i for i in os.listdir(folder_path) if file_ext in i]

def normalize_tiff(matrix, mat_min, mat_max):
    return (matrix - mat_min) / (mat_max - mat_min)

def tiff_to_png(files, path_to_files, dst, normalize=False):
    for item in files:
        file_path = os.path.join(path_to_files, item)
        dst_path = os.path.join(dst, item.replace(".tif", ".png"))
        dataset = gdal.Open(file_path)

        band1 = dataset.GetRasterBand(1)
        band2 = dataset.GetRasterBand(2)
        band3 = dataset.GetRasterBand(3)
        
        if normalize:
            b1 = band1.ReadAsArray()
            b1 = b1.astype(float)
            mat_min, mat_max = np.amin(b1), np.amax(b1)
            for i in range(len(b1)):
                b1[i] = normalize_tiff(b1[i], mat_min, mat_max)

            b2 = band2.ReadAsArray()
            b2 = b2.astype(float)
            mat_min, mat_max = np.amin(b2), np.amax(b2)
            for i in range(len(b2)):
                b2[i] = normalize_tiff(b2[i], mat_min, mat_max)

            b3 = band3.ReadAsArray()
            b3 = b3.astype(float)
            mat_min, mat_max = np.amin(b3), np.amax(b3)
            for i in range(len(b3)):
                b3[i] = normalize_tiff(b3[i], mat_min, mat_max)
        
        else:
            b1 = band1.ReadAsArray()
            b2 = band2.ReadAsArray()
            b3 = band3.ReadAsArray()

        image = np.dstack((b1, b2, b3))
        plt.imsave(dst_path, image)


def detectron_json(files, path_to_files, csv, num_dataset, train_val):
    files_dict = {}

    for file in files:
        file_path = os.path.join(path_to_files, file)

        # Image ID
        img_num = file.split(".")[0]
        img_id = img_num.split("img")[1]
        ImageId = f"AOI_{num_dataset}_img{img_id}"

        # Annotations
        buildings = csv[csv["ImageId"] == ImageId]["PolygonWKT_Pix"]
        regions = {}
        for i in range(len(buildings)):
            dataf = buildings.to_frame()
            row = dataf.iloc[i]
            literal = row.factorize()[1][0]

            if "EMPTY" in literal:
                regions = {}
                break
            if "),(" in literal:
                literal = literal.replace("),(", ",")

            tup = literal.split("((")[1]
            tup = tup[:-2]
            strlist = tup.split(",")
            all_points_x, all_points_y = [], []
            for j in range(len(strlist)):
                split = strlist[j].split(" ")
                all_points_x.append(round(float(split[0])))
                all_points_y.append(round(float(split[1])))
            regions[str(i)] = {"shape_attributes":
                                   {"name": "polygon",
                                    "all_points_x": all_points_x,
                                    "all_points_y": all_points_y
                                   },
                               "region_attributes": {}
                              }

        # complete dictionary
        dictionary = {"file_ref": '',
                      "size": os.path.getsize(file_path),
                      "filename": file.replace(".tif", ".png"),
                      "base64_img_data": '',
                      "file_attributes": {},
                      "regions": regions
                 }

        files_dict[file.replace(".tif", ".png")] = dictionary

    with open(f"Spacenet/{train_val}/AOI_{num_dataset}_region_data.json", "w") as fp:
        json.dump(files_dict, fp)