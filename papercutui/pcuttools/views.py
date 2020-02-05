from django.shortcuts import render
from django.http import HttpResponse


import os, sys, stat
import subprocess
import re

from pathlib import Path
from .forms import UploadFileForm

homeDir = str(Path.home())
idImportpath = os.path.join(homeDir, 'server', 'bin', 'linux-x64', 'paperImport')
serverCommandPath = os.path.join(homeDir, 'server', 'bin', 'linux-x64')

# Create your views here.
def home(request):
    
    
    # print(os.path.join(idImportpath, 'testfile.txt'))
    # print(os.path.exists(os.path.join(idImportpath, 'testfile.txt')))
    return render(request, 'home.html')

def idimport(request):
    message = ""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_File = request.Files('importfile')
            if import_file_valid(input_File):
                handle_uploaded_file(request.FILES['importfile'])
                run_id_import()
            return HttpResponse("Successful")
    else:

        form = UploadFileForm()

    return render(request, 'idimport.html', {'form':form, 'message':message})
        

def handle_uploaded_file(f):
    with open(os.path.join(idImportpath, 'import.txt'), 'wb+') as destination:
        print("writing file")
        for chunk in f.chunks():
            destination.write(chunk)
    f.close()
    

def import_file_valid(import_file):
    regex = re.compile("\w+\.\w+\t\d+")
    with open(import_file, 'r') as f:
        for line in f:
            result = regex.search(line)
            if not result:
                print("Error:\n" + result + "\n" + line)
                return False
            else:
                return True
    return False
    

def run_id_import():
    subprocess.run(["server-command", "batch-import-user-card-id-numbers", idImportpath+"/import.txt"])
   
