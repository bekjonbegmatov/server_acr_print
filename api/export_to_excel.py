from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import xlwt

def expot_action_to_exsel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=" ' + 'Actions_' + str(date.today()) + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Actions')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [ 'Штрих код' , 'Название' , 'Кол-ва' , 'Цена(прод)' , 'Cозданo' ,  'Oплачено' , 'Цена(покупка)' , 'Цена(тела)' , 'Общая сумма' , 'прибыль']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = []
    final_selling_price = 0
    final_paid = 0
    final_del_price = 0
    final_quantity = 0
    final_body_price = 0
    final_del_price = 0
    final_foida = 0

    for i in ActionModel.objects.all():
        temp = []
        tp = 0
        temp.append(i.barcode)
        temp.append(i.product_name)
        temp.append(i.quantity)
        temp.append(i.selling_price)
        temp.append(str(i.created)[0:10])
        temp.append(i.paid)
        temp.append(i.del_price)
        temp.append(i.body_price)
        temp.append(round(float(i.quantity)*float(i.selling_price),2))
        temp.append(float(i.paid - (i.body_price * i.quantity)))

        # nothing
        final_selling_price += float(i.selling_price)
        final_body_price += float(i.body_price)
        final_quantity += float(i.quantity)
        final_paid += float(i.paid)
        final_del_price += float(i.del_price)
        final_foida += float( i.paid - (i.body_price * i.quantity) )

        rows.append(temp)
    rows.append(" ")
    s_colums = ['Цена(прод.общ)' , 'Цена(покупка.общ)' , 'Цена(тела.общ)' , 'Общ.количество' , 'Общ.Oплачено' , 'Oбщая прибыль' ]
    rows.append(s_colums)

    temp1 = []
    temp1.append(final_selling_price)
    temp1.append(final_del_price)
    temp1.append(final_body_price)
    temp1.append(final_quantity)
    temp1.append(final_paid)
    temp1.append(final_foida)
    
    rows.append(temp1)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def excel_create(request, id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventory.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('recibo')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['barcode' , 'product_name' , 'quantity' , 'remained' , 'sales' , 'del_price']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = InventoryModel.objects.all()
    rows.values_list('num_orden', 'client', 'fechain', 'instrumento', 'marca')
    
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def exsel_report(request , from_date , to_date ):

    print(from_date , to_date)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ACR Print '+ str(date.today()) +'.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('recibo')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['№' , 'Qr code' , 'Название' , 'Кол-ва' , 'Eдиница' , 'Цена' , 'Цена(продажа)' , 'Оплачено' , 'Cозданo' , 'Общая сумма' ]
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Vatebles
    rows = []
    temp_quantity = 0
    temp_price = 0
    temp_selling_price = 0
    temp_paid = 0
    temp_total_price = 0
    count = 1

    if from_date and to_date :
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        for action in ActionModel.objects.filter(created__range=[from_date, to_date]):
            
            temp = []
            temp.append(count)
            temp.append(action.barcode)
            temp.append(action.product_name)
            temp.append(action.quantity)
            temp.append(action.birlik)
            temp.append(action.del_price)
            temp.append(action.selling_price)
            temp.append(action.paid)
            temp.append(str(action.created)[0:10])        
            temp.append(round(float(action.quantity)*float(action.selling_price),2))

            temp_total_price += round(float(action.quantity)*float(action.selling_price),2)
            temp_quantity += action.quantity
            temp_price += round(float(action.quantity)*float(action.del_price),2)
            temp_selling_price += round(float(action.quantity)*float(action.selling_price),2)
            temp_paid += action.paid


            rows.append(temp)
            count += 1 
        rows.append(" ")

        temp1 = []
        temp1.append(' ')
        temp1.append(' ')
        temp1.append(' ')
        temp1.append(temp_quantity)
        temp1.append(' ')
        temp1.append(temp_price)
        temp1.append(temp_selling_price)
        temp1.append(temp_paid)
        temp1.append(' ')
        temp1.append(temp_total_price)
        rows.append(temp1)
        rows.append(" ")
        rows.append(['pribl' , float(temp_paid) - float(temp_price)])
    else: 
        for action in ActionModel.objects.all():
            temp = []
            temp.append(count)
            temp.append(action.barcode)
            temp.append(action.product_name)
            temp.append(action.quantity)
            temp.append(action.birlik)
            temp.append(action.del_price)
            temp.append(action.selling_price)
            temp.append(action.paid)
            temp.append(str(action.created)[0:10])        
            temp.append(round(float(action.quantity)*float(action.selling_price),2))

            temp_total_price += round(float(action.quantity)*float(action.selling_price),2)
            temp_quantity += action.quantity
            temp_price += round(float(action.quantity)*float(action.del_price),2)
            temp_selling_price += round(float(action.quantity)*float(action.selling_price),2)
            temp_paid += action.paid


            rows.append(temp)
            count += 1 
        rows.append(" ")

        temp1 = []
        temp1.append(' ')
        temp1.append(' ')
        temp1.append(' ')
        temp1.append(temp_quantity)
        temp1.append(' ')
        temp1.append(temp_price)
        temp1.append(temp_selling_price)
        temp1.append(temp_paid)
        temp1.append(' ')
        temp1.append(temp_total_price)
        rows.append(temp1)
        rows.append(" ")
        rows.append(['pribl' , float(temp_paid) - float(temp_price)])

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response




