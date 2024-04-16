import json
import pandas as pd

import sys
sys.path.append('./code')

from load_data import *
from item_mapping import *
from matching_algo import *


def load_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config

def main():
    # Load config
    config = load_config('config.json')
    
    # Load data
    answer_df = pd.read_csv(config['import_path'])

    # Apply the custom function row-wise to create columns
    precisions = []
    recalls = []
    f1_scores = []

    for i in range(len(answer_df)):
        print("  ")
        print("## Unique Item ", i)

        data = {'brand1': [answer_df['brand'].iloc[i]]*len(answer_df),
                'item1': [answer_df['name'].iloc[i]]*len(answer_df),  # generate target item multiple times
                'brand2': answer_df['brand'],
                'item2': answer_df['name']}
        test_df = pd.DataFrame(data)

        # Apply custom function and evaluate
        result = test_df.apply(lambda row: check_same_item_v10(row), axis=1)
        test_df['answer'] = result.apply(lambda x: x[0])
        _, df = select_names_with_same_group(answer_df, answer_df['name'].iloc[i])
        act = df['actual'].to_list()
        test_df['actual'] = act
        test_df['result_detail'] = result.apply(lambda x: x[1])

        # Compute metrics
        p, r, f1 = compute_metrics(test_df['answer'].to_list(), act)
        precisions.append(p)
        recalls.append(r)
        f1_scores.append(f1)

        # Generate and save CSV
        test_df = test_df.sort_values(by='actual', ascending=False)
        filename = f"{config['export_folder']}_{i}.csv"
        test_df.to_csv(filename, index=False, encoding='utf-8-sig')

    print(" ")
    print(" ")
    print("**--------Search within a whole Brand is Done!---------**")

    # Save evaluation results to CSV
    evaluation_df = pd.DataFrame({'item': answer_df['name'],
                                  'precision': precisions,
                                  'recalls': recalls,
                                  'f1_scores': f1_scores})
    evaluation_df = evaluation_df.sort_values(by='f1_scores', ascending=False)
    filename = f"{config['evaluation_export_path']}.csv"
    evaluation_df.to_csv(filename, encoding='utf-8-sig')

if __name__ == "__main__":
    main()