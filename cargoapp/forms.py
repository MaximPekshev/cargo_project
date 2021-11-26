from django import forms
 
class RouteForm(forms.Form):

	# inputUid = forms.CharField(max_length = 36)
	inputFrom_date = forms.DateField(required=False)
	inputTo_date = forms.DateField(required=False)
	inputA_point = forms.CharField(max_length = 30, required=False)
	inputB_point = forms.CharField(max_length = 30, required=False)
	inputRoute_length = forms.CharField(max_length = 15, required=False)
	inputRoute_cost = forms.CharField(max_length = 15, required=False)
	inputExpenses_1 = forms.CharField(max_length = 15, required=False)
	inputVehicle = forms.CharField(max_length = 36, required=False)
	inputLogist = forms.CharField(max_length = 36, required=False)
	inputDriver = forms.CharField(max_length = 36, required=False)
	inputСlient = forms.CharField(max_length = 55, required=False)
	inputItems_count = forms.CharField(max_length = 3, required=False)
	inputWeight = forms.CharField(max_length = 15, required=False)
	inputVolume = forms.CharField(max_length = 15, required=False)
	inputWidth = forms.CharField(max_length = 15, required=False)
	inputHeight = forms.CharField(max_length = 15, required=False)
	inputDepth = forms.CharField(max_length = 15, required=False)

	inputDescription = forms.CharField(max_length = 256, required=False)
	inputRequest_number = forms.CharField(max_length = 30, required=False)

	