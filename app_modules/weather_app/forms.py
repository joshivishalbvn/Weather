from django import forms
from .models import City
from django_select2 import forms as s2forms

class CityWidget(s2forms.ModelSelect2Widget):
    
    model = City
    search_fields = [
        "name__icontains",
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-minimum-input-length"] = 0 
        attrs["data-allow-clear"] = True 
        return attrs

class CityForm(forms.Form):

    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by("name"),
        widget=CityWidget
    )

    class Meta:
        fields = ("city",)