from django import forms
from BeaconManager.models import Layout, Node

LAYOUTS = Layout.objects.all().values_list('id', 'name')

class LayoutForm(forms.Form):
    """A Django Forms Class for layout selection form"""
    layout_name = forms.CharField(label="Layout Name", widget=forms.Select(choices=LAYOUTS), required=True)

NODES = Node.objects.all().values_list('id', 'node_id')

class NodeSelectForm(forms.Form):
    """A Django Forms Class for node selection form"""
    node_name = forms.CharField(label="Node Name/Mac", widget=forms.Select(choices=NODES), required=True)