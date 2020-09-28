from django import forms
from .models import Auction, Bid


class AuctionModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Auction
        fields = ('content', 'image', 'name', 'start_price')


class BidModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a bid...'}))
    class Meta:
        model = Bid
        fields = ('body', 'max_bid_price')
