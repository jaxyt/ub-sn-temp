from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.


class Auction(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='auctions', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    watched = models.ManyToManyField(Profile, blank=True, related_name='watches')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='auctions')
    # additional fields
    name = models.TextField()
    duration = models.IntegerField(blank=True, null=True)
    terms = models.TextField(blank=True, null=True)
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    winning_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='winners', blank=True, null=True)

    def __str__(self):
        return str(self.content[:20])

    def num_watches(self):
        return self.watched.all().count()

    def num_bids(self):
        return self.bid_set.all().count()

    class Meta:
        ordering = ('-created',)


class Bid(models.Model):
    bidder = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    body = models.TextField(max_length=300, blank=True, default="user")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # additional fields
    current_bid_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    max_bid_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.pk)


WATCH_CHOICES = (
    ('Watch', 'Watch'),
    ('Unwatch', 'Unwatch'),
)


class Watch(models.Model): 
    watcher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    value = models.CharField(choices=WATCH_CHOICES, max_length=10)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.watcher}-{self.auction}-{self.value}"

