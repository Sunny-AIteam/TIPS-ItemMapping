from fuzzywuzzy import fuzz

#config
size_units = {
    'XS' : 0,
    '소형' : 1,
    '소형패드' : 1,
    'S' : 1,
    # '40 x 50': 1 ,
    '중형' : 2,
    'M' : 2,
    '대형' : 3,
    '대형패드' : 3,
    'L' : 3, 
    '특대형' : 4,
    '초대형' : 4,
    '초대형패드' : 4,
    'XL': 4,
    'XXL': 5
}

### ALGO 10 : 9 + 스트링 매치시 매수랑 사이즈 제거하지 말아보기 

def retreive_amount(item):
    for i in item:
        if any(char.isdigit() for char in i) and (('매' in i) or ('p' in i.lower()) or ('ea' in i.lower())): 
            amount = []
            for index, char in enumerate(i):
                if char.lower() == 'x' and index >= 2: # Modify to select the first one after splitting in the relevant unit
                    break
                if char.isdigit():
                    amount.append(char)
            amount = int(''.join(amount))
            break
        else:
            amount = None
    return amount

def retreive_quant(item):
    for i in item:
        if any(char.isdigit() for char in i) and 'g' in i:
            quant = i
            break
        else:
            quant = None
    return quant

def retreive_size(item, size_units):
    for i in item:
        if i in size_units:
            sizeunit = i
            size = size_units[i]
            break
        else:
            sizeunit = ""
            size = None
    return sizeunit, size

def get_seq(item, top_1st):
    filtered_item = []
    seq = ''

    if len(item) > 3: 
        for i in filtered_item:
            if i not in top_1st: 
                seq += i
    else:
        seq = ' '.join(filtered_item)

    return seq

def check_same_item(row): 

    item1 = row['item1'].split()
    item2 = row['item2'].split()
    brand1 = row['brand1']
    brand2 = row['brand2']

    #### === 0. Check brand ==================================================================
    if brand1 != brand2 :
            res = 'different brand'
            return 'F', res

    #### === 1. check the unit ==> 배수일 경우 같은 아이템으로 ==================================
    amount1 = retreive_amount(item1)
    amount2 = retreive_amount(item2)

    if amount1 != amount2 :
        # if 매수가 두개가 존재하는데 배수가 아닐경우 다른 아이템, 함수 종료
        if ((amount1 and amount2)):
            large = max(amount1, amount2)
            small = min(amount1, amount2)
            if (large % small != 0):
                return "F" , {'매수1' : amount1, '매수2': amount2}
        # else 매수 정보가 하나라도 없거나, 둘다없거나, 두개가 일치할 경우 다음 스텝
    
    ### === 2. check the quantity (gram) ==> 그램 정보가 둘다 존재하면 하드하게 분류하고 종료 ==========
    quant1 = retreive_quant(item1)
    quant2 = retreive_quant(item1)

    if (quant1 and quant2):
        if quant1 != quant2 :
            # 중량 정보가 하나만 있으면 서로 다른 상품 (매치 불가하므로 F처리)
            return "F" , {'중량1' : quant1, '중량2': quant2}
        else :
            # 중량이 둘다 존재하고 일치할때, 많은 브랜드의 경우 중량 == 상품라인이므로 True (정직한패드)
            return "T",  {'중량1' : quant1, '중량2': quant2}
        
    ### ===== 3. check the size ========================================================================
    sizeunit1, size1 = retreive_size(item1)
    sizeunit2, size2 = retreive_size(item2)

    #if (size1 != size2) : 사이즈와 g을 유니크하게
    if (((size1) and (size2)) and (size1 != size2)) : # 사이즈 정보가 없으면 g으로 구분 => 사이즈값이 존재하고 둘이 다를때만 다른상품
        return "F" , {'사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    
    ### ===== 4. check text =============================================================================
    # text preprocessing before text matching computing
    ## remove brand name 
    ## remove all numeric values

    seq1 = get_seq(item1)
    seq2 = get_seq(item2)

    similarity = fuzz.ratio(seq1.upper(), seq2.upper())

    if similarity > 49 :
        return "T" , {'seq1' : seq1, 'seq2': seq2, 'sim': similarity, '사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    else : 
        return "F" , {'seq1' : seq1, 'seq2': seq2, 'sim': similarity, '사이즈1' : size1, '사이즈2': size2, '중량1' : quant1, '중량2': quant2, '매수1' : amount1, '매수2': amount2}
    

