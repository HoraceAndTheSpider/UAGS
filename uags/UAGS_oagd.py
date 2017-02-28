## ------
##   scan through the results page, to see if anything matches
## --------

import glob, platform
from urllib.request import *
import urllib
import ssl
import os

from bs4 import BeautifulSoup

from uags.UAGS_Functions import *

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

        
def WebSearchResult(inWeb,GameName ,GameType, PassNumber = 0):
    
    f = urllib.request.urlopen(inWeb)
    SearchResultPage = f.read()
    f.close()

    soup = BeautifulSoup(SearchResultPage,'html.parser')
    soup = soup.find(id="fs-content")

    link=""
    image=""
    game = ""
        
    ResultCount = int((len(soup.find_all('div'))-3)/2)

    
    if ResultCount==0:
        z="no results"
        link=""
        image=""
        game = ""
        ZeroMessage = "     No results found. (Pass "+str(PassNumber)+")"
        if right(inWeb,5) == "[AGA]":
            ZeroMessage = ZeroMessage + " (" + GameType + " search.)"
        print (bcolors.WARNING + bcolors.BOLD + ZeroMessage + bcolors.ENDC)


    
    elif ResultCount>1:
        z="mutiple results"
        link=""
        image=""
        game = ""
        tempgame = ""
        templink = ""
        tempimage = ""

##        ' first, see if we have an 'exact match' answer (e.g. "Lemmings")
        soup = soup.find_all("div","game_box")
##        print ("Trying to match game name :" + GameName)

        OptionNumber = 0

        for tag in soup:
            link = tag.find("a")
            link = link.get('href')
            
            image = tag.find("img")
            game = image
            image = image.get("src")
            game = game.get("alt")

        
            game=str(game.encode('utf-8'), 'utf-8').replace("Cover for ","")
            OptionNumber = OptionNumber +1
            
            print ("     Found Game: " + game + bcolors.OKBLUE + " (" + str(OptionNumber) + ")" + bcolors.ENDC)

##          simple 'name' equals result , or name = 'the' + result
##          also allow eIF result has ": " swapped for " - "
            
            if (GameName.lower() == game.lower() or
                "the "+ GameName.lower() == game.lower() or
                GameName.lower() == game.lower().replace(": "," - ") or
                "the "+ GameName.lower() == game.lower().replace(": "," - ")):

                tempgame = game
                templink = link
                tempimage = image
                
##          simple name equals result, IF result has ": " swapped for " - "
#
# 
#
#

##          'name' + gametype (aga/ecs) = result
            elif ((GameName.lower() + " [" + GameType.lower() + "]") == game.lower() or
                 ("the "+GameName.lower() + " [" + GameType.lower() + "]") == game.lower()):
                tempgame = game
                templink = link
                tempimage = image
                
            else:
                link=""
                image=""
                game = ""               

        
##      ' if we still dont, then we will have to use a 'picker'

        GetOption = ""
        while GetOption == "" and tempgame=="":
        
            GetOption = input(bcolors.OKBLUE + "     Select 1-" + str(int(ResultCount)) + ", s to skip game, c to skip but continue next pass, or x to exit:  " + bcolors.ENDC)

            if is_number(GetOption) == False and GetOption != "x" and GetOption != "s" and GetOption != "c":
                print ("Invalid selection")
                GetOption = ""
                              
            elif is_number(GetOption) == True:
                if int(GetOption)<1 or int(GetOption)>ResultCount:
                    print ("Invalid selection")
                    GetOption = ""

        ##  we declined, an option 
        if GetOption == "s":
            link="s"
            image=""
            game = ""

        elif GetOption == "c":
            link="c"
            image=""
            game = ""
                    
        elif GetOption == "x":
            link="x"
            image=""
            game = ""

        ##  or we auto-picked earlier
        elif tempgame != "":

            game = tempgame
            link = templink
            image = tempimage
                       
            print ("     Multiple results but exact match on: " + bcolors.BOLD + bcolors.OKBLUE + game + bcolors.ENDC)

           
        ##  otherwise scroll through again, to get our option
        else:
            OptionNumber = 0

            
            for tag in soup:
                link = tag.find("a")
                link = link.get('href')
                
                image = tag.find("img")
                game = image
                image = image.get("src")
                game = game.get("alt")
                
                game=str(game.encode('utf-8'), 'utf-8').replace("Cover for ","")
                OptionNumber = OptionNumber +1

                if str(OptionNumber) == str(GetOption):
                        print ()
                        print ("     Selected: " + bcolors.OKBLUE + bcolors.BOLD + game + bcolors.ENDC)
                        break

            
    else:
        z="one result"
        
        soup = soup.find_all("div","game_box")    
        for tag in soup:
            link = tag.find("a")
            link = link.get('href')
            
            image = tag.find("img")
            game = image
            image = image.get("src")
            game = game.get("alt")
            
#            game=(game).encode('utf-8').replace("Cover for ","")
            game=str(game.encode('utf-8'), 'utf-8').replace("Cover for ","")
            print ( "     Single result on: " + bcolors.OKBLUE + bcolors.BOLD + game + bcolors.ENDC)
                

        if game=="":
            print (bcolors.WARNING + bcolors.BOLD + "     Single result found but could not be used. Possible unpublished openretro.org entry." + bcolors.ENDC)

            
    print ()
    return str(link),str(image),str(game)



## ------
##   Find the OAGD (openretro.org) entry
## --------
                
def OAGD_EntryResult(SearchResultPage,FindData):

    answer = ""
    biganswer = ''
    firstanswer = ''
    
##    f = urllib.request.urlopen(inWeb)
##    SearchResultPage = f.read()
##    f.close

    soup = BeautifulSoup(SearchResultPage,'html.parser')
    soup = soup.find("table")
    soup = soup.find_all("td")

##    FindData = 'tags'

    
    for tag in soup:
        biganswer = ''
    
        if  tag.get_text()==FindData:
            firstanswer = tag.parent.find('div')
            multianswer = firstanswer.find_all('a')
            
            for items in multianswer:

                if biganswer !=  '':
                    biganswer = biganswer + ", " + items.get_text()
                else:
                    biganswer = items.get_text()
        
            firstanswer =  str(firstanswer.get_text())
            biganswer = str(biganswer)
            break
        else:
            firstanswer = ""


    if len(biganswer) > len (firstanswer):
        answer = biganswer
    else:
        answer = firstanswer
        
    return str(answer)


## ------
##   Find a download link for an image, using the HOL number
## --------


def HOL_URL(inText,inType = "box"):

    inType = inType.lower()
    
    if inType != "title" and inType != "screen" and inType != "box":
        inType = "box"
        print ("what!")
        
    if is_number(inText) == False:
        return ''
     
    HOLnumber = int(inText)
    if HOLnumber > 9899:
            HOLnumber = 9899
    
    HOLnumber_text = str(((int((HOLnumber-1)/100) * 100) + 1)).zfill(4)
    HOLnumber_text = HOLnumber_text + '-'
    HOLnumber_text = HOLnumber_text + str((int((HOLnumber-1)/100)+1) * 100).zfill(4)

    HOLnumber_text = HOLnumber_text + "/" + str(HOLnumber)
    
    if inType == "box":
        ## http://hol.abime.net/pic_preview/boxscan/0101-0200/158_box1.jpg
        HOLnumber_text = "http://hol.abime.net/pic_preview/boxscan/" + HOLnumber_text + "_box1.jpg"
        
    elif inType == "screen":
        ## http://hol.abime.net/pic_full/screenshot/0101-0200/158_screen1.png
        HOLnumber_text = "http://hol.abime.net/pic_full/screenshot/" + HOLnumber_text + "_screen1.png"
        
    elif inType == "title":
        ## http://hol.abime.net/pic_full/dbs/0601-0700/619_dbs1.png
        HOLnumber_text = "http://hol.abime.net/pic_full/dbs/" + HOLnumber_text + "_dbs1.png"

        
    return str(HOLnumber_text)

## ------
##   Find the HOL number from a URL
## --------


def HOL_Number(inURL):

    inURL = inURL.lower()
    
    if inURL.find("http://hol.abime.net/")<0:
        return 0
    
    return int(inURL.replace("http://hol.abime.net/",""))





def MakeGameEntry(RealName,GameVariant,GameType,WebString):
# ====     create individual game XML based on reading from the  cached page
     # etree  ... ?


    if RealName ==  '_Config Maker.uae':
            GameEntry = ""
            GameEntry = GameEntry + "\t<game>\n" 
            GameEntry = GameEntry + "\t\t<path>./" + RealName + "</path>\n"                                                
            GameEntry = GameEntry + "\t\t<name>_HoraceAndTheSpider's UAE Configuration Maker</name>\n"
            GameEntry = GameEntry + "\t\t<image>./covers/" + RealName.replace('.uae','') + ".jpg" + "</image>\n"            
            GameEntry = GameEntry + "\t\t<desc></desc>\n"

            GameEntry = GameEntry + "\t\t<releasedate>2016</releasedate>\n"
            GameEntry = GameEntry + "\t\t<developer>Dom Cresswell</developer>\n"
            GameEntry = GameEntry + "\t\t<publisher>www.</publisher>\n"
            GameEntry = GameEntry + "\t\t<genre>Application</genre>\n"
            GameEntry = GameEntry + "\t\t<players>0</players>\n"
            GameEntry = GameEntry + "\t</game>\n"

        

    elif WebString != '':
        
            GameEntry = ""
            GameEntry = GameEntry + "\t<game>\n" 
            GameEntry = GameEntry + "\t\t<path>./" + RealName + "</path>\n"
            
            SelectedName = OAGD_EntryResult(WebString,'game_name')

            if GameVariant !='':
                SelectedName = SelectedName+ " " + GameVariant
                
            if GameType != 'ECS' and SelectedName.find("["+GameType+"]")<0:
                SelectedName = SelectedName+ " [" + GameType + "]"
                
            SelectedName = SelectedName.replace(":","")
            SelectedName = SelectedName.replace("/","-")                                           

                                                
            GameEntry = GameEntry + "\t\t<name>" + SelectedName + "</name>\n"
            GameEntry = GameEntry + "\t\t<image>./boxart/" + RealName.replace('.uae','') + ".jpg" + "</image>\n"


            GameEntry = GameEntry + "\t\t<marquee>./wheel/" + RealName.replace('.uae','') + ".png" + "</marquee>\n"


            if (os.path.isfile("./video/" + RealName.replace('.uae','') + ".mp4")) == True:
                GameEntry = GameEntry + "\t\t<video>./video/" + RealName.replace('.uae','') + ".mp4" + "</video>\n"
            else:
                GameEntry = GameEntry + "\t\t<video>./snap/" + RealName.replace('.uae','') + ".png" + "</video>\n"

            
            LongText = OAGD_EntryResult(WebString,'__long_description')
            LongText = LongText.replace('<cite>','')
            LongText = LongText.replace('</cite>','')
            LongText = LongText.replace('<p>',' ')
            LongText = LongText.replace('</p>','')
            LongReplace = chr(0xC2)+chr(0xA0)+chr(0x0D)+chr(0x0A)+chr(0x32)
            LongText = LongText.replace(LongReplace,' ')
            
            GameEntry = GameEntry + "\t\t<desc>" + LongText + "</desc>\n"

            GameEntry = GameEntry + "\t\t<releasedate>" + OAGD_EntryResult(WebString,'year') + "</releasedate>\n"
            GameEntry = GameEntry + "\t\t<developer>" + OAGD_EntryResult(WebString,'developer') + "</developer>\n"
            GameEntry = GameEntry + "\t\t<publisher>" + OAGD_EntryResult(WebString,'publisher') + "</publisher>\n"
            GameEntry = GameEntry + "\t\t<genre>" + OAGD_EntryResult(WebString,'tags') + "</genre>\n"
            GameEntry = GameEntry + "\t\t<players>" + OAGD_EntryResult(WebString,'players') + "</players>\n"
            GameEntry = GameEntry + "\t</game>\n"

    else:
            GameEntry = ""
            
    return GameEntry



def GetPictures(RealName,WebString,AllImages,NewImages,inputdir):

    myError = ""
    
    for Pass in range(1,4):

        if Pass == 1:
            oagd_image = "front_sha1"
            oagd_param = "?s=512&amp;f=jpg"
            hol_image = "box"
            my_save = "boxart/"
            my_desc = "box-art"
            pictureformat = ".jpg"

        elif Pass == 2:
            oagd_image = "title_sha1"
            oagd_param = "?w=332&amp;h=208"
            hol_image = "title"
            my_save = "wheel/"
            my_desc = "title screen"
            pictureformat = ".png"

        elif Pass == 3:
            oagd_image = "screen1_sha1"
            oagd_param = "?w=332&amp;h=208"
            hol_image = "screen"
            my_save = "snap/"
            my_desc = "screen-shot "
            pictureformat = ".png"


        
##   check if we are doing 'other' downloads
        if Pass>1 and AllImages != "y":
            break

        GetImage = ''
        HallOfLightLink = ''
        
##      try and get the OpenRetro box image 'name'
        if WebString != '':
           GetImage = str(OAGD_EntryResult(WebString,oagd_image))
           HallOfLightLink = OAGD_EntryResult(WebString,'hol_url')
 
        if GetImage != "":
             SpacePoint = GetImage.find(" ")
             if SpacePoint > 0:
                   GetImage = left(GetImage,SpacePoint)
             GetImage = "https://openretro.org/image/"+GetImage + oagd_param
    
       # otherwise, try HOL                    
        elif GetImage == "" and HallOfLightLink != '':
            GetImage = HOL_URL(HOL_Number(HallOfLightLink),hol_image)

        
        if RealName == "_Config Maker.uae" and Pass == 1:
            GetImage = "http://www.djcresswell.com/RetroPie/UAGS/_Config%20Maker.jpg"

##      do the  download 
        if GetImage != "" and (os.path.isfile(inputdir + my_save + RealName.replace('.uae','')  +pictureformat) == False or NewImages == "y"):


        ## dont forget to trap a failed download (HOL will always attempt) 
            try:
               a = urllib.request.urlretrieve(GetImage, inputdir + my_save + RealName.replace('.uae','') + pictureformat)

            except urllib.error.HTTPError as err:
               myError = myError + str(RealName) + "\t  no " + my_desc + " downloaded. (Web Page not found)\n"

        elif GetImage == "":
             myError = myError + str(RealName) + "\t  no " + my_desc + " downloaded. (Could not produce link)\n"
        

##                        awaiting Olly's code!
##                        if GetImage.find("hol.abime.net") > -1 and Pass == 2: 
##                            SplitPicture(inputdir + my_save + RealName.replace('.uae','')  + pictureformat)
                        

    return myError
