# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: excel.py
    Time: 2021/7/1 上午11:39
-------------------------------------------------
    Change Activity: 2021/7/1 上午11:39
-------------------------------------------------
    Desc: 
"""
import xlwt


def excel_style():
    # 为样式创建字体
    font = xlwt.Font()
    # 设置字体名字对应系统内字体
    font.name = u'微软雅黑'
    font.height = 240

    alignment = xlwt.Alignment()
    # 设置水平居中
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    # 设置垂直居中
    alignment.vert = xlwt.Alignment.VERT_CENTER

    borders = xlwt.Borders()  # Create borders
    # 添加边框-虚线边框
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    # 边框上色
    borders.left_colour = 23
    borders.right_colour = 23
    borders.top_colour = 23
    borders.bottom_colour = 23

    # 初始化样式
    style = xlwt.XFStyle()
    # 为样式设置字体
    style.font = font
    # 对齐方式设置
    style.alignment = alignment
    style.borders = borders

    return style


def write_excel(data, headers, name, path_name):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(name)

    style = excel_style()

    num = 1
    for k, v in headers.items():
        if k.startswith('$'):
            continue
        sheet.col(num).width = 100 * 50
        sheet.write(0, num, v, style)
        num += 1

    col = 0
    for n in range(0, len(data)):
        num = 1

        pattern = xlwt.Pattern()
        if n % 2 == 0:
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 22
        else:
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 1

        style.pattern = pattern

        sheet.row(col).height_mismatch = True
        sheet.row(col).height = 30 * 20

        # 根据文件头来获取数据
        for key in headers.keys():
            item = data[n][key]
            sheet.write(n + 1, num, item, style)
            num += 1

        # for k, v in data[n].items():
        #     sheet.write(n + 1, num, v, style)
        #     num += 1

        col += 1

    sheet.row(col).height_mismatch = True
    sheet.row(col).height = 30 * 20

    workbook.save(f'{path_name}')
    print(f'{name}.xls 写入成功')


if __name__ == '__main__':
    data_list = [
        {'desc': 'desc1', 'name': 'name1', 'plat': 'plat1'},
        {'desc': 'desc2', 'name': 'name2', 'plat': 'plat2'},
        {'desc': 'desc3', 'name': 'name3', 'plat': 'plat3'},
        {'desc': 'desc4', 'name': 'name4', 'plat': 'plat4'},
        {'desc': 'desc5', 'name': 'name5', 'plat': 'plat5'},
    ]

    title = {'desc': '描述', 'name': '店铺名称', 'plat': '渠道'}
    excel_name = 'test'
    write_excel(data_list, title, excel_name, excel_name)
