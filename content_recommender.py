import csv
from collections import OrderedDict
from array import *

itemDict = []

def importData():
    with open('data/games_clean.csv', newline='', encoding="utf8") as csvfile:
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
            matrix[i][j] = calculateSimilarity(i,j)
                
    print("Matrix has been populated with similarity scores!")
    print("First item: " + str(matrix[0][0]))

# Calculate the similarity between two items
# and return a score between 0 and 100.
# Fields used to determine similarity are the
# Name, Genre, Tags, Platform, Publisher,
# Developer, release Year, and Description.
def calculateSimilarity(id_one, id_two):
    similarity = 0
    nameWeight = 20
    genreWeight = 15
    tagsWeight = 20
    descriptionWeight = 20
    platformWeight = 5
    publisherWeight = 5
    developerWeight = 10
    yearWeight = 5

    d1 = itemDict[id_one]
    d2 = itemDict[id_two]

    # Get the 4-digit years from the release date field
    year1 = d1["ReleaseDate"][:4]
    year2 = d2["ReleaseDate"][:4]

    # A few heuristics to help make more
    # accurate recommendations. For example, if the games
    # being compared are both Nintendo games then
    # developer should be weighted more heavily since Nintendo
    # has high brand loyalty. If the games were both made
    # before 2005, then year should be weighted more since
    # those who like an old school game tend to like
    # other old school games, etc.
    
    if(d1["Developer"] == "nintendo" and d2["Developer"] == "nintendo"):
        developerWeight += 10
        nameWeight -= 10

    if(int(year1) < 2005 and int(year2) < 2005):
        yearWeight += 10
        platformWeight -= 5
        developerWeight -= 5
    

    # Similarity calculations

    # Name Similarity
    similarity += getStringSimilarity(d1["Name"], d2["Name"], " ") * nameWeight

    # Genre Similarity
    similarity += getStringSimilarity(d1["Genre"], d2["Genre"], ";") * genreWeight

    # Tags similarity
    similarity += getStringSimilarity(d1["Tags"], d2["Tags"], ";") * tagsWeight

    # Description similarity
    similarity += getStringSimilarity(d1["Description"], d2["Description"], " ") * descriptionWeight

    # Platform similarity
    similarity += getStringSimilarity(d1["Platform"], d2["Platform"], ";") * platformWeight

    # Publisher similarity
    if(d1["Publisher"] == d2["Publisher"]):
        similarity += publisherWeight

    # Developer Similarity
    if(d1["Developer"] == d2["Developer"]):
        similarity += developerWeight

    # Release year similarity    
    yearDifference = abs(int(year1) - int(year2))    

    if(yearDifference == 0):
        similarity += yearWeight
    else:
        similarity += yearWeight * ((40 - yearDifference)) / 40
        
        
    return similarity

# Returns a number between 0 and 1 depending on how many
# words are similar out of the total number of words
def getStringSimilarity(s1, s2, seperator):
    str1 = s1.split(seperator)
    str2 = s2.split(seperator)
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
def getTopTenRecommendations(item_id, matrix):
    newRow = []
    row = matrix[item_id]

    for i in range(len(matrix)):
        newRow.append((float(row[i]), i)) 
    
    newRow.sort(reverse=True)
    topTen = []
    
    for i in range(1,11):
        topTen.append(newRow[i][1])

    #for i in topTen:
    #    print("Similarity: " + str(i[0]) + " ID: " + str(int(i[1])))
        
    return topTen
        

#Writes the similarity matrix to
#a csv file
def writeSimilarityMatrixToCSV(matrix):
    with open('data/sMatrix.csv', 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(row)
            
#Reads similarity matrix from csv
def readSimilarityMatrixFromCSV():
    matrix = []
    with open('data/sMatrix.csv', 'r', newline='', encoding='utf8') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            matrix.append(row)
    return matrix

#Write top ten recs for each game to CSV file for easy retrieval
def writeTopTenRecsToCSV(matrix):
    with open('data/topTenRecs.csv', 'w', encoding='utf8', newline='') as file:
        itemID = 0
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(getTopTenRecommendations(itemID, matrix))
            itemID+=1

#Imports the top ten recs from the csv file into a dictionary
def importTopTenFromCSV():
    topTenDict = {}
    topTenList = []
    itemID = 0
    with open('data/topTenRecs.csv', 'r', newline='', encoding='utf8') as file:
        reader = csv.reader(file)
        for row in reader:
            topTenDict[itemID] = row
            itemID+=1
    return topTenDict
