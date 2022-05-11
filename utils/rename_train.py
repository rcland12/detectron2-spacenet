import os

files = [i for i in os.listdir("AOI_1_Rio_Train") if ".tif" in i]
for file in files:
    file_num = file.split("img")[1]
    os.system(f"mv AOI_1_Rio_Train/3band_AOI_1_RIO_img{file_num} AOI_1_Rio_Train/RGB-PanSharpen/RGB-PanSharpen_AOI_1_Rio_img{file_num}")
