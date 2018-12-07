from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Reviews.models import Review
from django.core import serializers


# Create your views here.


def addReviewPage(request):
    context = {}
    return render(request, 'Reviews/addReview.html', context)

def displayReviews(request):
    context = {}
    return render(request, 'Reviews/getReview.html', context)

def getReviews(request, l):
    if request.is_ajax():
        results = Review.objects.filter(location=l).order_by('-upvotes','-datePosted')
        data = serializers.serialize("json", results)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

<<<<<<< HEAD
@csrf_exempt
def incrementUpvote(request):
=======
def incrementUpvotes(request):
>>>>>>> bcfcd21b2c713dc10f710e0a2932d4318f6bb834
    if request.is_ajax() and request.method == 'POST':
        r = Review.objects.get(pk=request.POST['id'])
        r.upvotes = r.upvotes+1
        r.save()
        return HttpResponse("hello")

@csrf_exempt
def submitReview(request):
    print("Hello")
    if request.is_ajax() and request.method == 'POST':
        r = Review(author=request.POST['author'],location=request.POST['location'],reviewText=request.POST['review'])#,datePosted=datetime.date.today())
        r.save()
        return HttpResponse("Hello")
    else:
        raise Http404
