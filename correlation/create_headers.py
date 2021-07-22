import os
import pandas as pd
import numpy as np
from utils.google_sheets_sdk_correlations import update_cell, merge_rows, merge_cols, update_cells, get_cell, to_alphabet

from correlation import CATEGORIES_EXAMINATION, CATEGORIES_LABORATORY, CATEGORIES_QUESTIONNAIRE, TARGETS, TARGETS_POSITION, MAIN_CATEGORIES, MAIN_CATEGORIES_POSITION, CATEGORIES, CATEGORIES_POSITION, ALGORITHMS, ALGORITHMS_POSITION, INDENT


def create_header_residuals():
    sheet_name = "Residual"

    list_algorithms = np.array([ALGORITHMS * (len(TARGETS) * len(CATEGORIES))])
    update_cells(sheet_name, INDENT, ALGORITHMS_POSITION, list_algorithms.T)
    update_cells(sheet_name, ALGORITHMS_POSITION, INDENT, list_algorithms)

    # list_targets = np.array([np.repeat(TARGETS, len(MAIN_CATEGORIES))])
    # update_cells(sheet_name, INDENT, TARGETS_POSITION, list_targets.T)
    # update_cells(sheet_name, TARGETS_POSITION, INDENT, list_targets)

    # list_targets = np.array([np.repeat(TARGETS, len(MAIN_CATEGORIES))])
    # update_cells(sheet_name, INDENT, TARGETS_POSITION, list_targets.T)
    # update_cells(sheet_name, TARGETS_POSITION, INDENT, list_targets)

    # list_targets = np.array([np.repeat(TARGETS, len(MAIN_CATEGORIES))])
    # update_cells(sheet_name, INDENT, TARGETS_POSITION, list_targets.T)
    # update_cells(sheet_name, TARGETS_POSITION, INDENT, list_targets)

    # for idx_target, target in enumerate(TARGETS):
    #     first_main_category = idx_target * len(MAIN_CATEGORIES) + INDENT
    #     last_main_category = (idx_target + 1) * (len(MAIN_CATEGORIES)) + INDENT - 1
    #     merge_rows(sheet_name, (first_main_category, last_main_category), TARGETS_POSITION)
    #     merge_cols(sheet_name, TARGETS_POSITION, (first_main_category, last_main_category))



if __name__ == "__main__":
    create_header_residuals()

