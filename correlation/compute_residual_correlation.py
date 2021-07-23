import argparse
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm

from correlation import CORRELATIONS_METHODS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, MINIMUM_NUMBER_PARTICIPANTS


def compute_residual_correlation_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Compute the residual correlations between two targets."
    )
    parser.add_argument(
        "-ti",
        "--target_idx",
        help="Target represented on the indexes.",
        choices=["age", "all", "cvd", "cancer"],
        required=True,
    )
    parser.add_argument(
        "-tc",
        "--target_col",
        help="Target represented on the columns.",
        choices=["age", "all", "cvd", "cancer"],
        required=True,
    )
    args = parser.parse_args(argvs)
    print(args)

    compute_correlation(args.target_idx, args.target_col)


def get_correlation_all_same(target, main_category, category, algorithm, data, folds, correlations, correlations_std):
    residual = f"residual_{target}_{algorithm}"
    if f"{residual}_1" in data.columns and f"{residual}_2" in data.columns:
        for method in CORRELATIONS_METHODS:
            list_correlations_std = []
            for idx_fold in folds:
                if method == "spearman" and (data.loc[data["fold"] == idx_fold, f"{residual}_1"].std() == 0 or data.loc[data["fold"] == idx_fold, f"{residual}_2"].std() == 0):
                    list_correlations_std.append(np.nan)
                else:
                    list_correlations_std.append(data.loc[data["fold"] == idx_fold, f"{residual}_1"].corr(data.loc[data["fold"] == idx_fold, f"{residual}_2"], method=method))
            
            if method == "spearman" and (data[f"{residual}_1"].std() == 0 or data[f"{residual}_2"].std() == 0):
                correlation = 0
            else:
                correlation = data[f"{residual}_1"].corr(data[f"{residual}_2"], method=method)

            correlations[method].loc[(main_category, category, algorithm), (main_category, category, algorithm)] = correlation                            
            correlations_std[method].loc[(main_category, category, algorithm), (main_category, category, algorithm)] = pd.Series(list_correlations_std).std()


def get_correlation_same_main_category_category(main_category, category, target_idx, algorithm_idx, target_col, algorithm_col, data_idx, folds, correlations, correlations_std):
    residual_idx = f"residual_{target_idx}_{algorithm_idx}"
    residual_col = f"residual_{target_col}_{algorithm_col}"

    if f"{residual_idx}_1" in data_idx.columns and f"{residual_idx}_2" in data_idx.columns and f"{residual_col}_1" in data_idx.columns and f"{residual_col}_2" in data_idx.columns:
        for method in CORRELATIONS_METHODS:
            list_correlations = []
            list_correlations_std = []
            for random_state_idx in [1, 2]:
                for random_state_col in [1, 2]:
                    if method == "spearman" and (data_idx[f"{residual_idx}_{random_state_idx}"].std() == 0 or data_idx[f"{residual_col}_{random_state_col}"].std() == 0):
                        list_correlations.append(np.nan)
                    else:
                        list_correlations.append(data_idx[f"{residual_idx}_{random_state_idx}"].corr(data_idx[f"{residual_col}_{random_state_col}"], method=method))
                    
                    for idx_fold in folds:
                        if method == "spearman" and (data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_idx}_{random_state_idx}"].std() == 0 or data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_col}_{random_state_col}"].std() == 0):
                            list_correlations_std.append(np.nan)
                        else:
                            list_correlations_std.append(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_idx}_{random_state_idx}"].corr(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_col}_{random_state_col}"], method=method))
            
            correlations[method].loc[(main_category, category, algorithm_idx), (main_category, category, algorithm_col)] = pd.Series(list_correlations).mean()                                    
            correlations_std[method].loc[(main_category, category, algorithm_idx), (main_category, category, algorithm_col)] = pd.Series(list_correlations_std).std()


def get_correlation_all_different(target_idx, main_category_idx, category_idx, target_col, main_category_col, category_col, data_idx, data_col, correlations, correlations_std):
    for algorithm_idx in ALGORITHMS:
        for algorithm_col in ALGORITHMS:
            residual_idx = f"residual_{target_idx}_{algorithm_idx}"
            residual_col = f"residual_{target_col}_{algorithm_col}"
            if f"{residual_idx}_1" in data_idx.columns and f"{residual_idx}_2" in data_idx.columns and f"{residual_col}_1" in data_col.columns and f"{residual_col}_2" in data_col.columns:
                for method in CORRELATIONS_METHODS:
                    list_correlations = []
                    for random_state_idx in [1, 2]:
                        for random_state_col in [1, 2]:
                            if method == "spearman" and (data_idx[f"{residual_idx}_{random_state_idx}"].std() == 0 or data_col[f"{residual_col}_{random_state_col}"].std() == 0):
                                list_correlations.append(np.nan)
                            else:
                                list_correlations.append(data_idx[f"{residual_idx}_{random_state_idx}"].corr(data_col[f"{residual_col}_{random_state_col}"], method=method))

                    correlations[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations).mean()                                    
                    correlations_std[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations).std()


def compute_correlation(target_idx, target_col):
    list_main_cat_cat_algo = []
    list_main_cat_cat = []
    for main_category in MAIN_CATEGORIES:
        for category in CATEGORIES[main_category]:
            list_main_cat_cat.append((main_category, category))
            for algorithm in ALGORITHMS:
                list_main_cat_cat_algo.append((main_category, category, algorithm))

    main_cat_cat = pd.MultiIndex.from_tuples(list_main_cat_cat, names=["main_category", "category"])
    main_cat_cat_algo = pd.MultiIndex.from_tuples(list_main_cat_cat_algo, names=["main_category", "category", "algorithm"])

    template_number = pd.DataFrame(None, index=main_cat_cat, columns=main_cat_cat)
    template_correlations = pd.DataFrame(None, index=main_cat_cat_algo, columns=main_cat_cat_algo)
    
    number_participants = template_number.copy()
    correlations = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}
    correlations_std = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}

    for main_category_idx in tqdm(MAIN_CATEGORIES):
        for category_idx in CATEGORIES[main_category_idx]:
            data_idx = pd.read_feather(f"data/{main_category_idx}/{category_idx}.feather").set_index("SEQN")
            data_idx.drop(columns=data_idx.columns[~(data_idx.columns.str.startswith(f"residual") | (data_idx.columns == "fold"))], inplace=True)
            data_idx.drop(index=data_idx.index[data_idx.index.astype(str).str.startswith("feature_importances")], inplace=True)

            folds = data_idx["fold"].drop_duplicates()

            if data_idx.shape[1] == 1:  # only the column "fold" remains
                continue

            for main_category_col in tqdm(MAIN_CATEGORIES):
                for category_col in CATEGORIES[main_category_col]:
                    if main_category_idx == main_category_col and category_idx == category_col:
                        number_participants.loc[(main_category_idx, category_idx), (main_category_idx, category_idx)] = data_idx.shape[0]

                        for algorithm_idx in ALGORITHMS:
                            for algorithm_col in ALGORITHMS:
                                if target_idx == target_col and algorithm_idx == algorithm_col:
                                    get_correlation_all_same(target_idx, main_category_idx, category_idx, algorithm_idx, data_idx, folds, correlations, correlations_std)
                                else:
                                    get_correlation_same_main_category_category(main_category_idx, category_idx, target_idx, algorithm_idx, target_col, algorithm_col, data_idx, folds, correlations, correlations_std)
                    else:
                        data_col = pd.read_feather(f"data/{main_category_col}/{category_col}.feather").set_index("SEQN")
                        data_col.drop(columns=data_col.columns[~(data_col.columns.str.startswith(f"residual_{target_col}") | (data_col.columns == "fold"))], inplace=True)
                        data_col.drop(index=data_col.index[data_col.index.astype(str).str.startswith("feature_importances")], inplace=True)

                        if data_col.shape[1] == 1:  # only the column "fold" remains
                            continue

                        number_participants_intersection = len(data_col.index.intersection(data_idx.index))
                        if number_participants_intersection < MINIMUM_NUMBER_PARTICIPANTS:
                            continue
                        else:
                            number_participants.loc[(main_category_idx, category_idx), (main_category_col, category_col)] = number_participants_intersection
                        
                        get_correlation_all_different(target_idx, main_category_idx, category_idx, target_col, main_category_col, category_col, data_idx, data_col, correlations, correlations_std)
    
    number_participants.columns = map(str, number_participants.columns.tolist())
    number_participants.reset_index().to_feather(f"data/correlation/residual/number_participants_{target_idx}_{target_col}.feather")

    for method in CORRELATIONS_METHODS:
        correlations[method].columns = map(str, correlations[method].columns.tolist())
        correlations[method].reset_index().to_feather(f"data/correlation/residual/{method}_{target_idx}_{target_col}.feather")    
        
        correlations_std[method].columns = map(str, correlations_std[method].columns.tolist())
        correlations_std[method].reset_index().to_feather(f"data/correlation/residual/{method}_std_{target_idx}_{target_col}.feather")