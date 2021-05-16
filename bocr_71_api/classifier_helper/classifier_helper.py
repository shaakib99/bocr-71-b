def extractWordFromOutput(clsArr, classes= []):
    string = ''
    if len(clsArr) == 0:
      return string
    for cls in clsArr:
        tmpStr = ''
        # check special case for ref
        # ref belong to top. top class = 2
        if cls[2] != None and 66 in cls[2]: # 66 is the index number of ref
            tmpStr = classes[66] + tmpStr
        
        # main cls: 0
        if cls[0] != None:
            tmpStr += classes[cls[0][0]]
        
        # bottom: 4
        for b in cls[4]:
            tmpStr += classes[b]
        
        # right : 3
        for r in cls[3]:
            if classes[r] == 'া' and len(tmpStr) > 1 and tmpStr[-1] == 'অ':
                tmp = tmStr[:-1]
                tmpStr = tmpStr[-1]
                tmpStr = 'আ'
                tmpStr = tmp + tmpStr
            elif classes[r] == 'া' and len(tmpStr) == 1 and tmpStr[0] == 'অ':
                tmpStr = 'আ'
            else:
                tmpStr += classes[r]
        # top : 2
        for t in cls[2]:
            if t != 66:
                tmpStr += classes[t]
        
        # left : 1
        for l in cls[1]:
            tmpStr += classes[l]

        string += tmpStr
    return string