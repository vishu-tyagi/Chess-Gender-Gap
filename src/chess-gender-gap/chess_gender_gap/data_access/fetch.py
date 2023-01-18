import os
from pathlib import Path
import logging

import requests

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
    logger.info(f'Saved to {save_path}')
    return


def fetch():
    url = 'http://ratings.fide.com/download/standard_rating_list_xml.zip'
    fname = 'standard_rating_list.xml'
    current_path = Path(os.getcwd())
    data_path = Path(os.path.join(current_path, 'data'))
    data_path.mkdir(parents=True, exist_ok=True)
    save_path = Path(os.path.join(data_path, fname))
    download_data(url, save_path)
