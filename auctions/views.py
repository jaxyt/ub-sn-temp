from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Auction, Watch
from profiles.models import Profile
from .forms import AuctionModelForm, BidModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


@login_required
def auction_bid_create_and_list_view(request):
    qs = Auction.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    a_form = AuctionModelForm()
    b_form = BidModelForm()
    auction_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_a_form' in request.POST:
        print(request.POST)
        a_form = AuctionModelForm(request.POST, request.FILES)
        if a_form.is_valid():
            instance = a_form.save(commit=False)
            instance.owner = profile
            instance.save()
            a_form = AuctionModelForm()
            auction_added = True

    if 'submit_b_form' in request.POST:
        b_form = BidModelForm(request.POST)
        if b_form.is_valid():
            instance = b_form.save(commit=False)
            instance.bidder = profile
            instance.auction = Auction.objects.get(id=request.POST.get('auction_id'))
            instance.save()
            b_form = BidModelForm()


    context = {
        'qs': qs,
        'profile': profile,
        'a_form': a_form,
        'b_form': b_form,
        'auction_added': auction_added,
    }

    return render(request, 'auctions/main.html', context)



@login_required
def watch_unwatch_auction(request):
    user = request.user
    if request.method == 'POST':
        auction_id = request.POST.get('auction_id')
        auction_obj = Auction.objects.get(id=auction_id)
        profile = Profile.objects.get(user=user)

        if profile in auction_obj.watched.all():
            auction_obj.watched.remove(profile)
        else:
            auction_obj.watched.add(profile)

        watch, created = Watch.objects.get_or_create(watcher=profile, auction_id=auction_id)

        if not created:
            if watch.value=='Watch':
                watch.value='Unwatch'
            else:
                watch.value='Watch'
        else:
            watch.value='Watch'

            auction_obj.save()
            watch.save()

        # data = {
        #     'value': watch.value,
        #     'watches': auction_obj.watched.all().count()
        # }

        # return JsonResponse(data, safe=False)
    return redirect('auctions:main-auction-view')



class AuctionDeleteView(LoginRequiredMixin, DeleteView):
    model = Auction
    template_name = 'auctions/confirm_del.html'
    success_url = reverse_lazy('auctions:main-auction-view')
    # success_url = '/auctions/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Auction.objects.get(pk=pk)
        if not obj.owner.user == self.request.user:
            messages.warning(self.request, 'You need to be the owner of the auction in order to delete it')
        return obj



class AuctionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AuctionModelForm
    model = Auction
    template_name = 'auctions/update.html'
    success_url = reverse_lazy('auctions:main-auction-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.owner == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the owner of the auction in order to update it")
            return super().form_invalid(form)

