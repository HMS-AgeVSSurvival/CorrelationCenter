import argparse
import sys
import os

import pandas as pd

from residual import AGE_COLUMN, GENDER_COLUMN


def residual_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to merge the dumps with the data and to compute the residual from the predictions"
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

    data = merge_data_dumps(args.main_category, args.category)
    compute_residual(data, args.main_category, args.category)


def merge_data_dumps(main_category, category):
    data = pd.read_feather(f"../TrainingCenter/data/{main_category}/{category}.feather").set_index("SEQN")

    for target in ["age", "all", "cvd", "cancer"]:
        for algorithm in ["elastic_net", "light_gbm"]:
            for random_state in [1, 2]:
                path_dump = f"../TrainingCenter/dumps/prediction/{target}/{main_category}/{category}/{algorithm}_{random_state}.feather"
                
                if os.path.exists(path_dump):
                    dump = pd.read_feather(path_dump).set_index("SEQN")
                    data.loc[dump.index, dump.columns] = dump
                
                if os.path.exists(path_dump.replace("prediction", "feature_importances")):
                    dump = pd.read_feather(path_dump.replace("prediction", "feature_importances")).set_index("index").T   
                    for dump_index in dump.index:
                        data.loc[dump_index] = dump.loc[dump_index]
            
            if os.path.exists(path_dump.replace("prediction", "feature_importances").replace("2", "train")):
                dump = pd.read_feather(path_dump.replace("prediction", "feature_importances").replace("2", "train")).set_index("index").T
                for dump_index in dump.index:
                    data.loc[dump_index] = dump.loc[dump_index]

    return data


def compute_residual(data, main_category, category):
    raw_data = data.copy()

    data.drop(columns=data.columns[~(data.columns.str.startswith("prediction") | data.columns.isin([AGE_COLUMN, GENDER_COLUMN]))], inplace=True)
    data.drop(index=data.index[data.index.astype(str).str.startswith("feature_importances")], inplace=True)

    data["age_in_year"] = (data[AGE_COLUMN] / 12).round(0)

    for _, group in data.groupby(by=["age_in_year", GENDER_COLUMN]):
        group.drop(columns=group.columns[~group.columns.str.startswith("prediction")], inplace=True)
        residual = group.mean() - group

        residual.columns = residual.columns.map(lambda prediction_name: prediction_name.replace("prediction", "residual"))
        raw_data.loc[residual.index, residual.columns] = residual

    raw_data.index = raw_data.index.astype(str, copy=False)
    raw_data.reset_index().to_feather(f"data/{main_category}/{category}.feather")