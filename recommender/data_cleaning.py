import csv
from collections import OrderedDict

dictList = []

def importAndCleanData():
    
    itemCount = 0
    
    with open('data/vg_sales_original.csv', newline='', encoding="utf8") as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            oDict = OrderedDict()
            score = 0
            
            # Only keep rows with either a user and/or critic score present
            if (row["User_Score"] != "" or row["Critic_Score"] != "") and row["Year"] != "":

                itemCount+=1
                
                # Populate the custom ordered dict for the rows and cols being kept
                oDict["GameID"] = str(itemCount)
                oDict["Name"] = row["Name"].lower()
                oDict["Genre"] = row["Genre"].lower()
                oDict["ESRB"] = row["ESRB_Rating"].lower()
                oDict["Platform"] = row["Platform"].lower()
                oDict["Publisher"] = row["Publisher"].lower()
                oDict["Developer"] = row["Developer"].lower()

                # Score rating will be average of user and critic score
                # if both are present, otherwise will be whichever one
                # is present
                if row["User_Score"] == "":
                    score = row["Critic_Score"]
                elif row["Critic_Score"] == "":
                    score = row["User_Score"]
                else:
                    score = (float(row["Critic_Score"]) + float(row["User_Score"])) / 2

                oDict["Score"] = str(score)

                oDict["Year"] = row["Year"][:4]
                
                if len(oDict["Year"]) != 4:
                    raise ValueError('ERROR: Year on line ' + str(row["Rank"]) + " is not four digits.")
            
                oDict["URL"] = row["img_url"]

                #Add the cleaned row to the list of Ordered Dictionaries
                dictList.append(oDict)
          

        print("Cleaned data set contains " + str(itemCount) + " items.")

def writeCleanedDataToCSV():
    with open('data/games.csv', 'w', newline='', encoding="utf8") as csvfile:
        fieldnames = ['GameID', 'Name', 'Genre', 'ESRB', 'Platform', 'Publisher', 'Developer', 'Score', 'Year', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in dictList:
            writer.writerow(item)

def printCleanedData(dlist):
    for item in dlist:
        print(item)




