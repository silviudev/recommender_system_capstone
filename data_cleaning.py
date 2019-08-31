import csv
from collections import OrderedDict

dictList = []



def importAndCleanData():
    descriptionDict = {}
    mediaDict = {}

    # Put the descriptions into a dictionary for merging
    with open('data/original_data/steam_description_data.csv', newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            descriptionDict[row["steam_appid"]] = row["short_description"]

    # Put the game images into a dictionary for merging
    with open('data/original_data/steam_media_data.csv', newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            mediaDict[row["steam_appid"]] = row["header_image"]
            
    with open('data/original_data/steam.csv', newline='', encoding="utf8") as csvfile:

        itemCount = 0
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            oDict = OrderedDict()
            
            # Only keep rows with games that have English language
            if row["english"] == "1" and int(row["average_playtime"]) > 0 and int(row["positive_ratings"]) > 0:
                
                # Populate the custom ordered dict for the rows and cols being kept
                oDict["GameID"] = itemCount
                oDict["Name"] = row["name"].lower()
                oDict["ReleaseDate"] = row["release_date"]
                oDict["Developer"] = row["developer"].lower()
                oDict["Publisher"] = row["publisher"].lower()
                oDict["Platform"] = row["platforms"].lower()
                oDict["Genre"] = row["genres"].lower()
                oDict["Tags"] = row["steamspy_tags"].lower()
                oDict["PositiveRatings"] = row["positive_ratings"]
                oDict["NegativeRatings"] = row["negative_ratings"]
                oDict["AveragePlaytime"] = row["average_playtime"]
                oDict["Price"] = row["price"]

                # Merge the description and image from their respective dictionaries
                oDict["Description"] = descriptionDict[row["appid"]]
                oDict["Image"] = mediaDict[row["appid"]]

                #Add the cleaned row to the list of Ordered Dictionaries
                dictList.append(oDict)

                itemCount+=1
          

        print("Cleaned data set contains " + str(itemCount) + " items.")

def writeCleanedDataToCSV():
    with open('data/games_clean.csv', 'w', newline='', encoding="utf8") as csvfile:
        fieldnames = ['GameID', 'Name', 'ReleaseDate', 'Developer', 'Publisher', 'Platform', 'Genre', 'Tags', 'PositiveRatings', 'NegativeRatings', 'AveragePlaytime', 'Price', 'Description', 'Image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in dictList:
            writer.writerow(item)

def printCleanedData(dlist):
    for item in dlist:
        print(item)




