from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
import random

from . import util

def mark_to_HTML(title):
    content = util.get_entry(title) 
    converter = Markdown()
    
    if content == None:
        return None
    else:
        return converter.convert(content)
    
        
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = mark_to_HTML(title)
    if content == None:
        return render(request,"encyclopedia/error.html", {
             "message": title + " not found",
                "title":title +" 404 Error",
                "error":"404"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":content
        })
    
    
def search(request):
    #TODO if the title is in list redirect to the entry of that title
    #TODO search resutl part of the word e.g ytho should list return a list with ytho like python with link
    entries = util.list_entries()
    entries = list((entry.lower() for entry in entries))
    
    if request.method == "POST":
        q = request.POST.get('q')
        if q.lower() in entries:
            return entry(request,q)
        
        # Create a list 
        n_list=[]
        for item in entries:
            if q in item:
                n_list.append(item.capitalize())
       
        if len(n_list) > 0:
           return render(request, "encyclopedia/search.html", {
               "n_list":n_list,
               "title":q
           })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": q + " not found",
                "title":"404 Error",
                "error":"404"
            })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        entries = util.list_entries()
        entries = list((entry.lower() for entry in entries))
        
        if title and content:
            if title.lower() not in entries:
                util.save_entry(title.capitalize(),content)
                return entry(request,title)
            else:
                return render(request,"encyclopedia/error.html", {
                    "message":"page already exists",
                    "title":"Error",
                    "error":title.capitalize()
                })
        else:
            return render(request,"encyclopedia/error.html", {
                "message":"Fields cannot be empty"
            })
    return render(request, "encyclopedia/new_page.html", {
        "title":"GET"
    })
            
            
def edit(request):
    
    if request.method =="POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        print("post ",title,content)
        util.save_entry(title,content)
        return entry(request,title)
    
    title = request.GET.get("title")
    print("get ",title)
    content = util.get_entry(title)
    return render(request,"encyclopedia/edit.html", {
        "title": title,
        "content":content
    })


def rand(request):
    content = util.list_entries()
    content = list(content)
    r_num = random.randint(0, (len(content) - 1))
    
    return entry(request,content[r_num])