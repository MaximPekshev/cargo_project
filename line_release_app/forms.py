from django import forms

class LineReleaseForm(forms.Form):
    
    input_release_date = forms.DateTimeField(required=False)
    input_vehicle = forms.CharField(max_length = 36, required=False)
    input_trailer = forms.CharField(max_length = 36, required=False)
    input_driver = forms.CharField(max_length = 36, required=False)
    input_renewal = forms.BooleanField(required=False)
    input_for_repair = forms.BooleanField(required=False)

