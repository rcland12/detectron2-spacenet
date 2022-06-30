import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from osgeo import gdal


def grab_certain_file(file_ext, folder_path):
    """This creates a list of file names for all files within the :param:`folderpath` folder 
    if the file name contains the :param:`file_type` string

    :param file_ext: Type of file that should be included in the list of files
    :type file_ext: str

    :param folder_path: File path to the folder containing files that will be checked for inclusion in the list.
    Ex: ".png"
    :type folder_path: str

    :raises TypeError: Raised when a function or operation is applied to an object of an incorrect type.
    :raises ValueError: Raised when a function gets an argument of correct type but improper value.
    :raises FileNotFound: No such file or directory.

    :return: Sorted List containing the names of the files within the indicated folder that contain the :param:`file_ext` string
    :rtype: List
    """
    try:
        if file_ext == "":
            file_list = sorted([i for i in os.listdir(folder_path) if "." not in i])
        else:
            file_list = sorted([i for i in os.listdir(folder_path) if i.split(".")[-1] == file_ext or "." + i.split(".")[-1] == file_ext])
    
    except FileNotFoundError as e:
        print("Error raised: ", e)
        file_list = []

    return file_list

def normalize_array(array):
    """Normalizes an array of values from [0, 1]

    :param array: A numpy array of values to be normalized
    :type array: numpy.array


    :raises TypeError: Raised when a function or operation is applied to an object of an incorrect type.
    :raises ValueError: Raised when a function gets an argument of correct type but improper value.

    :return: Returns a numpy array  of values normalized to the range [0, 1]
    :rtype: numpy.array

    .. note:: An empty numpy array will return an empty numpy array while an array full of the same values 
    will return an array of identical size full of zeroes
    """
    try:
        if len(array) == 0:
            norm_array = []
        else:
            norm_array = array.astype(float)
            mat_min, mat_max = np.amin(norm_array), np.amax(norm_array)
            if mat_min != mat_max:
                for i in range(len(norm_array)):
                    norm_array[i] = (norm_array[i] - mat_min) / (mat_max - mat_min)
            elif  mat_min == mat_max == 0:
                norm_array = array.astype(float)
            else:
                for i in range(len(norm_array)):
                    norm_array[i] = (norm_array[i] - mat_min) / (mat_min)        
    
    except ValueError as e:
        print("Error encountered: ", e)
        norm_array = array
    
    return norm_array

def tif_to_png(files, path_to_files, dst, normalize=False):
    """Converts a list of tiff images into png images before saving them at a specified location 

    :param files: List of the names of the tiff images to be converted
    :type files: List

    :param path_to_files: File path of the tiff images
    :type path_to_files: str

    :param dst: File path that the converted images will be saved to
    :type dst: str

    :param normalize: Indicates whether the tiff image must be normalized, defaults to False
    :type normalize: bool

    :raises FileNotFound: No such file or directory.

    :return: Returns nothing, saves the converted png images at the indicated place
    :rtype: None
    
    """

    for item in tqdm(files, desc = f"Converting TIF images to PNG to {dst}", ncols=150, bar_format="{l_bar}{bar:10}{r_bar}"):
        file_path = os.path.join(path_to_files, item)
        dst_path = os.path.join(dst, item.replace(".tif", ".png"))
        image = gdal.Open(file_path)

        band1 = image.GetRasterBand(1)
        band2 = image.GetRasterBand(2)
        band3 = image.GetRasterBand(3)

        array1 = band1.ReadAsArray()
        array2 = band2.ReadAsArray()
        array3 = band3.ReadAsArray()

        if normalize:
            array1 = normalize_array(array1)
            array2 = normalize_array(array2)
            array3 = normalize_array(array3)

        image = np.dstack((array1, array2, array3))
        plt.imsave(dst_path, image)


def detectron_json(files, path_to_files, csv, num_dataset, train_val):
    """Creates JSON files for Detectron2 from SpaceNet images and their associated csv annotations

    :param files: List of file names that are represented by the SpaceNet csv file
    :type files: List

    :param path_to_files: File path to where the images represented by the SpaceNet csv file are
    :type path_to_files: str

    :param csv: Spacenet annotation csv that has been read into a pandas dataframe
    :type csv: pandas dataframe

    :param num_dataset: Number indicating which SpaceNet dataset the data belongs to. This should be represented in the image names as well
    :type num_dataset: int

    :param train_val: String indicating whether the images being converted are training or validation images
    :type train_val: str

    :raises TypeError: Raised when a function or operation is applied to an object of an incorrect type.
    :raises ValueError: Raised when a function gets an argument of correct type but improper value.
    :raises FileNotFound: No such file or directory.

    :return: Returns nothing, creates a JSON file within the folder the SpaceNet images are located
    :rtype: None
    
    """
    files_dict = {}

    for file in tqdm(files, desc=f"Creating JSONs for Detectron2 on {num_dataset}_{train_val}", ncols=150, bar_format="{l_bar}{bar:10}{r_bar}", position=0, leave=True):
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
                                    "all_points_y": all_points_y,
                                    "category": 0
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

    with open(f"Spacenet/{train_val}/AOI_{num_dataset}_region_data.json", "w") as f:
        json.dump(files_dict, f)