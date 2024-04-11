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

# Apply the custom function row-wise to create column 
precisions = []
recalls = []
f1_scores = []

for i in range(len(answer_df)):
    print("  ")
    print("## Unique Item " , i)

    data = {'brand1': [answer_df['brand'].iloc[i]]* len(answer_df),
            'item1': [answer_df['name'].iloc[i]]* len(answer_df), # generate target item multiple times
            'brand2': answer_df['brand'],
            'item2': answer_df['name']}
    test_df = pd.DataFrame(data)
    
    # search same items in testcase
    #test_df['answer'] = test_df.apply(lambda row: check_same_item_v5(row), axis=1)
    result = test_df.apply(lambda row: check_same_item_v10(row), axis=1)
    test_df['answer'] = result.apply(lambda x: x[0])
    
    # evaluation
    pre = test_df['answer'].to_list()
    print(i)
    _, df = select_names_with_same_group(answer_df, answer_df['name'].iloc[i])
    act = df['actual'].to_list() 

    test_df['actual'] = act
    test_df['result_detail'] = result.apply(lambda x: x[1])
    
    # store result
    p, r, f1 = compute_metrics(pre,act)
    precisions.append(p)
    recalls.append(r)
    f1_scores.append(f1)
    
    # generate csv
    test_df = test_df.sort_values(by='actual',ascending=False)
    filename = f'./0411/algo10/pooppad_{i}.csv'  # Construct filename with increment
    test_df.to_csv(filename, index=False, encoding='utf-8-sig') 

print(" ")
print(" ")
print("**--------Search within a whole Brnad is Done !---------**")

data = {'item': answer_df['name'],
        'precision': precisions,
        'recalls': recalls,
        'f1_scores': f1_scores}

evaluation_df = pd.DataFrame(data)
evaluation_df = evaluation_df.sort_values(by='f1_scores',ascending=False)
filename = f'./0411/pooppad_eval_algo10.csv'  # Construct filename with increment
evaluation_df.to_csv(filename, encoding='utf-8-sig') 
