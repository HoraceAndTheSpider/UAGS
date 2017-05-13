
#random test for VS2010

import glob, platform
from urllib.request import *
import ssl
import os

from bs4 import BeautifulSoup

from uags.UAGS_Functions import *
from uags.UAGS_oagd import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

## main section starting here...

print()
print(bcolors.BOLD + bcolors.OKBLUE + "HoraceAndTheSpider" + bcolors.ENDC + "'s " + "openretro.org " + bcolors.BOLD + "UAE4Arm Amiga Game Scraper" + bcolors.ENDC + " | " + "" + bcolors.FAIL + "www.ultimateamiga.co.uk" + bcolors.ENDC)
print()

## check for overwrite of existing entries
NewScrapes = input("Scrape existing game entries? " + bcolors.OKBLUE + "(y/n) " + bcolors.ENDC)

if NewScrapes != "yes" and NewScrapes != "y" and NewScrapes != "Y" and NewScrapes != "YES":
    NewScrapes = "n"
    print("Existing game entries will " + bcolors.BOLD + "not" + bcolors.ENDC + " be scraped.")    
else:
    NewScrapes = "y"
    print("All found game entries will be scraped.")
    
print()   

## all a filter to be used

ScanFilter = input("Limit scanned files to a specific pattern match? " + bcolors.OKBLUE + "(Enter pattern or leave blank) " + bcolors.ENDC)
print()


## check for overwrite of existing images
NewImages = input("Overwrite existing images, such as in " + bcolors.BOLD + "boxarts/" + bcolors.ENDC + " ? " + bcolors.OKBLUE + "(y/n) " + bcolors.ENDC)

if NewImages != "yes" and NewImages != "y" and NewImages != "Y" and NewImages != "YES":
    NewImages = "n"
    print("Existing images will " + bcolors.BOLD + "not" + bcolors.ENDC + " be overwritten.")
else:
    NewImages = "y"
    print("Existing images will be overwritten.")

print()


# Check for saving bonus material images
AllImages = input ("Store additional images to " + bcolors.BOLD + "snap/" + bcolors.ENDC + "and" + bcolors.BOLD + " wheel/" + bcolors.ENDC + " ? " + bcolors.OKBLUE + "(y/n) "+ bcolors.ENDC )

if AllImages != "yes" and AllImages != "y" and AllImages != "Y" and AllImages != "YES":
    AllImages = "n"
    print ("Additional images will " + bcolors.BOLD + "not"+ bcolors.ENDC + " be stored.")
else:
    AllImages = "y"
    print ("Additional images will be stored.")

print()


## initialisations   

ScannedGames = 0
LimitResults = 0
##ScanFilter = "Five"

XML = ""
ExitButton = False
KeyRead = 0
ErrorMessage = ""


try:
        ssl._create_default_https_context = ssl._create_unverified_context
except:
        pass
    
## -------- input dir

if platform.system()=="Darwin":
    inputdir="/Volumes/roms/amiga/"
    inputdir = "/Users/horaceandthespider/Documents/Gaming/AmigaWHD/WorkingFolder2/ECS Pack/"

 ## -------- I SEE YOU AINGER! o_o
elif platform.node()=="RAVEN":
    inputdir="C:\\Users\\oaing\\Desktop\\whdload\\"
else:
    inputdir="//home/pi/RetroPie/roms/amiga/"
    

# paths/folders if needed

os.makedirs(inputdir + "boxart", exist_ok=True)

if AllImages == "y":
    os.makedirs (inputdir + "wheel", exist_ok=True)
    os.makedirs (inputdir + "snap", exist_ok=True)



# here, we will open an existing XML, *or* create one.

XML_File = inputdir + "gamelist.xml"

if (os.path.isfile(XML_File)) == False:
    
        XML = '<?xml version="1.0"?>\n<gameList>\n'
        XML = XML + "</gameList>"

        text_file = open(XML_File, "w")
        text_file.write(XML)
        text_file.close()

text_file = open(XML_File, "r")
XML = text_file.read()
text_file.close()


## check XML validity
if XML.find("?xml version=")<0 or XML.find("<gameList>")<0 or XML.find("</gameList>")<0:

    print (bcolors.FAIL + ">> XML File "+ bcolors.BOLD + XML_File + bcolors.ENDC + bcolors.FAIL + " is malformed." + bcolors.ENDC )

    KillXML = input ("Delete file prior to restart? (y/n) "+ bcolors.ENDC )

    if KillXML != "yes" and KillXML != "y" and KillXML != "Y" and KillXML != "YES":
        raise SystemExit
    else:
        print("Deleting 'gamelist.xml'")
        os.remove(XML_File)
        raise SystemExit


## ======== MAIN FILE READING LOOP

for filename in glob.glob(inputdir+'*.uae'):

    ScannedGames = ScannedGames + 1

##    filename = "Bloodwych (& Extended Levels).uae"
    
    GameVariant = ""
    GameEntry = ""
    
# Get the name, and remove extension and path
    GameName = filename
    GameName = GameName.replace ('.uae','')
    GameName = GameName.replace (inputdir,'')

    RealName = filename
    RealName = RealName.replace (inputdir,'')


# finally, this filter should work...
    if GameName == "_Config Maker":
        print("Scraping data for " + bcolors.OKGREEN + GameName + bcolors.ENDC + " from external source.")
        
        GameEntry = MakeGameEntry(RealName,'','','',AllImages)
        ErrorMessage = ErrorMessage + GetPictures(RealName,"",AllImages,NewImages,inputdir)
    
    elif GameName.find(ScanFilter) == -1 and ScanFilter != '':
       print("Filter applied. Entry for " + bcolors.OKGREEN + GameName + bcolors.ENDC + " skipped.")

# so, if it's aready in there, and we are *not* scraping everything
    elif NewScrapes=="n" and XML.find("<path>./" + RealName + "</path>") > -1:
       print("Existing entry for " + bcolors.OKGREEN + GameName + bcolors.ENDC + " - skipping.")
        

##       OMG i cannot believe i just 'tabbed' *everything in the loop for this...
    else:  

  # Find the game type
  ## i think i can remove lots of these now.... (1,2,4 and 5)

        if GameName.find(' [AGA]')>0:
            GameType = 'AGA'
            SearchType = 'amiga'
            GameName = GameName.replace (' [AGA]','')
            
        elif GameName.find(' [CD32]')>0:
            GameType = 'CD32'
            SearchType = 'cd32'
            GameName = GameName.replace (' [CD32]','')
            
        elif GameName.find(' [CDTV]')>0:
            GameType = 'CDTV'
            SearchType = 'cdtv'
            GameName = GameName.replace (' [CDTV]','')

        elif GameName.find(' [CD]')>0:
            GameType = 'AGA'
            SearchType = 'amiga'
            GameName = GameName.replace (' [CD]','')
            
        else:
            GameType = 'ECS'
            SearchType = 'amiga'

    # Tidy the spaces etc for the search string
        ParseName = GameName.replace('-','')
        ParseName = ParseName.replace('&','%26')
        ParseName = ParseName.replace('+','%2B')
        ParseName = ParseName.replace(' ','+')
        ParseName = ParseName.replace('++','+')

        
    ##    print ("Searched for " + ParseName)
        print ()
        print (bcolors.OKBLUE + str(ScannedGames) + bcolors.ENDC + ": Searching for: " + bcolors.BOLD + GameName + bcolors.ENDC + " (" + ParseName+") " + GameType)
        print (bcolors.HEADER + "     "  + filename + bcolors.ENDC)
        print ()


    ##  lets search the database!
        FindLink = ""
        NewParseName = ""

     ### Here , we can do a loop
        ## we will 'break' if we find a link though
        ## pass 1, search as normal
        ## pass 2, search with brackets as '[' ']' ... for games where a name is shared 
        ## pass 3, search with brackets as '' ... for games like Cannon Fodder (New Campaign)
        ## pass 4, search with brackets omitted completely and the extra bits stored for later use .. in GameVariant
        ## ...        
        ## pass 9, ???
        ## pass 10, profit!
        
        ## if we *didnt find anything, we  re-try, with anything in brackets removed (alternative versions etc)
        ##  -- we will also store the brackets information to put in the XML description (to show different versions apart)            

    ##import re
    ##re.sub(r'\s\(.*\)', '', "Lemmings (2 Disk)")
        
        for Pass in range(1,5):

            # special 'pass' rules

            if Pass==1:
                    NewParseName = ParseName
            elif Pass==2:
                    NewParseName = ParseName
                    NewParseName = NewParseName.replace(')','')
                    NewParseName = NewParseName.replace('(','')
            elif Pass==3:
                    NewParseName = ParseName
                    NewParseName = NewParseName.replace('[','')
                    NewParseName = NewParseName.replace(']','')
            elif Pass==4:
                    NewParseName = ParseName
                    NewParseName = NewParseName.replace(GetBrackets(ParseName),'').strip()
                    GameVariant = GetBrackets(GameName)                   


        ##  here we do the actual searches
        ##    first of all, we have a special rule for AGA games, because they are pain in the b*m
            if GameType == 'AGA':
                    SearchString = 'https://openretro.org/browse/'+SearchType+'?q=' + NewParseName + "+[AGA]"+"&disabled=1&unpublished=1"
                    FindLink,FindImage,FindGame = WebSearchResult(SearchString,GameName,GameType,Pass)

        ##    for everything else,  we had no result, and/or we didnt select x/s, we will behave 'normally'
            if FindLink=="":
                    SearchString = 'https://openretro.org/browse/'+SearchType+'?q=' + NewParseName + "&disabled=1&unpublished=1"
                    FindLink,FindImage,FindGame = WebSearchResult(SearchString,GameName,GameType,Pass)

        ##    with these multiple searches, i may need a 'continue' option
            if FindLink =="c":
                   FindLink = ""
                    
            if FindLink != "":
                    break
                    
    ## check for abort

        if FindLink == "x":
            FindLink = ""
            temp = ">> " + str(GameName) + " aborted. no single page selected, and scraping ended."
            print (bcolors.FAIL + temp + bcolors.ENDC)
            ErrorMessage = ErrorMessage + str(RealName) + "\t aborted. no single page selected, and scraping ended.\n"
                    
            break

        elif FindLink == "s":
            FindLink = ""
##            temp = ">> " + str(GameName) + " aborted. no single page selected, user skipped."
##            print (bcolors.FAIL + temp + bcolors.ENDC)
##            ErrorMessage = ErrorMessage + str(RealName) + "\t aborted. no single page selected, user skipped..\n"



    ## after all that, we still havent found a link.
        if FindLink=="":
            temp = ">> " + str(GameName) + " skipped. no single page selected."
            print()
            ErrorMessage = ErrorMessage + str(RealName) + "\t skipped. no single page selected.\n"
    ##            game=str(game.encode('utf-8'), 'utf-8').replace("Cover for ","")
            print (bcolors.FAIL + temp + bcolors.ENDC)

        else:

    ##      resolve the link into a single string        
            FindLink = "https://openretro.org" + FindLink + "/edit"
            WebString = ""
            
            f = urllib.request.urlopen(FindLink)
            WebString = f.read()
            f.close()


    # ====     create individual game XML based on reading from the above cached page
        ##    see UAGS_oagd.py
            GameEntry = MakeGameEntry(RealName,GameVariant,GameType,WebString,AllImages)
    
    ## ========== do the image downloads
            print("real name: " + RealName)
            print("web string: "+WebString)
            print("all images: " + AllImages)
            print("new images: " + NewImages)
            print("input dir: "+inputdir)
            ErrorMessage = ErrorMessage + GetPictures(RealName,WebString,AllImages,NewImages,inputdir)
 

    ##      remove any previous game entry (if overwrite is on)

    if GameEntry != '':
        if NewScrapes=="y" and XML.find(RealName) > -1:
                print("     Removing existing entry for " + bcolors.OKBLUE + RealName + bcolors.ENDC +".")
                print()
                OldGameEntry = FindGameTagEntry(XML,RealName,"<game>")
                XML = XML.replace(OldGameEntry,"")

    ##      adds the game-entry 
        XML = XML.replace("</gameList>",GameEntry +"</gameList>")
        print (bcolors.OKGREEN + ">> " + filename + " scraped." + bcolors.ENDC)
        print ()

    ## save out the file(s) 
    ## we are done!!  let's create the new XML
        print (bcolors.OKGREEN + ">> Updating "+ bcolors.BOLD + "gamelist.xml" + bcolors.ENDC )
        text_file = open(XML_File, "w")
        text_file.write(XML)
        text_file.close()
        print()


    ## special code for testing only!
    if ScannedGames > LimitResults-1 and LimitResults != 0:
         break        


#### we are done!!  let's create the new XML
##print()
##print (bcolors.OKGREEN + ">> Generating "+ bcolors.BOLD + "gamelist.xml" + bcolors.ENDC )




if ErrorMessage != "":
    ErrorMessage = "The following errors occured during scraping:" + "\n\n" + ErrorMessage
    print (bcolors.FAIL + ">> Generating "+ bcolors.BOLD + "errorlist.txt" + bcolors.ENDC )
    text_file = open(inputdir + "errorlist.txt", "w")
    text_file.write(ErrorMessage)
    text_file.close()

print()

raise SystemExit


        


