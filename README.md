Start here.<br>

1. Clone this repository.
    ```bash
    # HTTPS
    git clone https://github.com/rl02898/detectron2-spacenet.git
    # SSH
    git clone git@github.com:rl02898/detectron2-spacenet.git
    ```
2. Run the following command. This command will download the data, put it into directories, rename it, convert the TIFF images to PNGs, and create the JSON files for Detectron2. This will take an hour or two. You may see warnings, they are expected.
    ```bash
    ./install.sh
    ```
    with a file structure like:
    ```bash
    Spacenet/
    ├─ AOI_1_Rio_train/
    ...
    ...
    ...
    ├─ AOI_5_Khartoum_Test_public/
    ├─ train/
    │  ├─ images.png
    │  ├─ via_region_data.json
    ├─ val/
    │  ├─ images.png
    │  ├─ via_region_data.json
    ├─ test/
    │  ├─ images.png
    ```
3. Follow the steps in the Medium article on how to properly use the inference functions in demo.py:<br>
https://russland.medium.com/using-detectron2-for-instance-segmentation-on-the-spacenet-dataset-94338f739cd0
