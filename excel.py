from main import product_arr
import xlsxwriter

def writter(parametr):
    book = xlsxwriter.Workbook(r'C:\Users\admin\Desktop\python\parcing\data.xlsx')
    page = book.add_worksheet('product')
    row = 0
    column = 0

    page.set_column('A:A', 20)
    page.set_column('B:B', 20)
    page.set_column('C:C', 20)
    page.set_column('D:D', 50)
    page.set_column('E:E', 50)

    for item in parametr:
        page.write(row, column, item[0])  # write name in A:A
        page.write(row, column+1, item[1]) # write price in A:B
        page.write(row, column+2, item[2]) # write sizes in A:C
        page.write(row, column+3, item[3]) # write description in A:D
        page.write(row, column+4, item[4]) # write features in A:E
        row += 1  # switching to the next line
    
    book.close()

writter(product_arr())