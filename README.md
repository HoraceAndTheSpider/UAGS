# UAGS
UAE Amiga Game Scraper

Stage 1 : New Program

'Scrape' WHDLoad data folders

 - > convert to .uae name (use existing config maker code)
 - > produce OpenRetro Link, -> WHDLoad page link (code for this exists) 
 - > store links in MasterWHDPageList.txt   gamename~


Stage 2: Updates Config Maker

 - > if a WHDLoad data folder is on MasterWHDPageList.txt
   .. - Read Existing Slave for file version
   .. - Read OpenRetro or WHDLoad.de For Latest version?

   - > If update is required

	.. download .lah
 	.. unpack
	.. copy to data folder
	.. 'soft' warning of update?


   .. - Delete any 'soft' warning in Data Folder:  WHDUpdateError.text


 - > if not ON MasterWHDPageList.txt
   .. - Create 'soft' warning in Data Folder:  WHDUpdateError.txt



Stage 3: WHD Booter Updates:

  - > in Data Folder:  WHDUpdateError.txt exists
  - > Display soft' update warning

  - > If any whdload error occurs, write to file 'critical' error 

  - > if whdload 'critical' error file has occured, display.
