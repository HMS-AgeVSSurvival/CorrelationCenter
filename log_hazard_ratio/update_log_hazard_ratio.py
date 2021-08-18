import numpy as np

from utils.google_sheets_sdk import find_cell, findall_cells, get_cell, update_cell

METRICS_COL_ORDER = {"elastic_net": 0, "light_gbm": 1}


def update_results_survival(
    main_category, category, source_algorithm, metrics, random_state
):
    category_row = find_cell(main_category + f" {random_state}", category).row
    p_value_column = findall_cells(main_category + f" {random_state}", "p-value")[
        METRICS_COL_ORDER[source_algorithm]
    ].col

    previous_p_value = get_cell(
        main_category + f" {random_state}", category_row, p_value_column
    ).value
    if previous_p_value is None or metrics["p-value"] < float(previous_p_value):
        print(metrics)
        for metric_name in list(metrics.keys()):
            metric_column = findall_cells(
                main_category + f" {random_state}", metric_name
            )[METRICS_COL_ORDER[source_algorithm]].col
            update_cell(
                main_category + f" {random_state}",
                category_row,
                metric_column,
                np.round(metrics[metric_name], 3),
            )
