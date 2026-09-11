from django.http import JsonResponse


# Custom error handlers for 404 and 500 errors
def custom_404(request, exception):
    return JsonResponse({'error 404': 'Page not found. This is because the page does not exist or you have mistyped the url, please try again.'}, status=404)

def custom_500(request):
    return JsonResponse({'error 500': 'Server error, something went wrong, please allow us time to fix it!'}, status=500)