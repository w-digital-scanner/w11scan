from io import BytesIO
import xlwt

# 将数据保存成excel
def write_data(data, tname):
    file = xlwt.Workbook(encoding='utf-8')
    table = file.add_sheet(tname, cell_overwrite_ok=True)
    l = 0
    for line in data:
        c = 0
        for _ in line:
            table.write(l, c, line[c])
            c += 1
        l += 1
    sio = BytesIO()
    file.save(sio)
    return sio


# excel业务逻辑处理
def CreateTable(cursor, id):
    item = []
    item.append(['任务状态', '域名', '网站标题', 'CMS识别结果', '其他信息'])
    for i in cursor:
        item.append(i)
    file = write_data(item, id)
    return file.getvalue()