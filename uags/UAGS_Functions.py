
## ------
##   other random 'borrowed' functions etc
## --------

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def onKeyPress(event):
    text.insert('end', 'You pressed %s\n' % (event.char, ))
    
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, point, amount):
    return s[point:point+amount]


def GetBrackets(inString):

    StartPoint = inString.find("(")
    Original = left(inString,StartPoint)

    for n in range(0 , len(inString)):
        
        EndPoint = n
        if mid(inString,len(inString)-n-1,1) != ")":
            continue

    Final = mid(inString,StartPoint,EndPoint-StartPoint+1)

    return Final




def FindGameTagEntry(inXML,GameToFind,FindTag = "<game>"):

    if FindTag.find("</")<0:
        FindTag = FindTag.replace("<","</")

    FindPoint = inXML.find(GameToFind)
    StartPoint = 0
    EndPoint = 0
    
##    scroll left from there    
    for n in range(0 , FindPoint):

        StartPoint = FindPoint - n        
        if mid(inXML,StartPoint,len(FindTag)) == FindTag:
            break

    StartPoint = StartPoint + len(FindTag) + 1

##    scroll right from there                      
    for n in range(0 , FindPoint):
        EndPoint = FindPoint + n        
        if mid(inXML,EndPoint,len(FindTag)) == FindTag:
            break

    EndPoint = EndPoint + len(FindTag)
    GamePart = mid(inXML,StartPoint,EndPoint-StartPoint)

    if StartPoint == 0 or EndPoint==len(inXML):
        GamePart = ''
        
    return GamePart
        


