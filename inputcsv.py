import csv
import pandas as pd

def judgePrice(price):
    for j in range(len(price)):
        if(price[j].isdigit()): return True
        if(j == len(price) - 1): return False

def countComma(price):
    commaCounter = 0
    for char in price:
        if char == ',': commaCounter += 1
    return commaCounter

def countPoint(price):
    pointCounter = 0
    for char in price:
        if char == '.': pointCounter += 1
    return pointCounter

def extractPrice(price):
    firstIndex = 0
    lastIndex = 0
    for i in range(len(price)):
        if price[i] != ' ':
            if i == 0 or price[i - 1] == ' ':
                firstIndex = i
            if i == len(price) - 1 or price[i + 1] == ' ':
                lastIndex = i
                break

    newPrice = price[firstIndex:lastIndex+1]
    pointNum = countPoint(newPrice)
    commaNum = countComma(newPrice)

    if pointNum == 1 and commaNum == 0:
        return newPrice
    elif pointNum == 0 and commaNum == 1:
        for char in newPrice:
            if char == ',':
                index = newPrice.index(char)
                newPrice = newPrice[:index] + '.' + newPrice[index+1:]
                return newPrice
    elif pointNum == 1 and commaNum == 1:
        for char in newPrice:
            if char == ',':
                commaIndex = newPrice.index(char)
                return newPrice[:commaIndex] + newPrice[commaIndex + 1:]
    else: return newPrice

def calculateAverage(prices):
    sum = 0
    for price in prices:
        sum += price
    average = sum/len(prices)
    return average

def searchMedian(prices):
    if(len(prices) & 2 == 0):
        return prices[len(prices) // 2]
    else:
        return prices[(len(prices) - 1) // 2]

def execute(file):
    csv_reader = csv.reader(open(file))
    prices = []
    for line in csv_reader:
        price = line[1]
        if(judgePrice(price)):
            print("--Model:", line[0], " ", "--Purchase link:", line[2])
            realPrice = extractPrice(price)
            prices.append(float(realPrice))

    prices.sort()

    result = []
    result.append(str(calculateAverage(prices)))
    result.append(str(searchMedian(prices)))
    productspd = pd.DataFrame(result)
    productspd.to_csv('results.csv', index=False)

    print("Average price is:", calculateAverage(prices), "dollars.")
    print("The median of prices is:", searchMedian(prices), "dollars.")

execute("./Samsung s10 output.csv")

