import os
import requests
import zipfile
import logging
from tqdm import tqdm
from typing import Any

class Downloader:
    def __init__(self, url: str, download_path: str = "../dataset") -> None:
        self.url: str = url
        self.download_path: str = download_path
        self.logger: Any = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def download(self) -> None:
        filename: str = self.url.split("/")[-1]
        file_path: str = os.path.join(self.download_path, filename)

        # Create the directory if it doesn't exist
        os.makedirs(self.download_path, exist_ok=True)

        try:
            # Check if the file already exists
            if not os.path.isfile(file_path):
                self.logger.info(f"Downloading {self.url}...")
                response: Any = requests.get(self.url, stream=True)
                total_size_in_bytes= int(response.headers.get('content-length', 0))
                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                with open(file_path, 'wb') as f:
                    for data in response.iter_content(chunk_size=1024):
                        progress_bar.update(len(data))
                        f.write(data)
                progress_bar.close()
                self.logger.info(f"Download completed. File saved to {file_path}")
            else:
                self.logger.info(f"File {file_path} already exists.")

            # If it's a zip file, extract it
            if zipfile.is_zipfile(file_path):
                self.logger.info(f"Extracting {file_path}...")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for member in tqdm(zip_ref.infolist(), desc='Extracting '):
                        zip_ref.extract(member, self.download_path)
                self.logger.info(f"File {file_path} extracted.")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")

# Usage
downloader = Downloader("https://physionet.org/static/published-projects/eegmmidb/eeg-motor-movementimagery-dataset-1.0.0.zip")
downloader.download()
