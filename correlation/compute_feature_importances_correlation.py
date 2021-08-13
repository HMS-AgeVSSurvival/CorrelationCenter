import argparse
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm

from correlation import CORRELATIONS_METHODS, CATEGORIES, FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS, FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS


def compute_feature_importances_correlation_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Compute the feature importances correlations for one main category."
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="The main category.",
        choices=["examination", "laboratory", "questionnaire"],
        required=True,
    )
    args = parser.parse_args(argvs)
    print(args)

    compute_correlation(args.main_category)


def get_correlation_same_target_same_algorithm(data, category, target, algorithm, folds, correlations, correlations_std):
    for method in CORRELATIONS_METHODS:
        item_a = data.loc[f"feature_importances_{target}_{algorithm}_1_train"]
        item_b = data.loc[f"feature_importances_{target}_{algorithm}_2_train"]
        if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
            correlations[method].loc[category, ("same_target_same_algorithm", target, algorithm)] = item_a.corr(item_b, method=method)

        list_correlations_std = []
        for random_state_a in [1, 2]:
            for fold_a in folds:
                for random_state_b in range(random_state_a, 3):
                    for fold_b in folds[folds >= fold_a]:
                        if random_state_a == random_state_b and fold_a == fold_b:
                            continue
                        item_a = data.loc[f"feature_importances_{target}_{algorithm}_{random_state_a}_{fold_a}"]
                        item_b = data.loc[f"feature_importances_{target}_{algorithm}_{random_state_b}_{fold_b}"]
                        if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
                            list_correlations_std.append(item_a.corr(item_b, method=method))
                        else:
                            list_correlations_std.append(np.nan)

        correlations_std[method].loc[category, ("same_target_same_algorithm", target, algorithm)] = pd.Series(list_correlations_std).std()


def get_correlation_same_target(data, category, target, algorithms, folds, correlations, correlations_std):
    algorithm_a, algorithm_b = algorithms.split(" vs ")

    for method in CORRELATIONS_METHODS:
        list_correlations = []
        for random_state_a in [1, 2]:
            for random_state_b in [1, 2]:
                item_a = data.loc[f"feature_importances_{target}_{algorithm_a}_{random_state_a}_train"]
                item_b = data.loc[f"feature_importances_{target}_{algorithm_b}_{random_state_b}_train"]
                if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
                    list_correlations.append(item_a.corr(item_b, method=method))
                else:
                    list_correlations.append(np.nan)
        correlations[method].loc[category, ("same_target_same_algorithm", target, algorithms)] = pd.Series(list_correlations).std()

        list_correlations_std = []
        for random_state_a in [1, 2]:
            for fold_a in folds:
                for random_state_b in [1, 2]:
                    for fold_b in folds:
                        item_a = data.loc[f"feature_importances_{target}_{algorithm_a}_{random_state_a}_{fold_a}"]
                        item_b = data.loc[f"feature_importances_{target}_{algorithm_b}_{random_state_b}_{fold_b}"]
                        if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
                            list_correlations_std.append(item_a.corr(item_b, method=method))
                        else:
                            list_correlations_std.append(np.nan)

        correlations_std[method].loc[category, ("same_target_same_algorithm", target, algorithms)] = pd.Series(list_correlations_std).std()


def get_correlation_same_algorithm(data, category, targets, algorithm, folds, correlations, correlations_std):
    target_a, target_b = targets.split(" vs ")

    for method in CORRELATIONS_METHODS:
        list_correlations = []
        for random_state_a in [1, 2]:
            for random_state_b in [1, 2]:
                item_a = data.loc[f"feature_importances_{target_a}_{algorithm}_{random_state_a}_train"]
                item_b = data.loc[f"feature_importances_{target_b}_{algorithm}_{random_state_b}_train"]
                if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
                    list_correlations.append(item_a.corr(item_b, method=method))
                else:
                    list_correlations.append(np.nan)
        correlations[method].loc[category, ("same_target_same_algorithm", targets, algorithm)] = pd.Series(list_correlations).std()

        list_correlations_std = []
        for random_state_a in [1, 2]:
            for fold_a in folds:
                for random_state_b in [1, 2]:
                    for fold_b in folds:
                        item_a = data.loc[f"feature_importances_{target_a}_{algorithm}_{random_state_a}_{fold_a}"]
                        item_b = data.loc[f"feature_importances_{target_b}_{algorithm}_{random_state_b}_{fold_b}"]
                        if method != "spearman" or (item_a.std() != 0 and item_b.std() != 0):
                            list_correlations_std.append(item_a.corr(item_b, method=method))
                        else:
                            list_correlations_std.append(np.nan)
                        
        correlations_std[method].loc[category, ("same_target_same_algorithm", targets, algorithm)] = pd.Series(list_correlations_std).std()


def compute_correlation(main_category):
    list_columns = []
    for same_different in FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS:
        targets = FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS[same_different]
        algorithms = FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS[same_different]
        list_columns.extend(pd.MultiIndex.from_product(([same_different], targets, algorithms)).tolist())

    columns = pd.MultiIndex.from_tuples(list_columns)
    template_correlations = pd.DataFrame(None, index=CATEGORIES[main_category], columns=columns)
    template_correlations.index.name = "category"
    
    correlations = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}
    correlations_std = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}

    for category in tqdm(CATEGORIES[main_category]):
        data = pd.read_feather(f"data/{main_category}/{category}.feather").set_index("SEQN")

        folds = data["fold"].drop_duplicates().dropna().astype(int)
        
        data.drop(index=data.index[~data.index.astype(str).str.startswith("feature_importances")], inplace=True)
        data.dropna(axis="columns", how="all", inplace=True)

        if data.shape[0] == 0:
            continue

        for target in FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS["same_target_same_algorithm"]:
            for algorithm in FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS["same_target_same_algorithm"]:
                feasibility = [f"feature_importances_{target}_{algorithm}_{random_state}_train" in data.index for random_state in [1, 2]]
                feasibility += [f"feature_importances_{target}_{algorithm}_{random_state}_{fold}" in data.index for random_state in [1, 2] for fold in folds]
                if all(feasibility):
                    get_correlation_same_target_same_algorithm(data, category, target, algorithm, folds, correlations, correlations_std)


        for target in FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS["same_target"]:
            for algorithms in FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS["same_target"]:
                feasibility = [f"feature_importances_{target}_{algorithm}_{random_state}_train" in data.index for random_state in [1, 2] for algorithm in algorithms.split(" vs ")]
                feasibility += [f"feature_importances_{target}_{algorithm}_{random_state}_{fold}" in data.index for random_state in [1, 2] for fold in folds for algorithm in algorithms.split(" vs ")]
                if all(feasibility):
                    get_correlation_same_target(data, category, target, algorithms, folds, correlations, correlations_std)

        for targets in FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS["same_algorithm"]:
            for algorithm in FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS["same_algorithm"]:
                feasibility = [f"feature_importances_{target}_{algorithm}_{random_state}_train" in data.index for random_state in [1, 2] for target in targets.split(" vs ")]
                feasibility += [f"feature_importances_{target}_{algorithm}_{random_state}_{fold}" in data.index for random_state in [1, 2] for fold in folds for target in targets.split(" vs ")]
                if all(feasibility):
                    get_correlation_same_algorithm(data, category, targets, algorithm, folds, correlations, correlations_std)

    for method in CORRELATIONS_METHODS:
        correlations[method].columns = map(str, correlations[method].columns.tolist())
        correlations[method].reset_index().to_feather(f"data/correlation/feature_importances/{method}_{main_category}.feather")    
        
        correlations_std[method].columns = map(str, correlations_std[method].columns.tolist())
        correlations_std[method].reset_index().to_feather(f"data/correlation/feature_importances/{method}_std_{main_category}.feather")