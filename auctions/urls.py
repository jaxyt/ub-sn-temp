from django.urls import path
from .views import auction_bid_create_and_list_view, watch_unwatch_auction, AuctionDeleteView, AuctionUpdateView

app_name = 'auctions'

urlpatterns = [
    path('', auction_bid_create_and_list_view, name='main-auction-view'),
    path('watched/', watch_unwatch_auction, name='watch-auction-view'),
    path('<pk>/delete/', AuctionDeleteView.as_view(), name='auction-delete'),
    path('<pk>/update/', AuctionUpdateView.as_view(), name='auction-update'),
]
