import os
import time
import numpy as np
import gspread
import json


def get_worksheet(sheet_name):
    service_account_id = np.random.randint(1, 6)
    gc = gspread.service_account(
        filename=f"credentials/credentials_{service_account_id}.json"
    )
    google_sheet = gc.open_by_key(os.environ.get("GOOGLE_RESULTS_SHEET_ID"))

    return google_sheet.worksheet(sheet_name)


def handle_gspread_error(error):
    error = json.loads(error.response._content)

    if error["error"]["code"] in [
        429,
        101,
        500,
    ]:  # Means too many Google Sheet API's calls
        sleep_time = 61
        print(f"Sleep {sleep_time}")
        time.sleep(sleep_time)
    else:
        raise error


def update_cell(sheet_name, row, col, value):
    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(sheet_name)
            worksheet.update_cell(row, col, str(value))
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)


def update_cells(sheet_name, first_row, first_col, values):
    last_row = first_row + values.shape[0] - 1
    last_col = first_col + values.shape[1] - 1
    first_col_letter = chr(ord("@") + first_col)
    last_col_letter = chr(ord("@") + last_col)

    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(sheet_name)
            worksheet.update(
                f"{first_col_letter}{first_row}:{last_col_letter}{last_row}",
                list(map(list, values.astype(str))),
            )
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)


def find_cell(sheet_name, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cell = worksheet.find(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cell


def findall_cells(sheet_name, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cells = worksheet.findall(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cells


def get_cell(sheet_name, row, col):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cell = worksheet.cell(row, col)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return cell


def get_col_values(sheet_name, col_name):
    col = find_cell(sheet_name, col_name).col

    got_col = False
    while not got_col:
        try:
            worksheet = get_worksheet(sheet_name)
            col_values = worksheet.col_values(col)
            got_col = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)

    return col_values
