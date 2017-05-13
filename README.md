# UAGS
UAE Amiga Game Scraper, primarily for UAE4ARM/Amiberry on the Raspberry Pi.

This Python script will scrape game information form openretro.org in order to generate gamelist.xml, and can also download boxart/screenshots.


## Installation
  
From Linux Command Line or via SSH, use the following:

### Install Direct
```bash
sudo wget https://github.com/HoraceAndTheSpider/UAGS/archive/master.zip
sudo unzip -o master.zip
sudo rm master.zip
mv UAGS-master .uags
```

### Updating/Running:
```bash
cd /home/pi
cd .uags
python3 UAGS.py
```

