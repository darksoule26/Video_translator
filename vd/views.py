from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
def home(request):
    return render(request, 'vd/home.html')



# vd/views.py

from .forms import VideoUploadForm
import os
import subprocess


# vd/views.py




def dub(request):
    dubbed_video_path = None

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the selected target language from the form
            target_language = request.POST.get('target_language')

            # Get the uploaded video file
            video_file = form.cleaned_data['video_file']

            # Save the uploaded video as "input.mp4" in the 'media' directory
            input_file_path = os.path.join('media', 'input.mp4')
            with open(input_file_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Call your dubbing script to generate the dubbed video
            dub_video_script = 'dub_script/dub_video.py'  # Modify the path to your dubbing script

            # Execute your dubbing script with the input file path and target language
            subprocess.run(['python', dub_video_script, input_file_path, target_language])

            # Set the path for the dubbed video to be displayed
            dubbed_video_path = 'media/dubbed_video.mp4'  # Modify this to the correct path

    else:
        form = VideoUploadForm()

    return render(request, 'vd/dub.html', {'form': form, 'dubbed_video_path': dubbed_video_path})


def play_dubbed_video(request):
    # Redirect to the URL of the dubbed video
    return redirect('http://localhost:8000/media/dubbed_video.mp4')