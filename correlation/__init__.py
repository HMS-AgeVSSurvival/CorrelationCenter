import os

CORRELATIONS_METHODS = ["pearson", "spearman"]

TARGETS = ["age", "all", "cvd", "cancer"]
TARGETS_TARGETS = [f"{target_1} vs {target_2}" for idx_target, target_1 in enumerate(TARGETS) for target_2 in TARGETS[idx_target:]]

MAIN_CATEGORIES = ["examination", "laboratory", "questionnaire"]

EXAMINATION_CATEGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/examination/")))
LABORATORY_CATEGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/laboratory/")))
QUESTIONNAIRE_CATEGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/questionnaire/")))
CATEGORIES = {"examination": EXAMINATION_CATEGORIES, "laboratory": LABORATORY_CATEGORIES, "questionnaire": QUESTIONNAIRE_CATEGORIES}

ALGORITHMS = ["elastic_net", "light_gbm"]
ALGORITHMS_ALGORITHMS = [f"{algorithm_1} vs {algorithm_2}" for idx_algorithm, algorithm_1 in enumerate(ALGORITHMS) for algorithm_2 in TARGETS[idx_algorithm:]]

MINIMUM_NUMBER_PARTICIPANTS = 10


FEATURE_IMPORTANCES_SAME_DIFFERENT_TARGETS = {"same_target_same_algorithm": TARGETS, "same_target": TARGETS, "same_algorithm": TARGETS_TARGETS}
FEATURE_IMPORTANCES_SAME_DIFFERENT_ALGORITHMS = {"same_target_same_algorithm": ALGORITHMS, "same_target": ALGORITHMS_ALGORITHMS, "same_algorithm": ALGORITHMS}