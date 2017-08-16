# UAGS
UAE Amiga Game Scraper, primarily for UAE4ARM/Amiberry on the Raspberry Pi.

# *** NOTE: THIS SCRAPER PROJECT IS NO LONGER IN DEVELOPMENT *** 

I have decided to close down development of this project, as it has now been supeseded by the vastly superior SkyScraper project by Lars Muldjord.

You can find details of his project here: https://github.com/muldjord/skyscraper


***  Old ReadMe for reference ***

This Python script will scrape game information form openretro.org in order to generate gamelist.xml, and can also download boxart/screenshots.


## Installation
  
From Linux Command Line or via SSH, use the following:

### Install Direct
```bash
cd /home/pi
sudo wget https://github.com/HoraceAndTheSpider/UAGS/archive/master.zip
sudo unzip -o master.zip
sudo rm master.zip
sudo rm -r .uags
sudo mv UAGS-master .uags
```

### Updating/Running:
```bash
cd /home/pi
cd .uags
python3 UAGS.py
```

