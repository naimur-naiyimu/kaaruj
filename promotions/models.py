from django.db import models
from coreapp.base import BaseModel
from . import constants
from utility.utils import model_utils
# Create your models here.
class Offer(BaseModel):
  offer_id = models.CharField(max_length=20,blank=True,null=True)
  name = models.CharField(max_length=200)
  category = models.ManyToManyField("inventory.Category",blank=True)
  product = models.ManyToManyField("inventory.Products",blank=True)
  banner = models.ForeignKey("coreapp.Document",on_delete=models.SET_NULL,null=True,blank=True)
  description = models.TextField()
  discount_type = models.SmallIntegerField(choices=constants.OfferType.choices,default=constants.OfferType.PERCENTAGE)
  discount_value = models.IntegerField(default=0.00)
  start_date = models.DateTimeField()
  expiry_date = models.DateTimeField()
  is_active = models.BooleanField(default=True)

  @property
  def discount_type_name(self):
    return "%" if self.discount_type == constants.OfferType.PERCENTAGE else "৳"
  
  def get_banner_url(self):
    return self.banner.get_url if self.banner else ""

  def __str__(self) -> str:
    return self.name

  def save(self, *args, **kwargs):
    if not self.id :
      self.offer_id = model_utils.get_code(Offer)
    super(Offer, self).save(*args, **kwargs)
    


class Wishlist(BaseModel):
    user = models.ForeignKey("coreapp.User", on_delete=models.CASCADE,
                                    related_name="user_wishlist")
    product = models.ForeignKey("inventory.Products", on_delete=models.CASCADE,
                                    related_name="product_wishlist")
    variant = models.ForeignKey("inventory.Variant", on_delete=models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField(default=True)
   
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.get_full_name + " - " + self.product.name
    



class Review(BaseModel):
  product = models.ForeignKey("inventory.Products", on_delete=models.CASCADE,blank=True,null=True)
  star = models.SmallIntegerField(default=0) 
  reviewed_by = models.ForeignKey("coreapp.User", on_delete=models.CASCADE)
  photos = models.ManyToManyField('coreapp.Document', related_name='review_photos',null=True,blank=True)
  descriptions = models.TextField()
  is_active = models.BooleanField(default=True)


  def __str__(self):
    return self.reviewed_by.get_full_name + " - " + self.product.name