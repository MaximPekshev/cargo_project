from django import forms
 
class ScheduledRepairForm(forms.Form):

    service_work_type = forms.CharField(max_length = 36, required=False)
    vehicle = forms.CharField(max_length = 36, required=False)
    title = forms.CharField(max_length = 150, required=False)
    date_from = forms.DateTimeField(required=False)
    date_to = forms.DateTimeField(required=False)
    date_from_logist = forms.DateTimeField(required=False)
    sto = forms.CharField(max_length = 36, required=False)
    comment = forms.CharField(max_length = 1024, required=False)
    status = forms.CharField(max_length = 36, required=False)