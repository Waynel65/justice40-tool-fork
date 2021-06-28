from pathlib import Path
import csv
import os
from config import settings

from utils import remove_files_from_dir, remove_all_dirs_from_dir, unzip_file_from_url


def reset_data_directories(data_path: Path) -> None:
    census_data_path = data_path / "census"

    # csv
    csv_path = census_data_path / "csv"
    remove_files_from_dir(csv_path, ".csv")

    # geojson
    geojson_path = census_data_path / "geojson"
    remove_files_from_dir(geojson_path, ".json")

    # shp
    shp_path = census_data_path / "shp"
    remove_all_dirs_from_dir(shp_path)


def get_state_fips_codes(data_path: Path) -> list:
    fips_csv_path = data_path / "census" / "csv" / "fips_states_2010.csv"

    # check if file exists
    if not os.path.isfile(fips_csv_path):
        unzip_file_from_url(
            settings.AWS_JUSTICE40_DATA_URL + "/Census/fips_states_2010.zip",
            data_path / "tmp",
            data_path / "census" / "csv",
        )

    fips_state_list = []
    with open(fips_csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                fips = row[0].strip()
                fips_state_list.append(fips)
    return fips_state_list