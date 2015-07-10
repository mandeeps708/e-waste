from django import forms
from waste.src.models import *
from django.db.models import Q
import datetime
from functools import partial
from bootstrap3_datetime.widgets import DateTimePicker

class DateRangeSelectionForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    # date2 = forms.DateField(
    # 	widget=DateTimePicker(options={"format": "YYYY-MM-DD",
    # 									"pickTime": False}))

class DepartmentSelect(forms.Form):
	select_department = forms.ModelChoiceField(queryset=Department.objects.all())
	def __init__(self, *args, **kwargs):
		super(DepartmentSelect, self).__init__(*args, **kwargs)
		self.fields['select_department'].widget.attrs={'id': 'department','class':'btn btn-default dropdown-toggle'}

class WasteGeneratedForm(forms.ModelForm):
	#try:
		#generated_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		#generated_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
	quantity = forms.FloatField()
	#except:
		#pass

	class Meta:
		model = WasteGenerated
		#exclude = ['department',]
		
		fields = ["quantity", "category", "description","department"]
		widgets = {
      'category': forms.HiddenInput(),
	  'description': forms.HiddenInput(),
	  'department': forms.HiddenInput(),
	
    }


class WasteStoredForm(forms.Form):
	try:
		stored_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		stored_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
		stored_waste_quantity = forms.FloatField()
	except:
		pass

	def __init__(self, *args, **kwargs):
		super(WasteStoredForm, self).__init__(*args, **kwargs)
		self.fields['stored_waste_category'].widget.attrs={'id': 'store_category','class':'btn btn-default dropdown-toggle'}
		self.fields['stored_waste_description'].widget.attrs={'id':'store_description','class':'btn btn-default dropdown-toggle'}
		self.fields['stored_waste_quantity'].widget.attrs={'id':'store_quantity','placeholder':'Kilogram'}

class WasteSentToRecyclerForm(forms.Form):
	try:
		sent_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		sent_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
		sent_waste_quantity = forms.FloatField()
	except:
		pass

	def __init__(self, *args, **kwargs):
		super(WasteSentToRecyclerForm, self).__init__(*args, **kwargs)
		self.fields['sent_waste_category'].widget.attrs={'id': 'sent_category','class':'btn btn-default dropdown-toggle'}
		self.fields['sent_waste_description'].widget.attrs={'id':'sent_description','class':'btn btn-default dropdown-toggle'}
		self.fields['sent_waste_quantity'].widget.attrs={'id':'sent_quantity','placeholder':'Kilogram'}

class UserSelectionForm(forms.Form):
	information_technology_and_telecommunication_equipment = forms.\
		ModelMultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple,queryset = None)

	consumer_electrical_and_electronics = forms.ModelMultipleChoiceField(required = \
			True, widget = forms.CheckboxSelectMultiple,queryset = None)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		user = self.request.user
		desc_id = UserSelections.objects.values_list('description', flat=True).filter(user=user)
		super(UserSelectionForm, self).__init__(*args, **kwargs)
		self.fields['information_technology_and_telecommunication_equipment'].\
			queryset= Description.objects.filter(category = 1).filter(~Q(id__in=desc_id))
		self.fields['consumer_electrical_and_electronics'].\
			queryset= Description.objects.filter(category = 2).filter(~Q(id__in=desc_id))

class DepartmentProfileForm(forms.ModelForm):
	class Meta:
		model = Department
		exclude = ['user']
