import argparse
import sys

import pandas as pd

from residual import AGE_COLUMN, GENDER_COLUMN


def residual_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to compute the residual from the predictions"
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

    compute_residual(args.main_category, args.category)


def compute_residual(main_category, category):
    data = pd.read_feather(f"../TrainingCenter/data/{main_category}/{category}.feather").set_index("SEQN")
    raw_data = data.copy()

    data.drop(columns=data.columns[~(data.columns.str.startswith("prediction") | data.columns.isin([AGE_COLUMN, GENDER_COLUMN]))], inplace=True)
    data.drop(index=data.index[data.index.astype(str).str.startswith("feature_importances")], inplace=True)

    data["age_in_year"] = (data[AGE_COLUMN] / 12).round(0)

    for _, group in data.groupby(by=["age_in_year", GENDER_COLUMN]):
        group.drop(columns=group.columns[~group.columns.str.startswith("prediction")], inplace=True)
        residual = group.mean() - group

        residual.columns = residual.columns.map(lambda prediction_name: prediction_name.replace("prediction", "residual"))
        raw_data.loc[residual.index, residual.columns] = residual

    raw_data.reset_index().to_feather(f"data/{main_category}/{category}.feather")