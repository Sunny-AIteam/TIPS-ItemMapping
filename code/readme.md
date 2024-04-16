### Current logic of Matching algorithm

* split words by space 


1. Brand
- assume all item has brand as meta data.
- check brand name first : if they are not matching, they are different items.

2. Units (매수)
- detect unit by keywords such as '매', 'P', 'ea' then drop out noise.
- if both exists but different (not a multiple relation), then they are different items.
- if they are multiples or one of it is missing, move to next steps.
  ```python
  for w in item:
        if any(char.isdigit() for char in w) and (('매' in w) or ('p' in i.lower()) or ('ea' in w.lower())): 
            amount = []
            for index, char in enumerate(i):
                if char.lower() == 'x' and index >= 2: # todo: 좀더 다양한 경우 고려해서 regex로 디테일하게 거르기
                    break
                if char.isdigit():
                    amount.append(char)
            amount1 = int(''.join(amount))
            break
        else :
            amount = None
  ```
3. Quantity (중량)
- detect quantity by keywords such as 'g'.
- if both exists and match, then they are same items.
- if only one has information, then they are different items.
- when both do not has this info, move to next steps.
```python3
 for i in item1:
        if any(char.isdigit() for char in i) and 'g' in i: 
            quant1 = i
            break
        else :
            quant1 = None

 if (quant1 and quant2):
        print(quant1, quant2)
        if quant1 != quant2 :
            # 중량 정보가 하나만 있으면 서로 다른 상품 (매치 불가하므로 F처리)
            return "F" , {'중량1' : quant1, '중량2': quant2}
        else :
            # 중량이 둘다 존재하고 일치할때, 많은 브랜드의 경우 중량 == 상품라인이므로 True (정직한패드)
            print('Match by gram !')
            return "T",  {'중량1' : quant1, '중량2': quant2}
```

4. Size (크기)
- size keywords are already defiend in dictionary
- if both exists but they are different, then they are different items
```python3
for i in item1: 
        if i in size_units:
            sizeunit1 = i
            size1 = size_units[i]
            break
        else:
            sizeunit1 = ""
            size1  = None

if (((size1) and (size2)) and (size1 != size2)) : # 사이즈 정보가 없으면 g으로 구분 => 사이즈값이 존재하고 둘이 다를때만 다른상품
        return "F"
```
5. Text  
   => _when filter out unit, quantity, and so on, precision increase (P:80, R:59, F1: 63)_  
   => _when comparing original text without stopwords, recall increase (P:70, R:65, F1:61)_
- if item has more than 3 words, drop out stopwords
- then compute fuzzy matching score
- if score is over 50, they are the same items
  
```python3
from fuzzywuzzy import fuzz

if len(item1) > 3: 
        for i in filtered_item1 :
            if i not in top_1st : 
                seq1 += i
    else :
        seq1 = (' ').join(filtered_item1)

similarity = fuzz.ratio(seq1.upper(), seq2.upper())

if similarity > 49 :
  return "T" 

```
