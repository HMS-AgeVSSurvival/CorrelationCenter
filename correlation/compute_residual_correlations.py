import pandas as pd
from correlation import CORRELATIONS_METHODS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, MINIMUM_NUMBER_PARTICIPANTS
import correlation

target_idx = "age"
# target_col = "age"
target_col = "cvd"

list_main_cat_cat_algo = []
list_main_cat_cat = []
for main_category in MAIN_CATEGORIES:
    for category in CATEGORIES[main_category]:
        list_main_cat_cat.append((main_category, category))
        for algorithm in ALGORITHMS:
            list_main_cat_cat_algo.append((main_category, category, algorithm))
        break
    break
main_cat_cat = pd.MultiIndex.from_tuples(list_main_cat_cat, names=["main_category", "category"])
main_cat_cat_algo = pd.MultiIndex.from_tuples(list_main_cat_cat_algo, names=["main_category", "category", "algorithm"])

template_number = pd.DataFrame(None, index=main_cat_cat, columns=main_cat_cat)
template_correlations = pd.DataFrame(None, index=main_cat_cat_algo, columns=main_cat_cat_algo)

number_participants = template_number.copy()
correlations = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}
correlations_std = {"pearson": template_correlations.copy(), "spearman": template_correlations.copy()}

for main_category_idx in MAIN_CATEGORIES:
    for category_idx in CATEGORIES[main_category_idx]:
        data_idx = pd.read_feather(f"data/{main_category_idx}/{category_idx}.feather").set_index("SEQN")
        data_idx.drop(columns=data_idx.columns[~(data_idx.columns.str.startswith(f"residual_{target_idx}") | data_idx.columms == "fold")], inplace=True)
        data_idx.drop(index=data_idx.index[data_idx.index.astype(str).str.startswith("feature_importances")], inplace=True)

        folds = data_idx["fold"].drop_duplicates()

        if data_idx.shape[1] == 1:  # only the column "fold" remains
            continue

        for main_category_col in MAIN_CATEGORIES:
            for category_col in CATEGORIES[main_category_col]:
                if main_category_idx == main_category_col and category_idx == category_col:
                    number_participants.loc[(main_category_idx, category_idx), (main_category_idx, category_idx)] = data_idx.shape[0]
                    for algorithm_idx in ALGORITHMS:
                        for algorithm_col in ALGORITHMS:
                            if algorithm_idx == algorithm_col:
                                residual_idx = f"residual_{target_idx}_{algorithm_idx}"
                                if f"{residual_idx}_1" in data_idx.columns and f"{residual_idx}_2" in data_idx.columns:
                                    for method in CORRELATIONS_METHODS:
                                        list_correlations_std = []
                                        for idx_fold in folds:
                                            list_correlations_std.append(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_idx}_1"].corr(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_idx}_2"], method=method))
                                        correlations[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = data_idx[f"{residual_idx}_1"].corr(data_idx[f"{residual_idx}_2"], method=method)                             
                                        correlations_std[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations_std).mean()
                            else:
                                residual_idx = f"residual_{target_idx}_{algorithm_idx}"
                                residual_col = f"residual_{target_idx}_{algorithm_col}"
                                if f"{residual_idx}_1" in data_idx.columns and f"{residual_idx}_2" in data_idx.columns and f"{residual_col}_1" in data_idx.columns and f"{residual_col}_2" in data_idx.columns:
                                    for method in CORRELATIONS_METHODS:
                                        list_correlations = []
                                        list_correlations_std = []
                                        for random_state_idx in [1, 2]:
                                            for random_state_col in [1, 2]:
                                                list_correlations.append(data_idx[f"{residual_idx}_{random_state_idx}"].corr(data_idx[f"{residual_col}_{random_state_col}"], method=method))
                                                for idx_fold in folds:
                                                    list_correlations_std.append(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_idx}_{random_state_idx}"].corr(data_idx.loc[data_idx["fold"] == idx_fold, f"{residual_col}_{random_state_col}"], method=method))
                                        correlations[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations).mean()                                    
                                        correlations_std[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations_std).mean()
                else:
                    data_col = pd.read_feather(f"data/{main_category_col}/{category_col}.feather").set_index("SEQN")
                    data_col.drop(columns=data_col.columns[~(data_col.columns.str.startswith(f"residual_{target_col}") | data_col.columms == "fold")], inplace=True)
                    data_col.drop(index=data_col.index[data_col.index.astype(str).str.startswith("feature_importances")], inplace=True)

                    if data_col.shape[1] == 1:  # only the column "fold" remains
                        continue

                    number_participants_intersection = len(data_col.index.intersection(data_idx.index))
                    if number_participants_intersection < MINIMUM_NUMBER_PARTICIPANTS:
                        continue
                    else:
                        number_participants.loc[(main_category_idx, category_idx), (main_category_col, category_col)] = number_participants_intersection

                    for algorithm_idx in ALGORITHMS:
                        for algorithm_col in ALGORITHMS:
                            residual_idx = f"residual_{target_idx}_{algorithm_idx}"
                            residual_col = f"residual_{target_col}_{algorithm_col}"
                            if f"{residual_idx}_1" in data_idx.columns and f"{residual_idx}_2" in data_idx.columns and f"{residual_col}_1" in data_col.columns and f"{residual_col}_2" in data_col.columns:
                                for method in CORRELATIONS_METHODS:
                                    list_correlations = []
                                    for random_state_idx in [1, 2]:
                                        for random_state_col in [1, 2]:
                                            list_correlations.append(data_idx[f"{residual_idx}_{random_state_idx}"].corr(data_col[f"{residual_col}_{random_state_col}"], method=method))

                                    correlations[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations).mean()                                    
                                    correlations_std[method].loc[(main_category_idx, category_idx, algorithm_idx), (main_category_col, category_col, algorithm_col)] = pd.Series(list_correlations).std()
                break
            break
        break
    break

number_participants.to_feather(f"number_participants_{target_idx}_{target_col}.feather")
for method in CORRELATIONS_METHODS:
    correlations[method].to_feather(f"correlations_{target_idx}_{target_col}.feather")    
    correlations_std[method].to_feather(f"correlations_std_{target_idx}_{target_col}.feather")