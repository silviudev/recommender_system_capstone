
import data_cleaning as clean
import content_recommender as cRecommender


#cRecommender.printData()

entry = ""
matrix = []

while entry.lower() != "exit":
     print("Select an action: ")
     print("1. Import and clean data and write to CSV")
     print("2. Print all data from cleaned CSV")
     print("3. Create and populate similarity matrix")
     print("4. Get similiartiy of two items by ID")
     print("5. Write similarity matrix to file")
     print("6. Read in similarity matrix from file")
     print("7. Get top 10 recommendations by ID")
     print("8. Write top 10 recommendations to CSV")
     
     entry = input()

     if(entry == "1"):
          clean.importAndCleanData()
          clean.writeCleanedDataToCSV()
     elif(entry == "2"):
          clean.printCleanedData(dictList)
     elif(entry == "3"):
          cRecommender.importData()
          cRecommender.createSimilarityMatrix()
          cRecommender.populateSimilarityMatrix()
     elif(entry == "4"):
          num = input("Enter First ID: ")
          id1 = int(num)
          num = input("Enter Second ID: ")
          id2 = int(num)
          print(cRecommender.getSimilarity(id1,id2))
     elif(entry == "5"):
          cRecommender.writeSimilarityMatrixToCSV()
     elif(entry=="6"):
          matrix = cRecommender.readSimilarityMatrixFromCSV()
     elif(entry=="7"):
          num = input("Enter item ID: ")
          cRecommender.getTopTenRecommendations(int(num), matrix)
     elif(entry=="8"):
          cRecommender.writeTopTenRecsToCSV(matrix)
