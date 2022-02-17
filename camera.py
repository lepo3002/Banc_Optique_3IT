from __future__ import annotations
from vimba import *
import numpy as np
import datetime
from time import time
from typing import Optional, Union
from pathlib import Path
import tifffile
from tifffile import TIFF
import json
import cv2


# Custom tag number to store JSON data
# Must be above 32768
custom_tag = 36000

GLOBAL_PICTURE_DATA_DICT = {
    # "experiment_name": "My experiment",
    # "datetime": datetime.now().strftime("%Y:%m:%d %H:%M:%S"),
    # "time_taken": time(),
    "software": "N/A",
    "camera_maker": "Allied Vision",
    "camera_model": "Guppy",
    "camera_model_number": "F-033",
    # paramètres
    # "camera_exposure": 11000,
    # "camera_black_level": 0,
    # "camera_gain": 0,
}
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()


def take_picture(
        camera: Camera,
        experiment_name: str,
        folder_name: Optional[str] = None,
        picture_data_dict: Optional[dict[str, Union[str, float]]] = None,
        picture_number: float = None,
        saving_path: Path = Path("Results"),
        display: bool = False,
        ) -> tuple[Path, np.array]:
    """Take a picture from the specified camera

        Function that takes a picture from one camera. The camera must be in video mode
        because we just take one frame and save it. We use the function display frame to
        achieve that.

        It put it in a folder corresponding to the polarization within a folder with the
        sample name in the provided root path

        Parameters
        ----------
        camera
            `Vimba` `Camera` object to get the picture from
        experiment_name
            Sample name

            Used to create the sample data folder
        folder_name
            Name of the folder to put the picture in

            If `None`, the picture will be saved in polarization folders directly in the
            sample folder

            Default: None
        additional_string
            String added in the middle of the picture file names

            Default: None
        root_path
            Define the root path where the sample data folder will be placed

            Default: Path("Results")
        display
            Display the picture taken

            Default: False

        Returns
        -------
        tuple
            Path to the picture taken and an array representing the picture

        """

    # TODO: Quelle est la polarisation de la camera? (S ou P)
    polarization: str = "S"

    exposure_time = camera.ExposureTime.get()
    black_level = camera.BlackLevel.get()
    gain = camera.Gain.get()

    folder_path: Path
    if folder_name is not None:
        folder_path = saving_path / folder_name / polarization
    else:
        folder_path = saving_path / polarization
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    local_picture_data_dict = dict(GLOBAL_PICTURE_DATA_DICT)
    local_picture_data_dict.update(
            {
                "experiment_name": experiment_name,
                "polarization": polarization,
                "datetime": datetime.now().strftime("%Y:%m:%d %H:%M:%S"),
                "time_taken": time(),
                "picture_number": picture_number,
                "camera_exposure": exposure_time,
                "camera_black_level": black_level,
                "camera_gain": gain,
            }
    )

    if picture_data_dict is not None:
        local_picture_data_dict.update(picture_data_dict)  # noqa
    print(local_picture_data_dict)

    picture_filename: Path
    # si local_picture data dict possede number
    if picture_number is None:
        picture_filename = (
                folder_path
                / f'{experiment_name} - {datetime.now().strftime("%d %B %Hh%Mm%Ss")}.tif'
        )
    else:
        picture_filename = folder_path / (f"{experiment_name} - {picture_number}.tif")

    ##
    frame = camera.get_frame
    current_datetime = local_picture_data_dict["datetime"].encode("ascii") + b"\0"
    tifffile.imwrite(
        picture_filename,
        frame,
        description=local_picture_data_dict["experiment_name"],
        datetime=current_datetime,
        software=local_picture_data_dict["software"],
        extratags=(
            (
                TIFF.TAGS["ImageDescription"],
                TIFF.DATATYPES.ASCII,
                None,
                local_picture_data_dict["experiment_name"],
            ),
            (
                TIFF.TAGS["Software"],
                TIFF.DATATYPES.ASCII,
                None,
                local_picture_data_dict["software"],
            ),
            (
                TIFF.TAGS["Make"],
                TIFF.DATATYPES.ASCII,
                None,
                local_picture_data_dict["camera_maker"],
            ),
            (
                TIFF.TAGS["ExposureTime"],
                TIFF.DATATYPES.RATIONAL,
                1,
                (1, round(1 / local_picture_data_dict["camera_exposure"] / 1e6)),
            ),
            (
                TIFF.TAGS["Model"],
                TIFF.DATATYPES.ASCII,
                None,
                f'{local_picture_data_dict["camera_model"]} '
                f'{local_picture_data_dict["camera_model_number"]}, ',
            ),
            (TIFF.TAGS["DateTime"], TIFF.DATATYPES.ASCII, 20, current_datetime),
            (TIFF.TAGS["DateTimeOriginal"], TIFF.DATATYPES.ASCII, 20, current_datetime),
            (
                TIFF.TAGS["DateTimeDigitized"],
                TIFF.DATATYPES.ASCII,
                20,
                current_datetime,
            ),
            (
                custom_tag,
                TIFF.DATATYPES.ASCII,
                None,
                json.dumps(local_picture_data_dict),
            ),
        ),
    )
    if display:
        cv2.imshow(f"{experiment_name} - {polarization}", frame)
        cv2.waitKey(1)

    return picture_filename, frame
