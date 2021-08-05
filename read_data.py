from xlrd import open_workbook,xldate_as_tuple

file_name = 'Monopoly_template.xls'
# sheets = ['Sheet1', 'Sheet2']


def get_property_info():
    return get_sheet('Sheet1')

def get_function_info():
    return get_sheet('Sheet2')

def get_sheet(sheet_name):
    with open_workbook(file_name) as workbook:
        worksheet=workbook.sheet_by_name(sheet_name)
        row_count = worksheet.nrows
        col_count = worksheet.ncols
        head = [worksheet.cell_value(0,col_index) for col_index in range(col_count)]
        data = []

        for row_index in range(1, row_count):
            single_data = {}
            for col_index in range(col_count):
                single_data[head[col_index]] = worksheet.cell_value(row_index,col_index)
            data.append(single_data)
    return data

