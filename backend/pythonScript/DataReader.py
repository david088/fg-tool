import requests
import io, json
import re
from bs4 import BeautifulSoup


# Get html of the Kharacter selection web page
kharacterSelectionURL = "https://www.kombatakademy.com/mortal-kombat-11/kharacters/"
kharacterR = requests.get(kharacterSelectionURL)
kharacterSoup = BeautifulSoup(kharacterR.text, "html.parser")
kharacterElement = kharacterSoup.find("div", class_="portraits")

# Initialize arraies
urlArr = []
kharacterNameArr = []

# Find all links to each kharacter
for link in kharacterElement.find_all('a'):

    # Parse kharacter name and url
    kharacterURL = link.get("href")
    kharacterURL = kharacterURL.encode("utf-8")
    kharacterNAME = link.find("img").get("alt")
    kharacterNAME = kharacterNAME.encode("utf-8")

    # Append to respective arraies
    urlArr.append(kharacterURL)
    kharacterNameArr.append(kharacterNAME)

# Initialize the move frame array
moveTableArr = []

# Check every kharacter link
for fighterLink in urlArr:

    # check correctness
    #print(fighterLink) 

    # Get html of the url
    r = requests.get(fighterLink)

    # Using BeautifulSpou to parse html
    soup = BeautifulSoup(r.text, "html.parser")
    element = soup.find("div", class_="scroll")

    # Initialize variables variables
    moveArr = []
    moveFrameArr = []
    frameNameArr = ["Damage", "Block Damage", "F/Block Damage", 
                "Move Type", "Variation", "Properties1", 
                "Properties2", "Description", "Startup", 
                "Active", "Recovery", "Hit Advantage", 
                "Block", "F/Block Advantage"]

    # In a loop, parse all <tr></tr> element
    for link in element.find_all('tr'):
    
        # Only convert string is it is not NoneType
        if (link.find("td").find("div", style="float: left; position: relative; height: auto;")) is not None:
        
            # Get name of the move
            moveName = (link.find("td").find("div", style="float: left; position: relative; height: auto;")).get_text()
        
            # Remove all space or tabs
            moveName = re.sub('\s+', '', moveName)

            # Serializing json
            moveArr.append(moveName)

        # print((link.find("td").find("div", style="float: left; position: relative; height: auto;")).get_text())
        # if link.find("td").get("class") != "subcategory":
        if link.find("td").get("class") is None:
            moveFrame = link.find("td").get("onmouseover")
            asciistring = moveFrame.encode("utf-8")
            asciistring = re.sub('\s+', '', asciistring)

            z = asciistring.replace("'", '"')
            tempArr = re.findall('"([^"]*)"', z)
            frameDic = {
                "Startup":tempArr[8],
                "Block":tempArr[13]
            }
            moveFrameArr.append(frameDic)
            #print(frameDic)

    #print(moveFrameArr)

    # Form move table dictionary 
    moveTable = dict(zip(moveArr, moveFrameArr))
    moveTableArr.append(moveTable) # Append to move frame data arr

# Create character table dictionary for all kharacters
characterTable = dict(zip(kharacterNameArr, moveTableArr))

# Convert to json
jsonCharacterTable = json.dumps(characterTable)

# Printing to check correctness
#print(jsonCharacterTable)

# Write json dictionary to a file
with open("KharacterMoveFrameData.json", "w") as outfile: 
    outfile.write(jsonCharacterTable) 
