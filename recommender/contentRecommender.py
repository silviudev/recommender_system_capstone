import csv
from collections import OrderedDict
from array import array

matrix = []
itemDict = []

def importData():
    with open('data/games.csv', newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            itemDict.append(row)
            
def printData():
    print(len(itemDict))
    for item in itemDict:
        print(item)

def createSimilarityMatrix():
    # Create a 2D Matrix of N x N, where N is the number of data items
    n = len(itemDict)
    print("Creating empty similarity matrix of " + str(n) + " X " + str(n) + " items.")

    for i in range(n):
        matrix.append([])
        for j in range(n):
            matrix[i].append(0)
    print("Empty matrix representing " + str(n) + " X " + str(n) + " items created.")

# Populate the matrix with similarity scores
def populateSimilarityMatrix():
    print("Populating matrix with similarity scores")
    n = len(itemDict)

    for i in range(n):
        if i == round(0.9 * n):
            print ("90% Complete!")
        elif i == round(0.8 * n):
            print("80% Complete")
        elif i == round(0.6666 * n):
            print("66% Complete")
        elif i == round(0.5 * n):
            print("50% Complete")
        elif i == round(0.3333 * n):
            print("33% Complete")
        elif i == round(0.25 * n):
            print("25% Complete")
        elif i == round(0.1 * n):
            print("10% Complete")
        
        for j in range(n):
            if(i == j):
                matrix[i][j] = 100
            else:
                matrix[i][j] = calculateSimilarity(i,j)
                
    print("Matrix has been populated with similarity scores")
    print(matrix[0][1])

# Calculate the similarity between two items
# and return a score between 0 and 100.
# Fields used to determine similarity are the
# Name, Genre, ESRB rating, Platform, Publisher,
# Developer,and Year.
def calculateSimilarity(id_one, id_two):
    similarity = 0
    nameWeight = 30
    genreWeight = 20
    esrbWeight = 5
    platformWeight = 10
    publisherWeight = 10
    developerWeight = 15
    yearWeight = 10

    d1 = itemDict[id_one]
    d2 = itemDict[id_two]

    # A few heuristics to help make more
    # accurate recommendations. For example, if the games
    # being compared are both Nintendo games then
    # developer should be weighted more heavily since Nintendo
    # has high brand loyalty. If the games are both console games,
    # then platform should be weighted more heavily
    # and year less heavily. If the games were both made
    # before 1990, then year should be weighted more since
    # those who like an old school game tend to like
    # other old school games, etc.
    
    if(d1["Developer"] == "nintendo" and d2["Developer"] == "nintendo"):
        developerWeight += 10
        nameWeight -= 10

    consoles = ["ps", "ps2", "ps3", "ps4", "x360", "xone", "ns", "wii", "nes", "snes"]
    if(d1["Platform"] in consoles and d2["Platform"] in consoles):
        platformWeight +=  12
        publisherWeight-= 5
        yearWeight-= 4
        esrbWeight -= 3

    if(int(d1["Year"]) < 1990 and int(d2["Year"]) < 1990):
        yearWeight += 12
        platformWeight -= 5
        developerWeight -= 5
        esrbWeight -= 2
    

    #Similarity calculations

    similarity += getStringSimilarity(d1["Name"], d2["Name"]) * nameWeight

    if(d1["Genre"] == d2["Genre"]):
        similarity += genreWeight

    if(d1["ESRB"] == d2["ESRB"] and d1["ESRB"] != "" and d2["ESRB"] != ""):
        similarity += esrbWeight

    if(d1["Platform"] == d2["Platform"]):
        similarity += platformWeight

    if(d1["Publisher"] == d2["Publisher"]):
        similarity += publisherWeight

    if(d1["Developer"] == d2["Developer"]):
        similarity += developerWeight
        
    yearDifference = abs(int(d1["Year"]) - int(d2["Year"]))    

    if(yearDifference == 0):
        similarity += yearWeight
    else:
        similarity += yearWeight * ((40 - yearDifference)) / 40
        
        
    return similarity

# Returns a number between 0 and 1 depending on how many
# words are similar out of the total number of words
def getStringSimilarity(s1, s2):
    str1 = s1.split()
    str2 = s2.split()
    totalWords = len(str1) + len(str2)
    common = set()
    commonCount = 0
    
    for word in str1:
        common.add(word)

    for word in str2:
        if word in common:
            commonCount+=2

    return commonCount / totalWords

# Gets the similarity between two items
# from the populated similarity matrix
def getSimilarity(id1, id2):
    return matrix[id1][id2]

# Get the top 10 items based on similarity score
# for a given item
def getTopTenRecommendations(item_id):
    row = matrix[item_id]

    for i in range(len(matrix)):
        row[i] = (float(row[i]), i) 
    
    row.sort(reverse=True)
    topTen = []

    for i in range(10):
        topTen.append(row[i])

    for i in topTen:
        print("Similarity: " + str(i[0]) + " ID: " + str(int(i[1] + 1)))
        
    return topTen
        

#Writes the similarity matrix to
#a csv file
def writeSimilarityMatrixToCSV():
    with open('data/sMatrix.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(row)
            
#Reads similarity matrix from csv
def readSimilarityMatrixFromCSV():
    global matrix;
    matrix = [];
    
    with open('data/sMatrix.csv', newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append(row)

    print(matrix[0][0])
