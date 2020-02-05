from django.shortcuts import render, redirect
from django.http import HttpResponse


import os, sys, stat
import subprocess
import re

from pathlib import Path
from .forms import UploadFileForm

homeDir = str(Path.home())
idImportpath = os.path.join(homeDir, 'server', 'bin', 'linux-x64', 'paperImport')
importFile = os.path.join(idImportpath, 'import.txt')
serverCommandPath = os.path.join(homeDir, 'server', 'bin', 'linux-x64')

# Create your views here.
def home(request):
    
    
    # print(os.path.join(idImportpath, 'testfile.txt'))
    # print(os.path.exists(os.path.join(idImportpath, 'testfile.txt')))
    return render(request, 'home.html')

def idimport(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_File = request.FILES['importfile']
            handle_uploaded_file(input_File)
            valid,message = import_file_valid(importFile)
            if valid:
                run_id_import()
            
            return render(request, 'pcuttools/idimport.html', {'form':form, 'message':message})
            
    else:

        form = UploadFileForm()

    return render(request, 'pcuttools/idimport.html', {'form':form})
        

def handle_uploaded_file(f):
    with open(importFile, 'wb+') as destination:
        print("writing file")
        for chunk in f.chunks():
            destination.write(chunk)
    f.close()
    

def import_file_valid(import_file):
    message = "Success"
    with open(import_file, 'r') as f:
        for line in f:
            results = re.findall(r'\w+\.\w+\t\d+', line)
            print(results)
            if len(results) == 0:
                message = "Error with import file: " + line
                return False, message
    return True, message

def run_id_import():
    subprocess.run(["server-command", "batch-import-user-card-id-numbers", idImportpath+"/import.txt"])
   
