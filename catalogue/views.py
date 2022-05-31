from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from django.db.models import Q

import datetime

from .forms import CustomUserCreationForm
from .models import Item, ItemInstance
# Create your views here.


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# rents an item
def rent_item(request, item_slug):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        item = Item.objects.get(slug=item_slug)
        group = Group.objects.filter(user=request.user).first().name
        instances = ItemInstance.objects.filter(item=item, status="Instance")
        holds = ItemInstance.objects.filter(item=item, status="Hold")
        reserves = ItemInstance.objects.filter(item=item, status="Reserve")
        available_copies = item.copies - instances.count()
        for i in range(1):
            if instances.filter(renter=request.user).count() != 0:
                break
            elif instances.count() >= item.copies:
                break
            elif (reserves.count() != 0) or ((holds.count() >= available_copies) and (holds.first().renter != request.user)):
                break
            elif group == "Student" and ItemInstance.objects.filter(renter=request.user).count() >= 5:
                break
            elif group == "Instructor" and ItemInstance.objects.filter(renter=request.user).count() >= 8:
                break
            else:
                if holds.filter(renter=request.user).count() != 0:
                    instance = holds.get(renter=request.user)
                    instance.delete()
                ItemInstance.objects.create(item=item, due_date=datetime.date.today() + datetime.timedelta(14), status="Instance", renter=request.user)
        return redirect('item', item_slug=item_slug)


# returns an item
def return_item(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        item = ItemInstance.objects.get(id=item_id)
        item.delete()
        return redirect('borrowed')


def renew_item(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        instance = ItemInstance.objects.get(id=item_id)
        due_date = instance.due_date
        for i in range(1):
            if due_date - datetime.date.today() > datetime.timedelta(days=3):
                break
            elif ItemInstance.objects.filter(item=instance.item, status="Reserve").count() != 0:
                break
            elif ItemInstance.objects.filter(item=instance.item, status="Hold") != 0:
                break
            else:
                new_due_date = due_date + datetime.timedelta(14)
                instance.due_date = new_due_date
                instance.save()
        return redirect('borrowed')


# requests to put an item on hold
def request_hold(request, item_slug):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        item = Item.objects.get(slug=item_slug)
        instances = ItemInstance.objects.filter(item=item, status="Instance")
        holds = ItemInstance.objects.filter(item=item, status="Hold")
        reserves = ItemInstance.objects.filter(item=item, status="Reserve")
        for i in range(1):
            if instances.filter(renter=request.user).count() != 0:
                break
            elif holds.filter(renter=request.user).count() != 0:
                break
            elif reserves.count() == 0 and (item.copies > instances.count()) and ((item.copies - instances.count()) > holds.count()):
                break
            else:
                ItemInstance.objects.create(item=item, status="Hold", renter=request.user)
        return redirect('item', item_slug=item_slug)


# reserve an item
def reserve_item(request, item_slug):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        item = Item.objects.get(slug=item_slug)
        group = Group.objects.filter(user=request.user).first().name
        reserves = ItemInstance.objects.filter(item=item, status="Reserve")
        for i in range(1):
            if group == "Student":
                break
            elif reserves.filter(renter=request.user).count() >= 5:
                break
            else:
                ItemInstance.objects.create(item=item, status="Reserve", renter=request.user)
        return redirect('item', item_slug=item_slug)


# in progress
def library_view(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        template = 'catalogue/library.html'
        item_list = Item.objects.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(item_list, 12)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {'items': items}
        return render(request, template, context)


# searches for an item
def search(request):
    template = 'catalogue/library.html'
    query = request.GET.get('q')
    if query:
        results = Item.objects.filter(
            Q(title__icontains=query) or
            Q(author__first_name__icontains=query) or
            Q(author__last_name__icontains=query) or
            Q(summary__icontains=query)
        )
    else:
        results = Item.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 12)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {'items': items}
    return render(request, template, context)


# shows an item
def item_view(request, item_slug):
    query_object = get_object_or_404(Item, slug=item_slug)
    context = {'query_object': query_object}
    return render(request, 'catalogue/item.html', context)


# shows users rented items
def user_items_view(request):
    query_list = ItemInstance.objects.filter(renter=request.user, status="Instance")
    context = {'query_list': query_list}
    return render(request, 'catalogue/borrowed_items.html', context)


# show the users pending holds
def user_holds_view(request):
    query_list = ItemInstance.objects.filter(renter=request.user, status="Hold")
    context = {'query_list': query_list}
    return render(request, 'catalogue/borrowed_items.html', context)


# show items reserved by the user
def user_reserves_view(request):
    query_list = ItemInstance.objects.filter(renter=request.user, status="Reserve")
    context = {'query_list': query_list}
    return render(request, 'catalogue/borrowed_items.html', context)


# shows user profile
def profile_view(request):
    query_user = request.user
    query_user_group = Group.objects.filter(user=request.user).first().name
    query_username = query_user.username.split('.')
    context = {
        'query_user': query_user,
        'query_username': query_username[0].capitalize()+' '+query_username[1].capitalize(),
        'query_user_group': query_user_group
    }
    return render(request, 'catalogue/profile.html', context)


