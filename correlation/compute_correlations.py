import pandas as pd
import numpy as np
from utils.google_sheets_sdk_correlations import update_cell, merge_rows, merge_cols, update_cells, get_cell

sheet_name = "Residual"
TARGETS = ["Age", "Survival All", "Survival CVD", "Survival Cancer"]
TARGETS_POSITION = 1
MAIN_CATEGORIES = ["examination", "laboratory", "questionnaire"]
MAIN_CATEGORIES_POSITION = 2
INDENT = 3

print(get_cell(sheet_name, 1, 3).value)
# list_main_categories = np.array([MAIN_CATEGORIES * len(TARGETS)])
# update_cells(sheet_name, INDENT, MAIN_CATEGORIES_POSITION, list_main_categories.T)
# update_cells(sheet_name, MAIN_CATEGORIES_POSITION, INDENT, list_main_categories)

# list_targets = np.array([np.repeat(TARGETS, len(MAIN_CATEGORIES))])
# update_cells(sheet_name, INDENT, TARGETS_POSITION, list_targets.T)
# update_cells(sheet_name, TARGETS_POSITION, INDENT, list_targets)

# for idx_target, target in enumerate(TARGETS):
#     first_main_category = idx_target * len(MAIN_CATEGORIES) + INDENT
#     last_main_category = (idx_target + 1) * (len(MAIN_CATEGORIES)) + INDENT - 1
#     merge_rows(sheet_name, (first_main_category, last_main_category), TARGETS_POSITION)
#     merge_cols(sheet_name, TARGETS_POSITION, (first_main_category, last_main_category))