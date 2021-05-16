def sortByX1Value(coordArr, clsCheck = [0], left = [], right = [], checkForOverlap = True):
  # coordArr = [[cls, confident_score, [x1,y1,x2,y2]],...]
  x1Values = sorted([x[2][0] for x in coordArr])
  sortedCoordArr = []
  for x in x1Values:
    for y in range(len(coordArr)):
      if x == coordArr[y][2][0]:
        sortedCoordArr.append(coordArr[y])
        del coordArr[y]
        break
  if checkForOverlap:
    sortedCoordArr = removeInnerBndBox(sortedCoordArr, clsCheck = clsCheck, left = left, right = right)
  return sortedCoordArr

def sortByY1Value(coordArr):
  # coordArr = [[cls, confident_score, [x1,y1,x2,y2]],...]
  y1Values = sorted([x[2][1] for x in coordArr])
  sortedCoordArr = []
  for x in y1Values:
    for y in range(len(coordArr)):
      if x == coordArr[y][2][1]:
        sortedCoordArr.append(coordArr[y])
        del coordArr[y]
        break
  # sortedCoordArr = removeInnerBndBox(sortedCoordArr,clsCheck = 0)
  return sortedCoordArr

# create class belongings Dict
def createDict(main = None, left = [],right = [],top = [],bottom = []):
  return {
    0: main,
    1: left,
    2: top,
    3: right,
    4: bottom
  }

def findNextAlphabet(arr, index = 0, left = [], right = [],top = [],bottom=[]):
  if index + 1 >= len(arr):
    return None
  for data in arr[index + 1 : ]:
    cls = data[0]
    isNotLeft = cls not in left
    isNotRight = cls not in right
    isNotTop = cls not in top
    isNotBottom = cls not in bottom

    # if cls not in left,right,top or bottom then it must belong to the main alphabet
    if isNotLeft and isNotRight and isNotTop and isNotBottom:
      return data # [cls, confidence_score, [x1,y1,x2,y2]]
  return None

# Calculate overlapped area
def calculateOverlappedArea(rect1,rect2,img_shape = None):
  # Assuming rect1 as mainAlphabet
  img_height, img_width = img_shape if img_shape != None else (rect1[3],0)
  # rect1 = [rect1[0], 0, rect1[2], img_height if img_shape else rect1[3]]
  rect1 = [rect1[0], 0, rect1[2], 1000000] # Assuming image height won't be bigger than this
  rect2 = [rect2[0], rect2[1], rect2[2], rect2[3]]
  overlappedArea = area(rect1, rect2)

  return overlappedArea


def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    if (dx>=0) and (dy>=0):
        return dx*dy
    return 0

  
def removeInnerBndBox(coordArr, clsCheck = [0],left = [], right= [], thres = 0.2):
  if clsCheck == None:
    return coordArr
  index = []
  exceptionClass = [60,61,62]
  for i in range(len(coordArr)):
    for j in range(len(coordArr)):
      iBelongToMainClass = coordArr[i][0] in clsCheck
      # iBelongToOther = coordArr[i][0] in left or coordArr[i][0] in right
      jBelongToException = coordArr[j][0] in exceptionClass
      # jBelongToOther = coordArr[j][0] in left or coordArr[j][0] in right
      iBelongToException = coordArr[i][0] in exceptionClass
      jBelongToMainClass = coordArr[j][0] in clsCheck
      exceptionClass = [60,61,62]
      if i != j:
        mainClassCoord = coordArr[i][2]
        otherClassCoord = coordArr[j][2]
        mainClassArea = abs(mainClassCoord[0] - mainClassCoord[2]) * abs(mainClassCoord[1] - mainClassCoord[3])
        overlappedArea = area(mainClassCoord, otherClassCoord)
        ratio = overlappedArea / mainClassArea
        if ratio > 0.85:
          index.append(i)
      
  index = sorted(list(set(index)))
  i = len(index)
  while i > 0:
    del coordArr[index[i - 1]]
    i -= 1
  return coordArr

def appendToConstructedArr(constructedArr = [], value = None, left = False, right = False, top = False, bottom = False):
  # tmp = constructedArr.copy()
  if left:
    tmp = constructedArr[-1][1].copy()
    tmp.append(value)
    constructedArr[-1][1] = tmp
  elif right:
    tmp = constructedArr[-1][3].copy()
    tmp.append(value)
    constructedArr[-1][3] = tmp
  elif top:
    tmp = constructedArr[-1][2].copy()
    tmp.append(value)
    constructedArr[-1][2] = tmp
  elif bottom:
    tmp = constructedArr[-1][4].copy()
    tmp.append(value)
    constructedArr[-1][4] = tmp
  return constructedArr

def topAndBottomBelongTo(coordArr = [], index = 0, constructedArr = [], left = [], right = [], top = [], bottom = [], img_shape = None):
  # constructedArr contains the current status of word constructing
  # index is the current index for top or bottom class
  # coordArr = All detected output
  if len(coordArr) == 0:
    return constructedArr
  
  topHolder = []
  bottomHolder = []
  # find next alphabet whether this top or bottom belongs to next alphabet or the current one
  nextAlphabet = findNextAlphabet(coordArr, index, left = left, right = right, top = top, bottom = bottom)
  crntCls = coordArr[index] # [cls, confident_score, [x1,y1,x2,y2]]
  crntMainAlphabet = constructedArr[-1][0] if len(constructedArr) > 0 else None # if constructedArr already initiated
 
  if nextAlphabet == None:
    # there is no next alphabet and crntCls overlap with mainAlphabet
    # then append to the current constructedArr
    if crntMainAlphabet != None and calculateOverlappedArea(crntMainAlphabet[2], crntCls[2], img_shape = img_shape) > 0:
      top = True if crntCls[0] in top else False
      bottom = True if crntCls[0] in bottom else False
      return appendToConstructedArr(constructedArr = constructedArr, value = crntCls[0], top = top, bottom = bottom) , topHolder, bottomHolder
    # there is no next alphabet and there is no mainAlphabet
    # or crntCls does not overlap with main alphabet then create new entry 
    else:
      top = [crntCls[0]] if crntCls[0] in top else []
      bottom = [crntCls[0]] if crntCls[0] in bottom else []
      constructedArr.append(createDict(top = top, bottom = bottom))
      return constructedArr, topHolder, bottomHolder
  else:
    # there is next alphabet so calculate overlap with the crntCls
    overlapWithNextAlphabet = calculateOverlappedArea(nextAlphabet[2], crntCls[2], img_shape = img_shape)
    # there is no main alphabet and crntCls overlap with next alphabet
    # then hold the value to be added with next alphabet
    if crntMainAlphabet == None and overlapWithNextAlphabet > 0:
      topHolder = [crntCls[0]] if crntCls[0] in top else []
      bottomHolder = [crntCls[0]] if crntCls[0] in bottom else []
      return constructedArr , topHolder, bottomHolder
    # there is no main alphabet and they dont overlap
    # then create new entry
    elif crntMainAlphabet == None and overlapWithNextAlphabet < 1:
      top = [crntCls[0]] if crntCls[0] in top else []
      bottom = [crntCls[0]] if crntCls[0] in bottom else []
      constructedArr.append(createDict(top = top, bottom = bottom))
      return constructedArr, topHolder, bottomHolder
    # there is mainAlphabet then calculate overlap portion
    overlapWithCrntAlphabet = calculateOverlappedArea(crntMainAlphabet[2], crntCls[2])
    # compare both overlap
    # print(crntCls[0],overlapWithCrntAlphabet,overlapWithNextAlphabet)
    if overlapWithNextAlphabet > overlapWithCrntAlphabet:
      topHolder = [crntCls[0]] if crntCls[0] in top else []
      bottomHolder = [crntCls[0]] if crntCls[0] in bottom else []
      return constructedArr , topHolder, bottomHolder
    else:
      # if none of them overlap it will add crntCls to currentMainAlphabet
      top = True if crntCls[0] in top else False
      bottom = True if crntCls[0] in bottom else False
      return appendToConstructedArr(constructedArr = constructedArr, value = crntCls[0], top = top, bottom = bottom) , topHolder, bottomHolder
      
def constructAlphabetsBelongings(coordArr,main = [], left = [], right = [], bottom = [], top = [], img_shape = None):
  # coordArr = [[cls, confident_score, [x1,y1,x2,y2]],...]
  coordArr = sortByX1Value(coordArr, clsCheck = main, left = left, right = right) # sorting coordArr by x1 value
  leftHolder = []
  topHolder = []
  bottomHolder = []
  constructedArr = [] # for স constructed arr will be [{0: 40, 1: [], 2: [], 3: [], 4: []},...]
  for i in range(len(coordArr)):
    cls = coordArr[i][0]
    if cls in left:
      # left = ে, ৈ, ি
      # They always mean the start of a new entry. or they don't belong to anybody
      leftHolder.append(cls)
      constructedArr.append(createDict(left = [cls]))

    elif cls in right:
      # right = ী, ৗ, া, ‍্য
      # They always mean the end of a new entry or the don't belong to anybody
      # clear leftHolding
      leftHolder = []
      # if there's already and entry
      # append to it's right array
      if len(constructedArr) > 0:
        constructedArr = appendToConstructedArr(constructedArr = constructedArr, value = cls, right = True)
      # else create new entry
      else:
        constructedArr.append(createDict(right = [cls], top = topHolder, bottom = bottomHolder))
        topHolder = []
        bottomHolder = []
    
    elif cls in top:
      # top = ঁ, ‍‍র্ (ref)
      constructedArr, tTop, _  = topAndBottomBelongTo(coordArr = coordArr, index = i, constructedArr = constructedArr, left = left, right = right, top = top, bottom = bottom, img_shape = img_shape)
      if len(tTop) > 0:
        topHolder.append(tTop[0])

    elif cls in bottom:
      # bottom = ৃ (ri-kar), ু (u-kar), ূ (dirgo-u-kar), ‍‍্র (ro-fola), ‍্ (hoshonto)
      constructedArr, _, tBottom  = topAndBottomBelongTo(coordArr = coordArr, index = i, constructedArr = constructedArr, left = left, right = right, top = top, bottom = bottom, img_shape = img_shape)
      if len(tBottom) > 0:
        bottomHolder.append(tBottom[0])
    
    else:
      # main alphabet
      if len(leftHolder) > 0:
        constructedArr[-1][0] = coordArr[i]
        constructedArr[-1][2] = topHolder
        constructedArr[-1][4] = bottomHolder

        leftHolder = []
        topHolder = []
        bottomHolder = []
      else:
        constructedArr.append(createDict(main = coordArr[i], top = topHolder, bottom = bottomHolder))
        topHolder = []
        bottomHolder = []
  return constructedArr