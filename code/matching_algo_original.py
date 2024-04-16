from fuzzywuzzy import fuzz

### ALGO 10 : 9 + 스트링 매치시 매수랑 사이즈 제거하지 말아보기 
def check_same_item_v10(row): 
    print('================================================================================')
    print(row['item1'], 'vs',  row['item2'])
    item1 = row['item1'].split()
    item2 = row['item2'].split()
    brand1 = row['brand1']
    brand2 = row['brand2']

    #### === Check brand
    if brand1 != brand2 :
            print('different brand :( terminate immediately!')
            res = 'different brand'
            return 'F', res

    #### === 0. check the unit ==> 배수일 경우 같은 아이템으로 
    for i in item1:
        
        
        if any(char.isdigit() for char in i) and (('매' in i) or ('p' in i.lower()) or ('ea' in i.lower())): 
            amount1 = []
            for index, char in enumerate(i):
                if char.lower() == 'x' and index >= 2: # 해당유닛에서 스필릿후 첫번째 고르기 로 수정 
                    break
                if char.isdigit():
                    amount1.append(char)
            amount1 = int(''.join(amount1))
            break
        else :
            amount1 = None

    for i in item2:
        if any(char.isdigit() for char in i) and (('매' in i) or ('p' in i.lower()) or ('ea' in i.lower())): 
            amount2 = []
            for index, char in enumerate(i):
                if char.lower() == 'x' and index >= 2:
                    break
                if char.isdigit():
                    amount2.append(char)
            amount2 = int(''.join(amount2))
            break
        else :
            amount2 = None

    print('매수: ', amount1, amount2)
    if amount1 != amount2 :
        # 매수가 두개가 존재하는데 배수가 아닐경우 다른 아이템, 함수 종료
        if ((amount1 and amount2)):
            large = max(amount1, amount2)
            small = min(amount1, amount2)
            if (large % small != 0):
                return "F" , {'매수1' : amount1, '매수2': amount2}
    ## 매수 정보가 하나라도 없거나, 둘다없거나, 두개가 일치할 경우 다음 스텝
    
    ### ===== 1. check the quantity (gram) ==> 그램 정보가 둘다 존재하면 하드하게 분류하고 종료
    for i in item1:
        if any(char.isdigit() for char in i) and 'g' in i: 
            quant1 = i
            break
        else :
            quant1 = None

    for i in item2:
        if any(char.isdigit() for char in i) and 'g' in i: 
            quant2 = i
            break
        else:
            quant2 = None

    print('중량: ', quant1, quant2)
    if (quant1 and quant2):
        print(quant1, quant2)
        if quant1 != quant2 :
            # 중량 정보가 하나만 있으면 서로 다른 상품 (매치 불가하므로 F처리)
            return "F" , {'중량1' : quant1, '중량2': quant2}
        else :
            # 중량이 둘다 존재하고 일치할때, 많은 브랜드의 경우 중량 == 상품라인이므로 True (정직한패드)
            print('Match by gram !')
            return "T",  {'중량1' : quant1, '중량2': quant2}
        
    # 중량 정보가 없으면 사이즈와 텍스트로 비교
    # ===== 2. check the size 
    for i in item1: 
        if i in size_units:
            sizeunit1 = i
            size1 = size_units[i]
            break
        else:
            sizeunit1 = ""
            size1  = None
    for i in item2: 
        if i in size_units:
            sizeunit2 = i
            size2 = size_units[i]
            break
        else:
            sizeunit2 = ""
            size2 = None
    print('크기: ', size1, size2)

    #if (size1 != size2) : 사이즈와 g을 유니크하게
    if (((size1) and (size2)) and (size1 != size2)) : # 사이즈 정보가 없으면 g으로 구분 => 사이즈값이 존재하고 둘이 다를때만 다른상품
        return "F" , {'사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    
    # text preprocessing before text matching computing
    ## remove brand name 
    ## remove all numeric values
    filtered_item1 = item1 #[]
    filtered_item2 = item2 #[]

    '''
    for i in item1:
        if not( any(char.isdigit() for char in i) or (brand1 in i) or (i == sizeunit1) or (i in ['배변패드', '강아지', '강아지패드', '배변용품']) ) : 
            filtered_item1.append(i)
    for j in item2:
        if not( any(char.isdigit() for char in j) or (brand1 in j)  or (j == sizeunit2) or (j in ['배변패드', '강아지', '강아지패드', '배변용품']) ) : 
            filtered_item2.append(j)
    '''
    
    # 3. compute similarity of core words by fuzzy matching
    ## filter out quant1, quant2, size1, size2, numneric value + unit, word in noise dictionary 
    ## top & bottom words (word in total group vs brand group)
    seq1 = ''
    seq2 = ''

    if len(item1) > 3: 
        for i in filtered_item1 :
            if i not in top_1st : 
                seq1 += i
    else :
        seq1 = (' ').join(filtered_item1)

    if len(item2) > 3: 
        for j in filtered_item2 :
            if j not in top_1st:
                seq2 += j
    else :
        seq2 = (' ').join(filtered_item2)

    similarity = fuzz.ratio(seq1.upper(), seq2.upper())
    print('seq1 : ', seq1)
    print('seq2 : ', seq2)
    print('similarity : ', similarity)

    if similarity > 49 :
        print("MAtch!")
        return "T" , {'seq1' : seq1, 'seq2': seq2, 'sim': similarity, '사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    else : 
        return "F" , {'seq1' : seq1, 'seq2': seq2, 'sim': similarity, '사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    