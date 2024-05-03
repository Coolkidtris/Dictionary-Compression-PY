import re                                                                   # Import necessary modules
import os
import math
import json

keyToCompress = ""                                                          # Key that will be used in the dictionary
keyCounter = 0                                                              # Current number that will be the Key

def compress(fileName):                                                     # Function that takes a file path/name 
    global keyToCompress, keyCounter                                        # Make our two variables global

    compressDict = {}                                                       # Dictionary to used to compress

    file = open(fileName, mode="r")                                         # Open our file
    fileContents = re.split(r"[ |,|:|\n]", file.read().replace(".","").replace("(","").replace(")","").replace("!","").lower())
    file.close()                                                            # Close our file
    
    for item in fileContents:                                               # Loop through the file contents
        if item not in compressDict:                                        # If the item is not already in the dictionary
            compressDict[item] = hex(keyCounter)[2:]                        # Insert the item into the dictionary, and set its value to the Hex value of the current counter
            keyCounter+=1                                                   # Increment the counter
    
    newFileToCompress = open(f"${fileName}", mode="w")                      # Create a new file, which stores our compressed contents
    for wordToReplace in fileContents:                                      # Loop through the current contents in the uncompressed file
        wordToReplace = compressDict[wordToReplace]+" "                     # Replace the current word with its compressed variant (in Hex)
        newFileToCompress.write(str(wordToReplace))                         # Write the new word to the new, compressed file
    newFileToCompress.close()                                               # Close our new file

    compressDict = dict((v,k) for k,v in compressDict.items())              # Reverse the contents of our dictionary, so it can be used for decompression

    dictFile = open(f"${fileName}.JSON", mode="w")                          # Create a new JSON file to store our dictionary so we can decompress the file
    json.dump(compressDict, dictFile)                                       # Dump our dictionary into the JSON file
    dictFile.close()                                                        # Close the JSON file.

def decompress(fileToDecompress):                                           # Function to decompress files, also takes a file path/name as a parameter
    file = open(fileToDecompress, mode="r")                                 # Open the file to read
    jsonContents = open(f"{fileToDecompress}.JSON", mode="r")               # Open the JSON file
    fileContents = file.read().split(" ")                                   # Get our file contents

    newFileContents = open(f"{fileToDecompress[1:]}", mode="w")             # Recreate the original file
    newDict = json.load(jsonContents)                                       # Create a dictionary from the JSON file

    for item in fileContents:                                               # Loop through the contents of our compressed file
        if item in newDict:                                                 # If the item is in the dictionary containing compressed keys
            newFileContents.write(f"{newDict[item]} ")                      # Write the decompressed value to the decompressed file
    file.close()                                                            # Close the original, compressed file
    jsonContents.close()                                                    # Close the JSON file

    os.remove(f"{fileToDecompress}")                                        # Remove the compressed file as its no longer needed
    os.remove(f"{fileToDecompress}.JSON")                                   # Remove the JSON file

    newFileContents.close()                                                 # Close our new, decompressed file
    
def main():                                                                 # Main entry point
    
    compressOrDecompress = input("Would you like to compress or decompress a file?\n>") # Ask if the user wants to compress or decompress

    if compressOrDecompress.lower() == "compress":                          # If the user wants to compress
        fileToCompress = input("Enter your file name!\n>")                  # Ask for the file name/path
        compress(fileToCompress)                                            # Compress
        os.remove(fileToCompress)                                           # Remove the original file

    elif compressOrDecompress.lower() == "decompress":                      # Otherwise, if its to decompress
        fileToDecompress = input("Enter your file name!\n>")                # Ask for file name/path
        decompress(f"${fileToDecompress}")                                  # Decompress the file
 
if __name__ == '__main__':
    main()

