
from coreapp.base import BaseModel,BaseModelActive
from coreapp.helper import *
from utility.utils import slug_utils,model_utils
from utility.utils.notification_utils import *
from . import constants
from django.core.validators import MaxValueValidator
from django.utils.functional import cached_property
from promotions.models import Offer
from promotions.constants import OfferType
from django.db import models
from django.conf import settings
from django.db.models import Q


class Products(BaseModelActive):
    pid = models.CharField(max_length=200,blank=True,null=True)
    name = models.CharField(max_length=200)
    main_category = models.SmallIntegerField(choices=constants.MainCategoryChoices.choices)
    category = models.ManyToManyField("inventory.Category")
    variant = models.ManyToManyField("inventory.Variant",blank=True)
    sku = models.CharField(max_length=200)
    # sku = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    stock = models.IntegerField()
    barcode = models.ImageField(upload_to='bar_codes/products/', blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/products/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(null=True, blank=True,)
    thumb = models.ForeignKey('coreapp.Document',on_delete=models.CASCADE,null=True,blank=True)
    thumb_resized = models.ImageField(upload_to='products/thumb_resized/', blank=True)
    feature_images = models.ManyToManyField('coreapp.Document',related_name="feature_images",blank=True)
    minimum_quantity = models.IntegerField(default=00)
    tags = models.ManyToManyField("inventory.Tags",blank=True)
    is_new_arrival = models.BooleanField(default=False)
    vendor_info = models.TextField(null=True, blank=True,)
    about_brand = models.TextField(null=True, blank=True,)
    shipping_info = models.TextField(null=True, blank=True,)
    variants_json = models.JSONField(null=True, blank=True,)

    
    # class Meta:
    #     ordering = ('?')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        model_utils.generate_product_barcode(self)

        if not self.id:
            pid_generated =  "KJP"+get_random_string(length=6, allowed_chars='1234567890')
            self.pid =pid_generated
            try:
                ProductNotification(self.name)
            except Exception as e:
                print_log(e)
        if not self.slug:
            self.slug = slug_utils.generate_unique_slug(self.name, self)
        # if not self.barcode:
            # text = f'{self.get_offer_price()}Tk  \n {self.name}  \n{self.pid}'
            # model_utils.generate_product_barcode(self)
        if not self.qr_code:
            text = f'{self.name} {self.get_offer_price()} \n{self.pid}'
            model_utils.generate_qrcode(self,text)

        if self.thumb and not self.thumb_resized:
            try:
                print("Resizing_12image",self.thumb.document.path)
                original_image = Image.open(self.thumb.document.path)
                max_size = (500, 500)  # Set the maximum size for the resized image
                original_image.thumbnail(max_size, Image.ANTIALIAS)
                resized_image_io = BytesIO()
                original_image.save(resized_image_io, format='JPEG',save=False)
                resized_image_content = ContentFile(resized_image_io.getvalue())
                self.thumb_resized.save(f'{self.slug}_resized.jpg', resized_image_content, save=False)
            except:
                print_log("Error in resizing image")
                pass
        return super(Products, self).save(*args, **kwargs)
    
    @cached_property
    def get_thumb_url(self):
        default_url = f"{settings.PLACEHOLDER_IMAGE}"
        # default_url = f"{settings.MEDIA_HOST}/media/default/products/default_kaaruj.jpg"
        return self.thumb.get_url if self.thumb else default_url
    @cached_property
    def get_thumb_resized_url(self):
        default_url = f"{settings.PLACEHOLDER_IMAGE}"
        return self.thumb_resized.get_url if self.thumb_resized else default_url
    def get_discount(self):
        offer = Offer.objects.filter(product=self).first()
        if offer:
            return offer.discount_value
        else:
            return 0
    def get_offer_price(self):
        import math
        offer = Offer.objects.filter(product=self).first()
        if offer:
            discount_type = offer.discount_type
            discount_value = offer.discount_value
            if discount_type == OfferType.PERCENTAGE:
                offer_price = math.ceil(self.price - (self.price * discount_value / 100))
            else:
                offer_price = math.ceil(self.price - discount_value)
        else:
            offer_price = math.ceil(self.price)
        return f"{offer_price:.1f}"

    def get_discount_type(self):
        offer = Offer.objects.filter(product=self).first()
        if offer:
            return offer.discount_type

    def get_discount_type_text(self):
        offer = Offer.objects.filter(product=self).first()
        if offer:
            return "%" if offer.discount_type==OfferType.PERCENTAGE else "৳"
        else:
            return "%"
        
    # @property
    # def get_attributes(self):
    #     attribute_values = self.variant.values_list('attribute_value__attribute', flat=True).distinct()
    #     attr_obj = []
    #     for attr in attribute_values:
    #         attr_obj.append(Attributes.objects.get(id=attr))
    #     return attr_obj
    
    # @property
    # def get_attributes_val(self):
    #     attribute_values = self.variant.attribute_value.all()
    #     return attribute_values
    # def today_total_amount(self):
    #     from datetime import datetime, timedelta
    #     from sales.models import Invoice
    #     today = datetime.today().date()
    #     start_date = datetime(today.year, today.month, today.day, 0, 0, 0)
    #     end_date = start_date + timedelta(days=1)
        
    #     invoices = Invoice.objects.filter(
    #     Q(invoice_date__range=(start_date, end_date)))
        
    #     total_amount = sum(invoice.total_amount for invoice in invoices)
    #     return total_amount
    
    def today_total_amount(self):
        from sales.models import Invoice_Products
        import datetime
        today = datetime.datetime.today()

        start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                       hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                     hour=23, minute=59, second=59)
        todays_invoices_productss = Invoice_Products.objects.filter(
            invoice_date__range=(start_date, end_date)).filter(product_id=self.id)
        total = 0
        for i in todays_invoices_productss:
            total += i.total
        return total

    def today_total_sales(self, product_id=None):

        from sales.models import Invoice_Products
        import datetime
        today = datetime.datetime.today()

        start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                       hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                     hour=23, minute=59, second=59)

        todays_invoices_productss = Invoice_Products.objects.filter(invoice__invoice_date__range=(start_date, end_date))
        todays_invoices_productss = todays_invoices_productss.filter(product_id=self.id)

        total = 0
        for i in todays_invoices_productss:
            total += i.quantity
        return total

    

class Variant(BaseModelActive):
    attribute_value = models.ManyToManyField("inventory.AttributeValue",blank=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    stock = models.IntegerField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    
class AttributeValue(BaseModel):
    attribute = models.ForeignKey("inventory.Attributes", on_delete=models.CASCADE,
                                    related_name="at_values")
    value = models.CharField(max_length=200)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.attribute.name + " - " + self.value


class Attributes(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('-created_at',)

    def get_values(self):
        return AttributeValue.objects.filter(attribute=self)

    def __str__(self):
        return self.name

class Tags(BaseModel):
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name



class Category(BaseModelActive):
    parent = models.ForeignKey("self", on_delete=models.SET_NULL,
                                    related_name="pt_category", null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    level = models.PositiveIntegerField(default=3,validators=[MaxValueValidator(5)])
    main_category = models.SmallIntegerField(choices=constants.MainCategoryChoices.choices)
    sub_main_category = models.ForeignKey("self", on_delete=models.SET_NULL,
                                    related_name="sub_main_category_new", null=True, blank=True)
    category_type = models.SmallIntegerField(choices=constants.CategoryType.choices)
    '''
    Level 1 = Main Category - Home decor, In style
    Level 2 = home decor - For dining,for living
              In style -  Casual Wears,Party Wears,Exclusive Wears,Footwears,For Couples,Kids Zones
    Level 3 = For dining - Dining table, Dining chair
              For living - Sofa, Sofa cum bed
              Casual Wears - T-shirts, Shirts
              e.t.c
    '''
    name = models.CharField(max_length=100)
    thumb = models.ForeignKey('coreapp.Document',on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name + " - Level : " + str(self.level)
    

    def count_products(self):
        return Products.objects.filter(category=self).count()
    
    def get_thumb_url(self):
        default_url = f"{settings.PLACEHOLDER_IMAGE}"
        return self.thumb.get_url if self.thumb else default_url
    
    def get_string_tree(self):
        category_tree = ""

        parent = self.parent
        while parent:
            if category_tree:
                category_tree = parent.name + " > " + category_tree
            else:
                category_tree = parent.name
            parent = parent.parent

        return category_tree

    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        
        if not self.slug:
            self.slug = slug_utils.generate_unique_slug(self.name, self)
          
        return super(Category, self).save(*args, **kwargs)



class Customer(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    mobile = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    # total_purchase = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    to_address = models.CharField(max_length=350)
    to_address2 = models.CharField(max_length=350, blank=True, null=True)
    to_zip_code = models.CharField(max_length=50, blank=True, null=True)
    to_city = models.CharField(max_length=50, blank=True, null=True)
    to_division = models.CharField(max_length=50, blank=True, null=True)
    to_district = models.CharField(max_length=50, blank=True, null=True)
    to_country = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slug_utils.generate_unique_slug(self.name, self)
        try:
            if self.id == None:
                CustomerNotifications_OnCreate(self.name)

            else:
                CustomerNotifications_OnUpdate(self.name)

        except Exception as e:
            print_log("Customer Notification Error",str(e))
        
        return super(Customer, self).save(*args, **kwargs)
    


    @property
    def get_products_text(self):
        from sales.models import Invoice
        invoices =  Invoice.objects.filter(to_mobile=self.mobile)
        inv_products = []
        for i in invoices:
            for inv_prod in i.invoice_products.all():
                inv_products.append(inv_prod)
        
        products_text = ""
        for inv in inv_products:
                name = inv.product.name if inv.product else inv.product_name
                name = f"{name} - {inv.variant_name}" 
                products_text += f'{name} - {inv.quantity} - {inv.total} \n'
        return products_text

    
    @property
    def total(self):
        from sales.models import Invoice
        todays_invoices = Invoice.objects.filter(to_mobile=self.mobile)
        total = 0
        for i in todays_invoices:
            total += i.total_amount
        return total
    
    @property
    def total_purchase_method(self):
        from sales.models import Invoice
        total_amount = Invoice.objects.filter(to_mobile=self.mobile).aggregate(models.Sum('total_amount'))
        return total_amount['total_amount__sum'] if total_amount['total_amount__sum'] is not None else 0

    @property
    def invoice_count_method(self):
        from sales.models import Invoice
        total_amount = Invoice.objects.filter(to_mobile=self.mobile).count()
        return total_amount

    def total_purchase(self, customer_phone=None, filter_by="all"):

        from sales.models import Invoice
        import datetime

        if(filter_by == "all"):
            todays_invoices = Invoice.objects.filter(to_mobile=customer_phone)
            total = 0
            for i in todays_invoices:
                total += i.total_amount
            return total

        if(filter_by == "today"):
            today = datetime.datetime.today()

            start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                           hour=0, minute=0, second=0)  # represents 00:00:00
            end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                         hour=23, minute=59, second=59)

            todays_invoices = Invoice.objects.filter(
                Q(invoice_date__range=(start_date, end_date)) & Q(to_mobile=customer_phone))
            total = 0
            for i in todays_invoices:
                total += i.total_amount
            return total

        if(filter_by == "week"):
            today = datetime.date.today()
            from utility.utils.filter_utils import getNumberofDays
            start_number = getNumberofDays()
            weeek_started = today - datetime.timedelta(days=start_number)
            todays_data = today + datetime.timedelta(days=1)  # so that it includes in the result

            invoices = Invoice.objects.filter(
                Q(invoice_date__range=(weeek_started, todays_data)) & Q(to_mobile=customer_phone))
            total = 0
            for i in invoices:
                total += i.total_amount
            return total

        if(filter_by == "month"):
            year = datetime.datetime.today().year
            month = datetime.date.today().month

            invoices = Invoice.objects.filter(invoice_date__year__gte=year,
                                              invoice_date__month__gte=month,
                                              invoice_date__year__lte=year,
                                              invoice_date__month__lte=month)

            invoices = invoices.filter(
                Q(to_mobile=customer_phone))
            total = 0
            for i in invoices:
                total += i.total_amount
            return total

    def invoice_count(self, customer_phone=None, filter_by="all"):
        from sales.models import Invoice
        import datetime
        from utility.utils.filter_utils import getNumberofDays

        if(filter_by == "all"):
            return Invoice.objects.filter(to_mobile=customer_phone).count()

        if(filter_by == "today"):

            from sales.models import Invoice
            import datetime
            today = datetime.datetime.today()

            start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                           hour=0, minute=0, second=0)  # represents 00:00:00
            end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                         hour=23, minute=59, second=59)

            invoices_count = Invoice.objects.filter(
                Q(invoice_date__range=(start_date, end_date)) & Q(to_mobile=customer_phone)).count()

            return invoices_count

        if(filter_by == "week"):
            today = datetime.date.today()
            start_number = getNumberofDays()
            weeek_started = today - datetime.timedelta(days=start_number)
            todays_data = today + datetime.timedelta(days=1)  # so that it includes in the result

            invoices_count = Invoice.objects.filter(
                Q(invoice_date__range=(weeek_started, todays_data)) & Q(to_mobile=customer_phone)).count()

            return invoices_count

        if(filter_by == "month"):
            year = datetime.date.today().year
            month = datetime.date.today().month

            invoices_count = Invoice.objects.filter(Q(invoice_date__year__gte=year,
                                                      invoice_date__month__gte=month,
                                                      invoice_date__year__lte=year,
                                                      invoice_date__month__lte=month) & Q(to_mobile=customer_phone)).count()

            return invoices_count

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


