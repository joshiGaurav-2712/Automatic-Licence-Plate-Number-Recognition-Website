import os
from django.shortcuts import render
from LP_Recognition import settings
from .forms import ImageForm
from .models import StoreImage, DriverInfo
from LPR import recognizer

# Create your views here.

def home(request):
    return render(request, 'home_page.html')

def processed_image(request):

    if request.method == 'POST':

        form=ImageForm(request.POST, request.FILES)
        if form.is_valid():
            
            images_dir = os.path.join((settings.MEDIA_ROOT), 'images')
            
            for filename in os.listdir(images_dir):
                file_path = os.path.join(images_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(e)
        
            StoreImage.objects.all().delete()

            modelInstance=form.save()

            for filename in os.listdir(images_dir):
                file_path = os.path.join(images_dir, filename)

            licenseText=recognizer.get_lic(file_path)
            driverQuerySet=DriverInfo.objects.filter(licenseNo__contains=licenseText)

            if driverQuerySet.exists():
                driverInfoInstance=driverQuerySet[0]
                context={ 'modelInstance' : modelInstance, 'driverInfoInstance' : driverInfoInstance}
            else:
                context={ 'modelInstance' : modelInstance}

            return render(request, 'processed_image.html', context)
        
        else:
            return render(request, 'processed_image.html', {'form': form}) 