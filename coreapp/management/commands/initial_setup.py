from django.core.management.base import BaseCommand

from .utils import setup_utils
from utility.utils.printer_utils import convert_zpl
from inventory.models import Products

class Command(BaseCommand):
    help = 'Initial configuration and settings for application'

    def handle(self, *args, **kwargs):
        # setup_utils.load_geo_json()
        demo_item = Products.objects.get(id=40)
        print(convert_zpl(demo_item.barcode.path))
        
