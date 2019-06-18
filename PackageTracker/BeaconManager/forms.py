from django import forms
from BeaconManager.models import Layout

LAYOUTS = Layout.objects.all().values_list('id', 'name')

class LayoutForm(forms.Form):
    """A Django Forms Class for layout form"""
    layout_name = forms.CharField(label="Layout Name", widget=forms.Select(choices=LAYOUTS), required=True)
