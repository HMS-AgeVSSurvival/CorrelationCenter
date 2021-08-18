import argparse
import sys

import pandas as pd
from lifelines import CoxPHFitter

from log_hazard_ratio.update_log_hazard_ratio import update_results_survival
from residual import (
    AGE_COLUMN,
    GENDER_COLUMN,
    ETHNICITIES,
    DEATH_COLUMN,
    FOLLOW_UP_TIME_COLUMN,
)
from log_hazard_ratio import COLUMNS_TO_DROP_FOR_SCALE, COLUMNS_TO_ADD_AFTER_SCALE


def log_hazard_ratio_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Pipeline to compute the log hazard ratio of the residuals of age prediction when the risk of dying is predicted"
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category.",
        choices=["examination", "laboratory", "questionnaire"],
        required=True,
    )
    parser.add_argument("-c", "--category", help="Name of the category.", required=True)
    parser.add_argument(
        "-sa",
        "--source_algorithm",
        help="Algorithm that has been used to compute the prediction from which the residuals have been computes.",
        required=True,
    )
    args = parser.parse_args(argvs)
    print(args)

    compute_log_hazard_ratio(args.main_category, args.category, args.source_algorithm)


def compute_log_hazard_ratio(main_category, category, source_algorithm):
    for random_state in [1, 2]:
        data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index(
            "SEQN"
        )
        residual_column = f"residual_age_{source_algorithm}_{random_state}"

        if residual_column not in data.columns:
            print(f"No {residual_column} in data")
            continue

        data.drop(
            columns=data.columns[
                ~data.columns.isin(
                    [
                        residual_column,
                        AGE_COLUMN,
                        GENDER_COLUMN,
                        FOLLOW_UP_TIME_COLUMN,
                        DEATH_COLUMN,
                    ]
                    + ETHNICITIES
                )
            ],
            inplace=True,
        )
        data.drop(
            index=data.index[
                data.index.astype(str).str.startswith("feature_importances")
                | data[DEATH_COLUMN].isna()
            ],
            inplace=True,
        )

        if (not data.empty) and ((data[DEATH_COLUMN] == 1.0).sum() > 0):
            columns_to_scale = data.columns.drop(COLUMNS_TO_DROP_FOR_SCALE)
            scaled_data = (data[columns_to_scale] - data[columns_to_scale].mean()) / (
                data[columns_to_scale].std() + 1e-16
            )
            scaled_data[COLUMNS_TO_ADD_AFTER_SCALE] = data[COLUMNS_TO_ADD_AFTER_SCALE]

            cph = CoxPHFitter()

            cph.fit(
                scaled_data, duration_col=FOLLOW_UP_TIME_COLUMN, event_col=DEATH_COLUMN
            )

            log_hazard_ratio, std_error, p_value = cph.summary.loc[
                residual_column, ["coef", "se(coef)", "p"]
            ]

            metrics = {
                "log hazard ratio": log_hazard_ratio,
                "std": std_error,
                "p-value": p_value,
            }
        else:
            metrics = {"log hazard ratio": -1, "std": -1, "p-value": -1}

        update_results_survival(
            main_category, category, source_algorithm, metrics, random_state
        )
