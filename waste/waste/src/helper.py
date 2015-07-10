from waste.src.models import *
from django.db.models import Sum

def calculate_generated(request):
	user = request.user
	newdate = ''
	date = request.POST['date'].split("/")
	newdate = date[2] + "-" + date[0] + "-" + date[1]
	datetwo = request.POST['datetwo'].split("/")
	newdatetwo = datetwo[2] + "-" + datetwo[0] + "-" + datetwo[1]

	if user.is_superuser:
  		categories = WasteGenerated.objects.values_list('category_id',flat=True).\
			filter(date=unicode(newdate)).distinct()
		# categories = WasteGenerated.objects.values_list('category_id',flat=True).\
		# 	filter(field__range=(newdate, newdatetwo))
	else:
 		dept = Department.objects.get(user=user.id)
		categories = WasteGenerated.objects.filter(department=dept.id,date=newdate).values_list('category_id',flat=True).\
			distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteGenerated.objects.values_list('description__description',flat=True).\
			filter(category = val,date=newdate).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteGenerated.objects.filter(department=dept.id,date=newdate).filter(category=val,date=newdate).aggregate(Sum('quantity'))
		except:
			total = WasteGenerated.objects.filter(category=val,date=newdate).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		temp['date'] = newdate
		generated.append(temp)
	return generated

def calculate_stored(super_user,request):
	newdate = ''
	date = request.POST['date'].split("/")
	newdate = date[2] + "-" + date[0] + "-" + date[1]
	print date[2]
	print date[1]
	print date[0]
	if super_user == True:
		categories = WasteStored.objects.values_list('category_id',flat=True).filter(date=newdate).\
		distinct()
	else:
		user = request.user
		dept = Department.objects.get(user=user.id)
		categories = WasteStored.objects.filter(department=dept.id,date=newdate).values_list('category_id',flat=True).\
			distinct()

	generated = []
	for val in categories:
		temp = {}
		desc = WasteStored.objects.values_list('description__description',flat=True).\
			filter(category = val, date=newdate).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteStored.objects.filter(department=dept.id, date=newdate).filter(category=val,date=newdate).aggregate(Sum('quantity'))
		except:
			total = WasteStored.objects.filter(category=val, date=newdate).aggregate(Sum('quantity'))

		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated

def calculate_sent(request):
	user = request.user
	newdate = ''
	date = request.POST['date'].split("/")
	newdate = date[2] + "-" + date[0] + "-" + date[1]
	if user.is_superuser:
		categories = WasteSentToRecycler.objects.values_list('category_id',flat=True).filter(date=newdate).\
		distinct()
	else:
		dept = Department.objects.get(user=user.id)
		categories = WasteSentToRecycler.objects.filter(department=dept.id,date=newdate).\
		values_list('category_id',flat=True).distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteSentToRecycler.objects.values_list('description__description',flat=True).\
			filter(category = val, date=newdate).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteSentToRecycler.objects.filter(department=dept.id, date=newdate).filter(category=val).aggregate(Sum('quantity'))
		except:
			total = WasteSentToRecycler.objects.filter(category=val, date=newdate).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated