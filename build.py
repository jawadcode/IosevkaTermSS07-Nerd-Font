from dataclasses import dataclass
from io import BytesIO
import os
from os import path
import shutil
import subprocess
from zipfile import ZipFile

import requests

latest_release = requests.get("https://api.github.com/repos/be5invis/Iosevka/releases/latest") \
                         .json()
print("Downloading latest release: " + latest_release["name"])

def rm_if_exists(p: str):
    if path.exists(p): shutil.rmtree(p)

rm_if_exists("patched")
os.mkdir("patched")

ver_name = latest_release["tag_name"]
iosevka_zipfile_name = f"PkgTTF-IosevkaTermSS07-{ver_name[1:]}.zip"
iosevka_zipfile_url = \
    f"https://github.com/be5invis/Iosevka/releases/download/{ver_name}/{iosevka_zipfile_name}"
iosevka_zip_data = requests.get(iosevka_zipfile_url).content

with ZipFile(BytesIO(iosevka_zip_data), mode="r") as iosevka_zip:
    os.mkdir("unpatched")
    print("hi")
    files = iosevka_zip.namelist()
    for font in files:
        iosevka_zip.extract(font, "unpatched")
        subprocess.run(
            ["nerd-font-patcher",
             f"unpatched/{font}",
             "-out", "patched"]
        )

    shutil.rmtree("unpatched")
        
