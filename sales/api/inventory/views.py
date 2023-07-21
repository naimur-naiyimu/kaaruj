
from sales.api.filters import CustomInvoiceSearchFilter, InvoiceSearchFilter
from . import serializers
from ...models import *
from coreapp.models import User
from coreapp.helper import *
from utility.utils.bulk_utils import *
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from coreapp.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.decorators import action
from .serializers import *
from utility.utils.model_utils import *
import calendar
from datetime import date,timedelta
from inventory.models import *
from django.db.models import Q


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny,]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        delivery_status_queue = {
            'Returned':0,
            'Recieved':1,
            'Delivered':2,
            'Pending':3,
            'Hold':4,
            'Dispatched':5
        }
        
        source_status_queue = {
            'Ecommerce Website':0,
            'Inventory':1,
            'Admin Panel':2
        }
        
        delivery_type_queue = {
            'Regular':0,
            'Urgent':1
        }
        
        payment_status_queue = {
            'Paid':0,
            'Unpaid':1,
            'Due':2
        }

        
        q = self.request.query_params.get('query')
        if q:
            queryset = queryset.filter(Q(number__icontains=q) | Q(created_by__first_name__icontains=q) | Q(created_by__last_name__icontains=q) | Q(total_amount__icontains=q) | Q(invoice_date__icontains=q) | Q(delivery_status__in=[delivery_status_queue[label] for label in delivery_status_queue if label.lower().startswith(q.lower())]) | Q(source__in=[source_status_queue[label] for label in source_status_queue if q.lower() in label.lower()]) | Q(delivery_type__in=[delivery_type_queue[label] for label in delivery_type_queue if label.lower().startswith(q.lower())]) | Q(payment_status__in=[payment_status_queue[label] for label in payment_status_queue if label.lower().startswith(q.lower())])
            )
        return queryset
    
    def get_serializer_class(self):
        print("self.action",self.action)
        if self.action == 'list':
            return InvoiceListSerializer
        elif self.action == 'update':
            return InvoiceSerializer_Update
        elif self.action == 'partial_update':
            return InvoiceSerializer_Update
        else:
            return InvoiceSerializer
    
    
    @paginate
    @action(detail=False, methods=['get'])
    def filter(self, request, *args, **kwargs):
        start = request.GET.get("start")
        end = request.GET.get("end")
        try:
            start_month, start_day,  start_year = start.split("/")
        except:
            return Response({"data": [], "error": "Start date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        try:
            end_month, end_day,  end_year = end.split("/")
        except:
            return Response({"data": [], "error": "End date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                                        hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                                        hour=23, minute=59, second=59)
        return self.get_queryset().model.objects.filter(invoice_date__range=[start_date, end_date],is_custom=False)
        



class ExportDailyReportAPIView(APIView):
   permission_classes = (AllowAny,)
   def get(self, request):
        start_date= request.GET.get('start')
        end_date = request.GET.get('end')
        is_custom = request.GET.get('is_custom')
        query = request.GET.get('query')
        dataset = DailyReportResource(start_date,end_date,is_custom,query).export()
        today = datetime.date.today().strftime('%Y-%m-%d')  # get current date in YYYY-MM-DD format
        filename = f'DailyReport_{today}.xlsx'  # create filename with current date
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] =f'attachment; filename="{filename}"'
        return response
   
   
class AllInvoiceView(FilterGivenDateInvoice,viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,IsAuthenticated)
    queryset = Invoice.objects.all()
    serializer_class = All_InvoiceSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = InvoiceSearchFilter



    def get_serializer_class(self):
        if self.action == 'list':
            return  InvoiceListSerializer
        else:
            return  InvoiceSerializer
        
    
    

class InvoiceView(FilterGivenDateInvoice,viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,IsAuthenticated)
    queryset = Invoice.objects.all()
    serializer_class =  InvoiceSerializer
    lookup_field = 'slug'
    filterset_class = InvoiceSearchFilter
    
    

    def get_serializer_class(self):
        if self.action == 'list':
            return  InvoiceListSerializer
        else:
            return  InvoiceSerializer

    def get_queryset(self):
        return self.queryset.filter(is_custom=False)

    @paginate
    @action(detail=False, methods=['get'])
    def filter(self, request, *args, **kwargs):
        start = request.GET.get("start")
        end = request.GET.get("end")
        try:
            start_month, start_day,  start_year = start.split("/")
        except:
            return Response({"data": [], "error": "Start date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        try:
            end_month, end_day,  end_year = end.split("/")
        except:
            return Response({"data": [], "error": "End date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                                        hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                                        hour=23, minute=59, second=59)
        return self.get_queryset().model.objects.filter(invoice_date__range=[start_date, end_date],is_custom=False)

class CustomInvoiceView(FilterGivenDateInvoice,viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,IsAuthenticated)
    queryset = Invoice.objects.all()
    serializer_class =  InvoiceSerializer
    lookup_field = 'slug'
    filterset_class = CustomInvoiceSearchFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return  InvoiceListSerializer
        else:
            return  InvoiceSerializer

    def get_queryset(self):
        return self.queryset.filter(is_custom=True)

    @paginate
    @action(detail=False, methods=['get'])
    def filter(self, request, *args, **kwargs):
        start = request.GET.get("start")
        end = request.GET.get("end")
        try:
            start_month, start_day,  start_year = start.split("/")
        except:
            return Response({"data": [], "error": "Start date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        try:
            end_month, end_day,  end_year = end.split("/")
        except:
            return Response({"data": [], "error": "End date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
        start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                                        hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                                        hour=23, minute=59, second=59)
        return self.get_queryset().model.objects.filter(invoice_date__range=[start_date, end_date],is_custom=True)

class DailySalesReportAPIView(APIView):
    def get(self, request, format=None):
        today = datetime.datetime.today()
        start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                       hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                     hour=23, minute=59, second=59)  # represents 23:59:59

        invoices = Invoice_Products.objects.filter(invoice_date__range=(start_date, end_date))

        sales = {}
        total_quantity = 0
        total_amount = 0

        for invoice_product in invoices:
            product_name = invoice_product.product_name
            quantity = invoice_product.quantity
            amount = invoice_product.total

            if product_name in sales:
                sales[product_name]['quantity'] += quantity
                sales[product_name]['total_amount'] += amount
            else:
                sales[product_name] = {
                    'quantity': quantity,
                    'total_amount': amount
                }

            total_quantity += quantity
            total_amount += amount

        response_data = {
            'today_sales': sales,
            'today_total_quantity': total_quantity,
            'today_total_amount': total_amount
        }
        return Response(response_data)

def createDailyReport():
    today = datetime.datetime.today()
    start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                   hour=0, minute=0, second=0)  # represents 00:00:00
    end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                 hour=23, minute=59, second=59)  # represents 23:59:59

    todays_invoices_productss =  Invoice_Products.objects.filter(
        Q(invoice__invoice_date__range=(start_date, end_date)) & ~Q(product=None))
    
    print("todays_invoices_productss",todays_invoices_productss)

    try:
        todaysProductList = []
        for inv_prod in todays_invoices_productss:
            # todaysProductList[]
            if inv_prod.product.id not in todaysProductList:
                mainProudct = inv_prod.product.id
                todaysProductList.append(mainProudct)
        for current_prod in todaysProductList:
            getCurrentProduct = Products.objects.filter(id=current_prod).first()
            alreadyReportCheck =  DailyReport.objects.filter(
                Q(created_at__range=(start_date, end_date)) & Q(products_id=current_prod)).first()
            if getCurrentProduct is not None and alreadyReportCheck is None:
                 DailyReport.objects.create(
                    products_id=getCurrentProduct.id, total_amount=getCurrentProduct.today_total_amount(getCurrentProduct.id), quantity=getCurrentProduct.today_total_sales(getCurrentProduct.id))
            else:
                alreadyReportCheck.total_amount = getCurrentProduct.today_total_amount(getCurrentProduct.id)
                alreadyReportCheck.quantity = getCurrentProduct.today_total_sales(getCurrentProduct.id)
                alreadyReportCheck.save()
    except Exception as e:
        traceback.print_exc()


class createDailyReportFromAPi(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            createDailyReport()
            return Response({"data": "Generated"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"data": "Generated", "error": str(e)}, status=status.HTTP_200_OK)


class GetDailyReport(APIView):

    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)
    queryset = DailyReport.objects.all()

    def get_object(self, pk):
        try:
            return  DailyReport.objects.get(pk=pk)
        except  DailyReport.DoesNotExist:
            raise Http404

    def get(self, request):
        try:
            today = datetime.datetime.today()
            start = request.GET.get("start")
            end = request.GET.get("end")
            is_custom = request.GET.get("is_custom", "false")
      
            ReportList = []
            if (start == None and end == None):
                if is_custom == "true":
                    ReportList =  DailyReport.objects.filter(is_custom=True)
                else:
                    ReportList =  DailyReport.objects.filter(is_custom=False)

            else:
                # month / date / year
                try:
                    start_month, start_day,  start_year = start.split("/")
                except:
                    return Response({"data": [], "error": "Start date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
                try:
                    end_month, end_day,  end_year = end.split("/")
                except:
                    return Response({"data": [], "error": "End date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
                # start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                #                                hour=0, minute=0, second=0)  # represents 00:00:00
                # end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                #                              hour=23, minute=59, second=59)
                start_date = datetime.datetime.strptime(start, '%m/%d/%Y').date()
                end_date = datetime.datetime.strptime(end, '%m/%d/%Y').date()
                if is_custom == "true":
                    ReportList =  DailyReport.objects.filter(created_at__range=[start_date, end_date],is_custom=True)
                else:
                    ReportList =  DailyReport.objects.filter(created_at__range=[start_date, end_date],is_custom=False)
            
            print("ReportList", ReportList)

            if (len(list(ReportList)) > 0):
                # ReportList =  DailyReport.objects.filter(created_at__range=(start_date, end_date))
                data = []
                for report in ReportList:
                    if report.products is not None or report.product_name is not None:
                        data.append({
                            "id": report.id,
                            "created_at": report.created_at,
                            "product": report.products.name if report.products!=None else report.product_name,
                            # "image": report.products.thumb.url if report.products.thumb else None,
                            "total_sales": report.quantity,
                            "total_amount": report.total_amount,
                            'is_custom': report.is_custom,

                        })

                return Response({"data": data}, status=status.HTTP_200_OK)
            return Response({"data": []}, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            data = {
                "data": [],
                "error": str(e)
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class DeleteDailyReport(APIView):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)
    queryset =  DailyReport.objects.all()

    def get_object(self, pk):
        try:
            return  DailyReport.objects.get(pk=pk)
        except  DailyReport.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        DailyReport.objects.get(pk=pk).delete()
        return Response({"data": 'Deleted'}, status=status.HTTP_204_NO_CONTENT)


class InvoiceNewProductsView(APIView):
    def post(self, request):
        try:
            data = request.data.get('data')
            run = 0
            for item in data:
                product = item['product']
                product_name = item.get("product_name", None)
                variant = item['variant']
                invoice = item['invoice']
                quantity = item['quantity']
                price = item['price']
                total = item['total']

                try:
                    newObj =  Invoice_Products.objects.create(
                        product_id=product,
                        product_name=product_name,
                        variant_id=variant,
                        invoice_id=invoice,
                        quantity=quantity,
                        total=total

                    )
                except Exception as e:  # in except that means this product or its variant doesn't exist anymore
                    traceback.print_exc()
                data = {'data': "created"}
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            msg = str(e)
            return Response({'msg': msg}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data.get('data')
            for item in data:
                product = item['product']
                product_name = item.get("product_name", None)
                variant = item['variant']
                invoice = item['invoice']
                quantity = item['quantity']
                price = item['price']
                total = item['total']
                inv_product_id = item['inv_product_id']

                try:
                    pass

                except Exception as e:  # in except that means this product or its variant doesn't exist anymore
                    traceback.print_exc()

            return Response({'data': "Updated"}, status=status.HTTP_200_OK)

        except Exception as e:
            msg = str(e)
            return Response({'msg': msg}, status=status.HTTP_400_BAD_REQUEST)


def getNumberofDays():
    count = 6
    today = date.today()
    while 1:
        my_date = today - timedelta(days=count)
        dayname = calendar.day_name[my_date.weekday()]
        print(dayname)
        if (dayname == 'Saturday'):
            break
        count -= 1

    return count


def getTodayDay(today):
    dayname = calendar.day_name[today.weekday()]
    return dayname


dateFormat = '%d-%m-%Y'


class ReportChartData(APIView):
    def get(self, request):
        try:
            filter_by = request.GET.get("filter", "week")
            is_custom = request.GET.get("is_custom",None)

            if (filter_by == "week"):
                '''
                # /api/v1/sales/date/?filter=week
                if /api/v1/sales/date/ default will be current week

                '''
                today = date.today()
                start_number = getNumberofDays()
                weeek_started = today - timedelta(days=start_number)
                todays_data = today + timedelta(days=1)  # so that it includes in the result

                if is_custom == "true":
                    filtered_data =  Invoice.objects.filter(invoice_date__range=[weeek_started, todays_data],is_custom=True)
                    print("filtered_data",filtered_data)
                elif is_custom == "false":
                    filtered_data =  Invoice.objects.filter(invoice_date__range=[weeek_started, todays_data],is_custom=False)
                else:
                    filtered_data =  Invoice.objects.filter(invoice_date__range=[weeek_started, todays_data])

                delta = datetime. timedelta(days=1)
                data = {
                    "Saturday": 0,
                    "Sunday": 0,
                    "Monday": 0,
                    "Tuesday": 0,
                    "Wednesday": 0,
                    "Thursday": 0,
                    "Friday": 0,

                }

                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.invoice_date.strftime('%A')] += items.total_amount  # adding all sold data
                        # data[items.created_at.strftime('%d/%m/%Y')] += items.product.total_amount  # adding all sold data

                    return Response({"data": data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)

            if (filter_by == "month"):
                '''
                # /api/v1/sales/date/?filter=month?month=9
                if /api/v1/sales/date/?filter=month default will be current month
                '''
                today = datetime.datetime.today()
                year = today.year
                month = today.month
                filter_month = request.GET.get("month", month)
                if is_custom == "true":
                   filtered_data =   Invoice.objects.filter(invoice_date__year__gte=year,
                                                              invoice_date__month__gte=filter_month,
                                                              invoice_date__year__lte=year,
                                                              invoice_date__month__lte=filter_month,
                                                              is_custom=True)
                elif is_custom == "false":
                    filtered_data =  Invoice.objects.filter(invoice_date__year__gte=year,
                                                              invoice_date__month__gte=filter_month,
                                                              invoice_date__year__lte=year,
                                                              invoice_date__month__lte=filter_month,
                                                              is_custom=False
                                                              
                                                              )
                else:
                    filtered_data =  Invoice.objects.filter(invoice_date__year__gte=year,
                                                              invoice_date__month__gte=filter_month,
                                                              invoice_date__year__lte=year,
                                                              invoice_date__month__lte=filter_month
                                                              )
                data = {}
                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.invoice_date.strftime(dateFormat)] = 0  # intialized 0 to all date
                    now = datetime.datetime.now()
                    year = now.year
                    month = now.month
                    num_days = calendar.monthrange(year, month)[1]
                    days = [datetime.date(year, month, day).strftime(dateFormat) for day in range(1, num_days + 1)]
                    for dates in days:
                        data[dates] = 0

                    if (len(list(filtered_data)) > 0):
                        for items in filtered_data:
                            # print("report -- ", items)
                            # adding all sold data
                            data[items.invoice_date.strftime(dateFormat)] += items.total_amount

                    sorted_data = {}
                    for key in sorted(data):
                        # print (key, data[key])
                        sorted_data[key] = data[key]
                    return Response({"data": sorted_data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChartDataInvoiceByCreated(APIView):

    def get(self, request):
        try:
            filter_by = request.GET.get("filter", "week")
            is_custom = request.GET.get("is_custom","false")

            if (filter_by == "week"):
                '''
                # /api/v1/sales/date/?filter=week
                if /api/v1/sales/date/ default will be current week

                '''
                today = date.today()
                start_number = getNumberofDays()
                weeek_started = today - timedelta(days=start_number)
                todays_data = today + timedelta(days=1)  # so that it includes in the result
                print("============")
                print("weeek_started", weeek_started)
                print("todays_data", todays_data)
                print("============")
                # filtered_data =  Invoice_Products.objects.all()

                if is_custom == "true":
                    filtered_data =  Invoice.objects.filter(invoice_date__range=[weeek_started, todays_data],is_custom=True)
                else:
                    filtered_data =  Invoice.objects.filter(invoice_date__range=[weeek_started, todays_data],
                    is_custom=False
                    )

                delta = datetime.timedelta(days=1)

                data = {
                    "Saturday": 0,
                    "Sunday": 0,
                    "Monday": 0,
                    "Tuesday": 0,
                    "Wednesday": 0,
                    "Thursday": 0,
                    "Friday": 0,

                }

                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.invoice_date.strftime('%A')] += 1  # adding all sold data
                        # data[items.created_at.strftime('%d/%m/%Y')] += items.product.total_amount  # adding all sold data

                    return Response({"data": data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)

            if (filter_by == "month"):
                '''
                # /api/v1/sales/date/?filter=month?month=9
                if /api/v1/sales/date/?filter=month default will be current month
                '''
                today = datetime.datetime.today()
                year = today.year
                month = today.month
                filter_month = request.GET.get("month", month)
                if is_custom == "true":
                    filtered_data =  Invoice.objects.filter(invoice_date__year__gte=year,
                                                                                invoice_date__month__gte=filter_month,
                                                                                invoice_date__year__lte=year,
                                                                                invoice_date__month__lte=filter_month,is_custom=True)
                else:
                    filtered_data =  Invoice.objects.filter(invoice_date__year__gte=year,
                                                              invoice_date__month__gte=filter_month,
                                                              invoice_date__year__lte=year,
                                                              invoice_date__month__lte=filter_month,
                                                                is_custom=False
                                                              
                                                              )
                data = {}
                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.invoice_date.strftime(dateFormat)] = 0  # intialized 0 to all date
                    now = datetime.datetime.now()
                    year = now.year
                    month = now.month
                    num_days = calendar.monthrange(year, month)[1]
                    days = [datetime.date(year, month, day).strftime(dateFormat) for day in range(1, num_days + 1)]
                    for dates in days:
                        data[dates] = 0

                    if (len(list(filtered_data)) > 0):
                        for items in filtered_data:
                            # print("report -- ", items)
                            # adding all sold data
                            data[items.invoice_date.strftime(dateFormat)] += 1

                    sorted_data = {}
                    for key in sorted(data):
                        # print (key, data[key])
                        sorted_data[key] = data[key]
                    return Response({"data": sorted_data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChartDataCustomer(APIView):

    def get(self, request):
        try:
            filter_by = request.GET.get("filter", "week")
            if (filter_by == "week"):
                '''
                # /api/v1/sales/date/?filter=week
                if /api/v1/sales/date/ default will be current week

                '''
                today = date.today()
                start_number = getNumberofDays()
                weeek_started = today - timedelta(days=start_number)
                todays_data = today + timedelta(days=1)  # so that it includes in the result
                print("============")
                print("weeek_started", weeek_started)
                print("todays_data", todays_data)
                print("============")
                # filtered_data =  Invoice_Products.objects.all()
                filtered_data = Customer.objects.filter(created_at__range=[weeek_started, todays_data])
                print("weekly filtered data", filtered_data)
                delta = datetime. timedelta(days=1)

                data = {
                    "Saturday": 0,
                    "Sunday": 0,
                    "Monday": 0,
                    "Tuesday": 0,
                    "Wednesday": 0,
                    "Thursday": 0,
                    "Friday": 0,
                }

                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.created_at.strftime('%A')] += 1  # adding all sold data
                        # data[items.created_at.strftime('%d/%m/%Y')] += items.product.total_amount  # adding all sold data

                    return Response({"data": data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)

            if (filter_by == "month"):
                '''
                # /api/v1/sales/date/?filter=month?month=9
                if /api/v1/sales/date/?filter=month default will be current month
                '''
                today = datetime.datetime.today()
                year = today.year
                month = today.month
                filter_month = request.GET.get("month", month)
                filtered_data = Customer.objects.filter(created_at__year__gte=year,
                                                        created_at__month__gte=filter_month,
                                                        created_at__year__lte=year,
                                                        created_at__month__lte=filter_month)
                data = {}
                if (len(list(filtered_data)) > 0):
                    for items in filtered_data:
                        data[items.created_at.strftime(dateFormat)] = 0  # intialized 0 to all date
                    now = datetime.datetime.now()
                    year = now.year
                    month = now.month
                    num_days = calendar.monthrange(year, month)[1]
                    days = [datetime.date(year, month, day).strftime(dateFormat) for day in range(1, num_days + 1)]
                    for dates in days:
                        data[dates] = 0

                    if (len(list(filtered_data)) > 0):
                        for items in filtered_data:
                            # print("report -- ", items)
                            # adding all sold data
                            data[items.created_at.strftime(dateFormat)] += 1

                    sorted_data = {}
                    for key in sorted(data):
                        # print (key, data[key])
                        sorted_data[key] = data[key]
                    return Response({"data": sorted_data}, status=status.HTTP_200_OK)
                else:
                    return Response({"data":[]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SaveAndSendPdf(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # invoice =  Invoice.objects.get
        instance =  Invoice.objects.filter().first()

        params = {}
        params['is_custom'] = instance.is_custom
        params['number'] = instance.number
        params['barcode'] = instance.barcode
        params['barcode_text'] = instance.barcode_text
        params['invoice_date'] = instance.invoice_date
        params['bill_from'] = instance.bill_from
        params['bill_to'] = instance.bill_to
        params['from_email'] = instance.from_email
        params['to_email'] = instance.to_email
        params['from_mobile'] = instance.from_mobile
        params['to_mobile'] = instance.to_mobile
        params['from_address'] = instance.from_address
        params['to_address'] = instance.to_address
        params['delivery_type'] = instance.delivery_type
        params['delivery_charge'] = instance.delivery_charge
        params['delivery_charge_type'] = instance.delivery_charge_type
        params['payment_type'] = instance.payment_type
        params['delivery_statu s'] = instance.delivery_status
        params['total_due'] = instance.total_due
        params['total_paid'] = instance.total_paid
        params['total_amount'] = instance.total_amount
        params['total_discount'] = instance.total_discount
        params['payment_status'] = instance.payment_status
        params['notes'] = instance.notes
        params['payment_status'] = instance.payment_status
        params['total_due'] = instance.total_due
        params['total_paid'] = instance.total_paid
        params['total_amount'] = instance.total_amount
        params['total_discount'] = instance.total_discount
        params['delivery_type'] = instance.delivery_type
        params['invoice_view_json'] = instance.invoice_view_json
        params['header_image_url'] = "http://ims-backend.kaaruj.cloud/media/default/KAARUJ_PDF_Header.png"
        params['default_image'] = "http://ims-backend.kaaruj.cloud/media/default/product-default.png"
        data = request.data
        import logging
        logger = logging.getLogger('django')
        logger.error(f'-----------test------------------')
        logger.error(f'params : {params}')
        logger.error(f'delivery charge {instance.delivery_charge}')
        logger.error(f'-----------test------------------')
        subtotal = 0
        for i in instance.invoice_view_json:
            subtotal += i['total']

        params['subtotal'] = subtotal

        file_name, status = save_pdf(params)
        if not status:
            return Response({"error": "error"})
        return HttpResponse(file_name)
    
from sales.models import Notification

class NotificationView(APIView):
    def get(self, request):
        user = self.request.user

        # Filter notifications by the current user
        notifications = Notification.objects.filter(user=user)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)