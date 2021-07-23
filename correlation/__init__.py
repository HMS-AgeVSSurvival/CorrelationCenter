import os

CORRELATIONS_METHODS = ["pearson", "spearman"]

TARGETS = ["Age", "Survival All", "Survival CVD", "Survival Cancer"]

MAIN_CATEGORIES = ["examination", "laboratory", "questionnaire"]

EXAMINATION_CATEGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/examination/")))

LABORATORY_CATEGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/laboratory/")))
QUESTIONNAIRE_CATEOGORIES = list(map(lambda name_feather: name_feather.split(".feather")[0], os.listdir("data/questionnaire/")))
CATEGORIES = {"examination": EXAMINATION_CATEGORIES, "laboratory": LABORATORY_CATEGORIES, "questionnaire": QUESTIONNAIRE_CATEOGORIES}

ALGORITHMS = ["elastic_net", "light_gbm"]

MINIMUM_NUMBER_PARTICIPANTS = 10