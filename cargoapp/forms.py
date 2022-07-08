from django import forms
 
class RouteForm(forms.Form):

	# inputUid = forms.CharField(max_length = 36)
	inputFrom_date = forms.DateField(required=False)
	inputTo_date = forms.DateField(required=False)
	inputA_point = forms.CharField(max_length = 150, required=False)
	inputB_point = forms.CharField(max_length = 150, required=False)
	inputRoute_length = forms.CharField(max_length = 15, required=False)
	inputRoute_cost = forms.CharField(max_length = 15, required=False)
	inputExpenses_1 = forms.CharField(max_length = 15, required=False)
	inputVehicle = forms.CharField(max_length = 36, required=False)
	inputLogist = forms.CharField(max_length = 36, required=False)
	inputDriver = forms.CharField(max_length = 36, required=False)
	inputOrganization = forms.CharField(max_length = 36, required=False)
	inputWeight = forms.CharField(max_length = 15, required=False)

	inputContragent = forms.CharField(max_length = 36, required=False)
	inputContract = forms.CharField(max_length = 36, required=False)

	inputBanner_all = forms.BooleanField(required=False)
	inputBanner_side = forms.BooleanField(required=False)
	inputControl_penalty = forms.BooleanField(required=False)

	inputStraight_boolean = forms.BooleanField(required=False)

	inputDescription = forms.CharField(max_length = 256, required=False)
	inputRequest_number = forms.CharField(max_length = 30, required=False)

	inputRequest_img = forms.FileField(required=False)
	inputLoa_img = forms.FileField(required=False)

	inputSaveAndExit_boolean = forms.BooleanField(required=False)

	inputBanner_a = forms.BooleanField(required=False)
	inputBanner_b = forms.BooleanField(required=False)
	inputPayment_type = forms.CharField(max_length = 1, required=False)

class FilterForm(forms.Form):
	columnar = forms.CharField(max_length = 36, required=False)
	status = forms.CharField(max_length = 36, required=False)