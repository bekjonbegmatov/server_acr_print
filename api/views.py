from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import xlwt
from . import export_to_excel

def index(request):
    return HttpResponse("<h1>Hello I'ts a first page</h1>")

@api_view(['GET'])
def getRoutes(request):
    # print(request)
    routes = [
        {
            'Developer': 'Begmatov Behruz',
            'Phone number': '+992920851515',
            'Git Hub': 'https://github.com/bekjonbegmatov',
            'FaceBook': '',
            'Instagram': 'https://www.instagram.com/behruz_1312_tj',
            'Telegram': 'https://t.me/behruz_begmatov',
            'Email': 'behruzbegmatov28@gmail.com',
        },
    ]
    return Response(routes)

def get_month(mon , year):
    date.today()
    ye = year
    months_range = mon
    m1 = date.today()
    m1 = str(m1)
    if str(mon) == "01":
        m1 = str(year)+'-' +str(months_range)+"-31"
    elif str(mon) == "02":
        m1 = str(year)+'-' + str(months_range)+"-28"
    elif str(mon) == "03":
        m1 =str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "04":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "05":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "06":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "07":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "08":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "09":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "10":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "11":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "12":
        m1 = str(year)+'-' + str(months_range)+"-31"
    return m1
        
@api_view(['GET'])
def getInventoryProducts(request):
    inventory = InventoryModel.objects.all()

    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)
    months_range = request.query_params.get('months', None)

    barcode = request.query_params.get('barcode', None)

    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)

        inventory = InventoryModel.objects.filter(created__range=[from_date, to_date])
    elif months_range:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)

        inventory = InventoryModel.objects.filter(created__range=[dtoday, dtarget])
    elif barcode:
        inventory = InventoryModel.objects.filter(barcode=barcode)
        
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createInventoryProduct(request):
    data = request.data
    print(data)
    serializer = InventorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print('------------------->>>' , serializer.data)
        return Response(serializer.data)
    print(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getActions(request):
    action = ActionModel.objects.all()
    
    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)

    months_range = request.query_params.get('months', None)
    year = request.query_params.get('year', None)

    from_barcode = request.query_params.get('from_barcode' , None)
    to_barcode = request.query_params.get('to_barcode' , None)

    if from_barcode and to_barcode :
        if int(from_barcode) == 0:
            from_barcode = None
        if int(to_barcode) == 0:
            to_barcode = None

    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        action = ActionModel.objects.filter(created__range=[from_date, to_date])
        if from_barcode and to_barcode :
            c = []
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
    elif months_range and year:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        action = ActionModel.objects.filter(created__range=[m1 , get_month(months_range , year)])
        if from_barcode and to_barcode :
            c = []
            n = from_barcode
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
        # print(get_month(months_range) , m1)
    elif from_barcode and to_barcode :
        c = []
        n = from_barcode
        for i in ActionModel.objects.all():
            if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                c.append(i) 
        action = c
    serializer = ActionSerializer(action, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createAction(request):
    data = request.data
    print("Data:", data)
    serializer = ActionSerializer(data=data)
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained -= float(data['quantity'])
    inventory.sales +=float(data['quantity'])
    inventory.save()
    if serializer.is_valid():
        print("Foobarrrrrr")
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def action_delete(request , pk):
    try:
        action = ActionModel.objects.get(id=pk)
    except ActionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def postBirlik(request):
    data = request.data
    print('data ==> :' , data)
    serializer = BrilikSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print("SAVED !!!!")
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getBriliks(request):
    brlik = BirlikModel.objects.all()
    serializer = BrilikSerializer(brlik , many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def brlik_detailes(request, pk):
    try :
        brlik = BirlikModel.objects.get(id=pk)
    except BirlikModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BrilikSerializer(brlik , many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = BrilikSerializer( brlik , data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        brlik.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def inventory_details(request, pk):
    try:
        inventory = InventoryModel.objects.get(id=pk)
    except InventoryModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventorySerializer(inventory, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InventorySerializer(inventory, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def export_action_to_excel(request):
    return export_to_excel.expot_action_to_exsel(request)
@api_view(['GET'])
def report_actions_and_kresit_to_excel(request):
    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)
    return export_to_excel.exsel_report(request , from_date , to_date )

@api_view(['POST', 'GET'])
def refund_inventory_product(request):
    if request.method == 'GET':
        routes = [
            {
                'Developer': 'Begmatov Behruz',
                'Phone number': '+992920851515',
                'Git Hub': 'https://github.com/bekjonbegmatov',
                'FaceBook': '',
                'Instagram': 'https://www.instagram.com/behruz_1312_tj',
                'Telegram': 'https://t.me/behruz_begmatov',
                'Email': 'behruzbegmatov28@gmail.com',
            },
        ]
        return Response(routes)
    data = request.data
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained += float(data['quantity'])
    inventory.sales -=float(data['quantity'])
    inventory.save()

    try:
        action = ActionModel.objects.get(id=data['id'])
    except ActionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    action.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


