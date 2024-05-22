from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Book
from django.http import HttpResponseNotFound
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
import requests
import base64
import json




def homeView(request):
    books=Book.objects.all()
    search_query = request.GET.get('q')

    if search_query:
        books = Book.objects.filter(title__icontains=search_query)
    else:
        books = Book.objects.all()

    return render(request, "viewbook.html", {"books": books})   

def addBookView(request):
    return render(request,"addbook.html")

def addBook(request):
     if request.method=="POST":
        nam=request.POST["title"]
        pri=request.POST["price"]
        
        book=Book()
        book.title=nam
        book.price=pri
        book.save()
        return HttpResponseRedirect('/')
    
def borrow_view(request):
    available_books = Book.objects.filter(is_available=True)
    
    context = {'available_books': available_books}
    return render(request, 'borrow.html', context)

def process_borrow(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        payment_amount = int(request.POST.get('payment'))

        # Retrieve book details and calculate total price (e.g., from your database)
        book = Book.objects.get(pk=book_id)
        total_price = book.price * payment_amount

        # Create a Stripe PaymentIntent
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total_price * 100,  # Amount in cents
            currency='usd',  # Currency code
        )
        
        selected_payment_method = request.POST.get('payment_method')

        if selected_payment_method == 'mpesa':
            # Construct the M-Pesa request body
            mpesa_request_body = {
                "BusinessShortCode": "174379",
                "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
                "Timestamp": "20160216165627",
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1",
                "PartyA": "254708374149",
                "PartyB": "174379",
                "PhoneNumber": "254708374149",
                "CallBackURL": "https://mydomain.com/pat",
                "AccountReference": "Test",
                "TransactionDesc": "Test"
            }

            # Convert the request body to a JSON string
            mpesa_request_json = json.dumps(mpesa_request_body)

            # Encode the JSON string to base64
            mpesa_request_base64 = base64.b64encode(mpesa_request_json.encode()).decode()

            # Make a POST request to the M-Pesa API
            mpesa_api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'  # Replace with the actual M-Pesa API URL
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'nL9TFUKOs3KdNKFoI4v4DHZjOtdMNYuy'  # Replace with your M-Pesa API key
            }

            response = requests.post(mpesa_api_url, data=mpesa_request_base64, headers=headers)

            # Handle the API response
            mpesa_response = response.json()
            
            if not book.is_borrowed:
                book.is_borrowed = True
                book.save()
                
                return redirect('process_borrow')

            # Check if the payment was successful
            if mpesa_response.get('ResponseCode') == '0':
                # Payment was successful, handle accordingly
                # You can redirect or display a success message here
                return render(request, 'payment.html', {'client_secret': intent.client_secret})
            else:
                # Payment failed, handle accordingly
                # Display an error message to the user
    # ... (the rest of your view code)
                return render(request, 'payment.html')
        
    else:
       return redirect('/borrow/') 
   
def available_books(request):
    books = Book.objects.filter(is_borrowed=False)
    return render(request, 'available_books.html', {'books': books})

def borrowed_books(request):
    books = Book.objects.filter(is_borrowed=True)
    return render(request, 'borrowed_books.html', {'books': books})

def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if not book.is_borrowed:
        book.is_borrowed = True
        book.save()
    return redirect('available_books')

def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.is_borrowed:
        book.is_borrowed = False
        book.save()
    return redirect('borrowed_books')

def return_books_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_to_return')
        
        try:
            book = Book.objects.get(pk=book_id)
            if book.is_borrowed:
                # Mark the book as returned (update your model field accordingly)
                book.is_borrowed = False
                book.save()
                return render(request, 'return_success.html')  # Display a success message
            else:
                # Handle the case where the book is not marked as borrowed
                return render(request, 'return_failure.html')  # Display an error message
        except Book.DoesNotExist:
            # Handle the case where the book does not exist
            return render(request, 'return_failure.html')  # Display an error message
    else:
        # Display the list of borrowed books for selection
        borrowed_books = Book.objects.filter(is_borrowed=True)
        return render(request, 'returnbook.html', {'borrowed_books': borrowed_books})
           

        

        
    
