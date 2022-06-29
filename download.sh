#!/bin/bash

mkdir Spacenet
cd Spacenet



# Rio de Janeiro
# Download training data, organize into directories, and rename the files.
aws s3 cp s3://spacenet-dataset/spacenet/SN1_buildings/tarballs/SN1_buildings_train_AOI_1_Rio_3band.tar.gz .
tar -xvzf SN1_buildings_train_AOI_1_Rio_3band.tar.gz
rm SN1_buildings_train_AOI_1_Rio_3band.tar.gz
mv 3band AOI_1_Rio_Train
cd AOI_1_Rio_Train
mkdir RGB-PanSharpen
cd ..

# Download testing data, organize into directories, and rename the files.
aws s3 cp s3://spacenet-dataset/spacenet/SN1_buildings/tarballs/SN1_buildings_test_AOI_1_Rio_3band.tar.gz .
tar -xvzf SN1_buildings_test_AOI_1_Rio_3band.tar.gz
rm SN1_buildings_test_AOI_1_Rio_3band.tar.gz
mv 3band AOI_1_Rio_Test_public
cd AOI_1_Rio_Test_public
mkdir RGB-PanSharpen
cd ..
python ../utils/rename.py

# Download geojson files and organize them into a directory.
aws s3 cp s3://spacenet-dataset/spacenet/SN1_buildings/tarballs/SN1_buildings_train_AOI_1_Rio_geojson_buildings.tar.gz .
tar -xvzf SN1_buildings_train_AOI_1_Rio_geojson_buildings.tar.gz
rm SN1_buildings_train_AOI_1_Rio_geojson_buildings.tar.gz
mv geojson AOI_1_Rio_Train
echo "Done downloading and organzing Rio de Janeiro dataset (1 of 5)"



# Download Las Vegas training and testing data and organize into directories.
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/SN2_buildings_train_AOI_2_Vegas.tar.gz .
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/AOI_2_Vegas_Test_public.tar.gz .

tar -xvzf SN2_buildings_train_AOI_2_Vegas.tar.gz
rm SN2_buildings_train_AOI_2_Vegas.tar.gz
tar -xvzf AOI_2_Vegas_Test_public.tar.gz
rm AOI_2_Vegas_Test_public.tar.gz

cd AOI_2_Vegas_Train
rm -rf MUL MUL-PanSharpen PAN geojson
cd ..

cd AOI_2_Vegas_Test_public
rm -rf MUL MUL-PanSharpen PAN
cd ..
echo "Done downloading and organzing Las Vegas dataset (2 of 5)"



# Download Paris training and testing data and organize into directories.
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/SN2_buildings_train_AOI_3_Paris.tar.gz .
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/AOI_3_Paris_Test_public.tar.gz .

tar -xvzf SN2_buildings_train_AOI_3_Paris.tar.gz
rm SN2_buildings_train_AOI_3_Paris.tar.gz
tar -xvzf AOI_3_Paris_Test_public.tar.gz
rm AOI_3_Paris_Test_public.tar.gz

cd AOI_3_Paris_Train
rm -rf MUL MUL-PanSharpen PAN geojson
cd ..

cd AOI_3_Paris_Test_public
rm -rf MUL MUL-PanSharpen PAN
cd ..
echo "Done downloading and organzing Paris dataset (3 of 5)"



# Download Shanghai training and testing data and organize into directories.
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/SN2_buildings_train_AOI_4_Shanghai.tar.gz .
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/AOI_4_Shanghai_Test_public.tar.gz .

tar -xvzf SN2_buildings_train_AOI_4_Shanghai.tar.gz
rm SN2_buildings_train_AOI_4_Shanghai.tar.gz
tar -xvzf AOI_4_Shanghai_Test_public.tar.gz
rm AOI_4_Shanghai_Test_public.tar.gz

cd AOI_4_Shanghai_Train
rm -rf MUL MUL-PanSharpen PAN geojson
cd ..

cd AOI_4_Shanghai_Test_public
rm -rf MUL MUL-PanSharpen PAN
cd ..
echo "Done downloading and organzing Shanghai dataset (4 of 5)"



# Download Khartoum training and testing data and organize into directories.
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/SN2_buildings_train_AOI_5_Khartoum.tar.gz .
aws s3 cp s3://spacenet-dataset/spacenet/SN2_buildings/tarballs/AOI_5_Khartoum_Test_public.tar.gz .

tar -xvzf SN2_buildings_train_AOI_5_Khartoum.tar.gz
rm SN2_buildings_train_AOI_5_Khartoum.tar.gz
tar -xvzf AOI_5_Khartoum_Test_public.tar.gz
rm AOI_5_Khartoum_Test_public.tar.gz

cd AOI_5_Khartoum_Train
rm -rf MUL MUL-PanSharpen PAN geojson
cd ..

cd AOI_5_Khartoum_Test_public
rm -rf MUL MUL-PanSharpen PAN
cd ..
echo "Done downloading and organzing Khartoum dataset (5 of 5)"



mkdir train val test

cd ..