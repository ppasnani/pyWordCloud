#!/usr/bin/python -tt

import re
import sys
import math
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
from random import randint

fileToAnalyze = "constitution.txt"

height = 512
width = 1024
scale = 3

def drawWords(sortedList, wordCount, maxWords):
    img_grey = Image.new("L", (width, height),color=0)    
    draw = ImageDraw.Draw(img_grey)
    #Draw two crossing grey lines for test
    #draw.line((0, 0) + img_grey.size, fill = 128)
    #draw.line((0, img_grey.size[1], img_grey.size[0], 0), fill = 128)
    
    #draw.text((10, 25), "world", font=font, fill="white")
    print 'max:', maxWords
    
    for word in sortedList:
        fontSize = int(math.ceil(math.log(wordCount[word], 1.3)))
        font = ImageFont.truetype("arial.ttf", fontSize * scale)
        
        location = findPlaceWord(img_grey, draw.textsize(word, font=font))
        if location is not None:            
            draw.text(location, word, font=font, fill=int((float(wordCount[word])/maxWords) * 255))
            print word, location, wordCount[word], int((float(wordCount[word])/maxWords) * 255)
        else:
            break
        
    #print draw.textsize("world", font=font)
    
    img_grey.show()

def findPlaceWord(img_grey, textSize):
    #Wherever it is 0, it should be possible to draw text
    fitText = ndimage.filters.uniform_filter(img_grey, textSize)
    #print fitText, "END\n"
    rows = len(fitText)
    columns = len(fitText[0])

    x = randint(0, columns-1)
    y = randint(0, rows-1)
    #print 'x', x, 'y', y, fitText[y][x] == 0
    if fitText[y][x] == 0:
        #and x + textSize[0] < rows
        #and  y + textSize[0] < columns
        #and fitText[y+textSize[1]][x+textSize[0]] == 0:
        #Then move left and up until we reach a non zero point
        #while fitText[y][x] == 0 and x > 0:
        #    x -= 1
        #while fitText[y][x+1] == 0 and y > 0:
        #    y -= 1
        #if x + textSize[0] < rows and y + textSize[0] < columns:
        #    if (
        return (x, y)
    else:
        #First check the same row
        for i in range(x+1, columns):
            if fitText[y][i] == 0:
                return (i, x)
        #Then check the rest of the image for the first 0
        for i in range(y+1, rows):
            for j in range(0, columns):
                if fitText[i][j] == 0:
                    return (j, i)

#Requires: A non empty string of words with spaces as tokens
#Ensures: Returns a dictionary of the number of occurences
#   of each word and a count of the total number of words    
def countWords(wordString):
    wordDict = {}
    maxWords = 0
    for word in wordString.split(' '):
        
        if word in wordDict:
            wordDict[word] += 1
            if wordDict[word] > maxWords:
                maxWords = wordDict[word]
        else:
            wordDict[word] = 1

    return (wordDict, maxWords)

#Just catch the lower case alphabets to get rid of punctuations
def filter(string):    
    regex = re.compile('[^a-z\n\s]')
    return regex.sub('', string)
    
def main():
    #Read in the file
    f = open(fileToAnalyze, 'r')
    fileString = f.read().lower()
    
    wordString = filter(fileString)
    (wordCount, maxWords) = countWords(wordString)
    sortedList = sorted(wordCount, key=lambda count: wordCount[count], reverse=True)
    #print '\n'.join(sortedList)
    drawWords(sortedList, wordCount, maxWords)

if __name__ == '__main__':
    main()
