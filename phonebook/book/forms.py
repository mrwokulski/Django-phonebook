from django import forms
from .models import Person, Email, Phone


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person 
        fields = (
            'name',
            'surname'
        )


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = (
            'phone',
            'person'
        )

    def __init__(self, person_id, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['person'] = forms.ModelChoiceField(
            queryset=Person.objects.filter(pk=person_id),
            initial=Person.objects.filter(pk=person_id).first()
            ) 
        self.fields['phone'] = forms.IntegerField(max_value=999999999)


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = (
            'email',
            'person'
        )

    def __init__(self, person_id, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['person'] = forms.ModelChoiceField(
            queryset=Person.objects.filter(pk=person_id),
            initial=Person.objects.filter(pk=person_id).first()
            )  
        self.fields['email'] = forms.EmailField()
