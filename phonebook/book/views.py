from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages

from .models import Person, Phone, Email
from .forms import PersonForm, PhoneForm, EmailForm

import re

# widok z lista osob
def person_list_view(request):
    queryset = Person.objects.all()
    context = {
        'person_list' : queryset,
    }
    return render(request, 'book/person_list.html', context)

# widok z pogladem na pojedyncza osobe
def person_detail_view(request, id_person):
    try:
        person = Person.objects.get(pk=id_person)
    except Person.DoesNotExist:
        raise Http404
    try:
        numbers = Phone.objects.filter(person=person)
    except Phone.DoesNotExist:
        messages.info(request, 'Ta osoba nie ma jeszcze dodanych numerow telefonu.')
    try:
        emails = Email.objects.filter(person=person)
    except Email.DoesNotExist:
        messages.info(request, 'Ta osoba nie ma jeszcze dodanych emaili.')    
     
    context = {
        'person': person,
        'number_list': numbers,
        'email_list': emails
    }
    return render(request, 'book/person_detail.html', context)

# widok usuniecia osoby z ksiazki telefonicznej
def person_delete_view(request, id_person):
    obj = get_object_or_404(Person, pk=id_person)
    if Phone.objects.filter(person=id_person).union(Email.objects.filter(person=id_person)):
        return redirect('../../')
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        'object': obj
    }
    return render(request, 'book/person_delete.html', context)

# widok zmiany istniejacej osoby
def person_update_view(request, id_person):
    obj = get_object_or_404(Person, pk=id_person)
    form = PersonForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('../')
    context = {
        'form': form,
        'person': obj
    }
    return render(request, 'book/person_update.html', context)

# widok z tworzeniem nowej osoby
def person_create_view(request):
    initial_data = {
        'name': "Wpisz tutaj imie",
        'surname': "Wpisz tutaj nazwisko"
    }
    form = PersonForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        form.save()
        return redirect('../')
    context = {
        'form' : form
    }
    return render(request, 'book/person_create.html', context)

# widok dodania maila do osoby
def email_add_view(request, id_person):
    form = EmailForm(id_person, request.POST)
    if request.method == "POST":
        if form.is_valid:
            form.save()
            return redirect('../')
    context = {
        'form': form
    }
    return render(request, 'book/email_add.html', context)

# widok dodania telefonu do osoby
def phone_add_view(request, id_person):
    form = PhoneForm(id_person, request.POST)
    if request.method == "POST":
        if form.is_valid:
            form.save()
            return redirect('../')

    context = {
        'form': form
    }
    return render(request, 'book/phone_add.html', context)

# usuniecie telefonu u osoby
def phone_delete_view(request, id_person, id_phone):
    obj = get_object_or_404(Phone, pk=id_phone)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')

    context = {
        'object': obj
    }
    return render(request, 'book/person_detail.html', context)

# usuniecie emaila u osoby
def email_delete_view(request, id_person, id_email):
    obj = get_object_or_404(Email, pk=id_email)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')

    context = {
        'object': obj
    }
    return render(request, 'book/person_detail.html', context)

# widok z wyszukiwaniem
def search_view(request):
    if request.method == "GET":
        search_query = request.GET.get('search', None)
        # jaki typ danych zostal wprowadzony do pola wyszukiwania
        has_digits = re.search("[0-9]", search_query)
        has_letters = re.search("[a-z]", search_query)
        has_atsign = re.search("@", search_query)
        # jezeli ma cyfry i nie posiada liter szukaj po emailach i numerach telefonu
        if has_digits and not has_letters:
            results_email = Email.objects.filter(email__contains=search_query)
            results_person_email = results_email.values('person')
            results_phone = Phone.objects.filter(phone__contains=search_query)
            results_person_phone = results_phone.values('person')
            # laczenie wynikow
            results_person_ids = results_person_email.union(results_person_phone)
            # wydostaje uzytkownikow ze znalezionych id
            person_ids = set( val for dic in results_person_ids.values('person') for val in dic.values())
            results_person = Person.objects.filter(id__in=person_ids)
        # jezeli ma (cyfry i litery) lub znak "@" to szukaj jedynie po emailach
        elif has_digits and has_letters or has_atsign:
            results_email = Email.objects.filter(email__contains=search_query)
            results_person_ids = results_email.values('person')
            # wydostaje uzytkownikow ze znalezionych id
            person_ids = set( val for dic in results_person_ids.values('person') for val in dic.values())
            results_person = Person.objects.filter(id__in=person_ids)
        # jezeli ma tylko litery szukaj po emailach, imieniu i nazwisku
        else:
            results_name = Person.objects.filter(name__icontains=search_query)
            results_surname = Person.objects.filter(surname__icontains=search_query)
            results_email = Email.objects.filter(email__contains=search_query)
            # wydostaje uzytkownikow ze znalezionych emaili
            person_ids = set( val for dic in results_email.values('person') for val in dic.values())
            results_email_person = Person.objects.filter(id__in=person_ids)
            # lacze wyniki wyszukiwania po name i surname
            results_person = results_name.union(results_surname)
            # lacze wyniki wyszukiwania z emailem
            results_person = results_person.union(results_email_person)
        
    context = {
        'person_list': results_person,
        'search_query': search_query
    }    
    return render(request, 'book/person_list.html', context)