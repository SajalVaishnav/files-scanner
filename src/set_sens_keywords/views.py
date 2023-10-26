from django.shortcuts import render
from django.views import View
from pymongo import MongoClient
from .forms import KeyWordsForm
from django.conf import settings 
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

class SetSensKeywords(View):

    def post(self, request):
        form = KeyWordsForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            settings.SENS_KEYWORDS_COLLECTION.insert_document(keywords)
            return HttpResponseRedirect('success')
        return render(request, 'set_sens_keywords/keywords.html', {'form': form})
                
    def get(self, request):
        form = KeyWordsForm()
        return render(request, 'set_sens_keywords/keywords.html', {'form': form})

class KwSetSuccessfully(View):
    
    def get(self, request):
        return HttpResponse("Keywords set successfully!", content_type="text/plain")

class GetSensKeywords(View):

    def get(self, request):
        sens_words_values = SENS_KEYWORDS_COLLECTION.get_kws_dict()
        return JsonResponse(sens_words_values)
