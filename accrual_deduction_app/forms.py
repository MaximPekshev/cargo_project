from django import forms
 
class AccrualDeductionForm(forms.Form):

    input_date = forms.DateField(required=False)
    input_sum = forms.CharField(max_length = 15, required=False)
    input_vehicle = forms.CharField(max_length = 36, required=False)
    input_reason = forms.CharField(max_length = 36, required=False)
    input_type = forms.CharField(max_length = 36, required=False)

	