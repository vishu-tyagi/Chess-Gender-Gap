import os
from pathlib import Path
import logging
from typing import List, Tuple

import requests
import zipfile
import xml.etree.ElementTree as Xet
from tqdm import tqdm
import pandas as pd
import numpy as np

from chess_gender_gap.utils import timing

logger = logging.getLogger(__name__)


@timing
def download_data(url:str, save_path: Path) -> None:
    logger.info(f"Downloading {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(str(save_path), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    logger.info(f'Downloaded to {save_path}')
    return


@timing
def unzip(fpath: Path, directory_to_extract_to: Path):
    logger.info(f'Unzipping {fpath} ...')
    with zipfile.ZipFile(fpath, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    logger.info(f'Unzipped and saved to {directory_to_extract_to}')
    return


@timing
def parseXML(
    file_path: Path,
    columns: List[Tuple[str, type]],
    save_path: Path
) -> pd.DataFrame:
    logger.info(f'Parsing {file_path} into CSV ...')
    xmlparse = Xet.parse(file_path)
    root = xmlparse.getroot()
    rows = []
    for player in tqdm(root):
        row = {}
        for attribute, _ in columns:
            row[attribute] = player.find(attribute).text
        rows.append(row)
    df = pd.DataFrame(
        rows,
        columns=[attribute for attribute, _ in columns]
    )
    df.fillna(value=np.nan, inplace=True)
    for attribute, dtype in columns:
        if dtype != str:
            df[attribute] = df[attribute].astype(dtype)
    df.to_csv(save_path, index=False)
    logger.info(f'Saved to {save_path}')
    return


@timing
def fetch():
    url = 'http://ratings.fide.com/download/standard_rating_list_xml.zip'
    current_path = Path(os.getcwd())
    data_path = Path(os.path.join(current_path, 'data'))
    data_path.mkdir(parents=True, exist_ok=True)
    fname = 'standard_rating_list'
    zip_path = Path(os.path.join(data_path, f'{fname}.zip'))
    xml_path = Path(os.path.join(data_path, f'{fname}.xml'))
    csv_path = Path(os.path.join(data_path, f'{fname}.csv'))
    download_data(url, zip_path)
    unzip(zip_path, data_path)
    columns = \
        [
            ('fideid', int), ('name', str), ('country', str), ('sex', str),
            ('title', str), ('w_title', str), ('rating', int), ('birthday', float)
        ]
    parseXML(xml_path, columns, csv_path)
    return
