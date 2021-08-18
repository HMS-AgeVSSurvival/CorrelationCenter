import argparse
import sys

import pandas as pd

from residual import DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN
from correlation import TARGETS, ALGORITHMS, RANDOM_STATES


def feature_importances_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Store the feature importances"
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category.",
        choices=["examination", "laboratory", "questionnaire"],
        required=True,
    )
    parser.add_argument("-c", "--category", help="Name of the category.", required=True)
    args = parser.parse_args(argvs)
    print(args)
        
    store_feature_importances(args.main_category, args.category)



def store_feature_importances(main_category, category):
    data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

    folds = data["fold"].drop_duplicates().dropna().astype(int)

    data.drop(columns=data.columns[data.columns.str.startswith("prediction") | data.columns.str.startswith("residual") | data.columns.str.startswith("survival") | data.columns.isin([DEATH_COLUMN, FOLLOW_UP_TIME_COLUMN, "fold"])], inplace=True)
    data.drop(index=data.index[~data.index.astype(str).str.startswith("feature_importances")], inplace=True)

    feature_importances = pd.DataFrame(None, columns=["feature_importances", "std"], index=pd.MultiIndex.from_product((TARGETS, ALGORITHMS, RANDOM_STATES, data.columns), names=["target", "algorithm", "random_state", "predictors"]))
    
    for target in TARGETS:
        for algorithm in ALGORITHMS:
            for random_state in RANDOM_STATES:
                feasibility = [f"feature_importances_{target}_{algorithm}_{random_state}_{fold}" in data.index for fold in folds]
                feasibility += [f"feature_importances_{target}_{algorithm}_{random_state}_train" in data.index]
                if all(feasibility):
                    feature_importances.loc[(target, algorithm, random_state, data.columns), "feature_importances"] = data.loc[f"feature_importances_{target}_{algorithm}_{random_state}_train"].values
                    feature_importances.loc[(target, algorithm, random_state, data.columns), "std"] = data.loc[[f"feature_importances_{target}_{algorithm}_{random_state}_{fold}" for fold in folds]].std().values

    feature_importances.reset_index().to_feather(f"data/feature_importances/{main_category}/{category}.feather")