from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Address, UserProfile, Wishlist, WishlistItem


# Helper functions for session-based cart
def get_session_cart(request):
    """Get cart dictionary from session, create if doesn't exist"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def add_to_session_cart(request, product_id, quantity=1):
    """Add product to session cart"""
    cart = get_session_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    request.session.modified = True


def remove_from_session_cart(request, product_id):
    """Remove product from session cart"""
    cart = get_session_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session.modified = True


def update_session_cart_item(request, product_id, quantity):
    """Update product quantity in session cart"""
    cart = get_session_cart(request)
    product_id_str = str(product_id)
    
    if quantity > 0:
        cart[product_id_str] = quantity
    elif product_id_str in cart:
        del cart[product_id_str]
    
    request.session.modified = True


def clear_session_cart(request):
    """Clear all items from session cart"""
    request.session['cart'] = {}
    request.session.modified = True


def get_session_cart_items(request):
    """Get list of cart items from session"""
    cart = get_session_cart(request)
    items = []
    
    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id_str))
            items.append({
                'product': product,
                'quantity': quantity,
                'product_id': int(product_id_str)
            })
        except Product.DoesNotExist:
            pass
    
    return items


def get_session_cart_total_price(request):
    """Get total price of session cart"""
    items = get_session_cart_items(request)
    return sum(item['product'].price * item['quantity'] for item in items)


def get_session_cart_total_items(request):
    """Get total number of items in session cart"""
    cart = get_session_cart(request)
    return sum(cart.values())


def merge_session_cart_to_user(request, user):
    """
    Merge anonymous user's session cart with their authenticated cart
    Called after successful login
    """
    session_items = get_session_cart_items(request)
    
    if session_items:
        # Get or create user's cart
        user_cart, created = Cart.objects.get_or_create(user=user)
        
        # Add each session item to user's cart
        for item in session_items:
            product = item['product']
            quantity = item['quantity']
            
            # Get or create cart item
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # If item already exists, add to quantity
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
        
        # Clear session cart
        clear_session_cart(request)



def home(request):
    """
    Home page view - displays featured products and categories
    """
    products = Product.objects.all()[:12]
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'shop/index.html', context)


def products_list(request):
    """
    Products listing view - displays all products with filtering and pagination
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Sort by price if provided
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
        products = products.order_by(sort_by)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            name__icontains=search_query
        ) | products.filter(
            description__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'shop/products_list.html', context)


def product_detail(request, pk):
    """
    Product detail view - displays a single product's information
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:3]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'shop/product_detail.html', context)


def cart_view(request):
    """
    View to display the shopping cart - supports both authenticated and anonymous users
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = None
        
        context = {
            'cart': cart,
            'session_items': None,
            'is_authenticated': True,
        }
    else:
        # For anonymous users, show session cart
        session_items = get_session_cart_items(request)
        total_price = get_session_cart_total_price(request)
        
        context = {
            'cart': None,
            'session_items': session_items,
            'session_total_price': total_price,
            'is_authenticated': False,
        }
    
    return render(request, 'shop/cart.html', context)



def add_to_cart(request, product_id):
    """
    Add a product to the cart or update quantity
    Supports both authenticated users and anonymous users (via session)
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    
    if request.user.is_authenticated:
        # Get or create cart for the authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        # Update quantity if item already exists
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        total_items = cart.get_total_items()
        total_price = str(cart.get_total_price())
    else:
        # Handle anonymous user - store in session
        add_to_session_cart(request, product_id, quantity)
        total_items = get_session_cart_total_items(request)
        total_price = str(get_session_cart_total_price(request))
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'product_id': product_id,
            'quantity': quantity,
            'cart_total_items': total_items,
            'cart_total_price': total_price
        })
    
    return redirect('cart')



def remove_from_cart(request, item_id):
    """
    Remove an item from the cart - supports both authenticated and anonymous users
    For authenticated users: uses cart item ID
    For anonymous users: uses product ID (passed as item_id)
    """
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        cart_item.delete()
    else:
        # For anonymous users, item_id is the product_id
        remove_from_session_cart(request, item_id)
    
    return redirect('cart')


def update_cart_item(request, item_id):
    """
    Update the quantity of a cart item - supports both authenticated and anonymous users
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Quantity updated',
                    'item_id': item_id,
                    'quantity': quantity,
                    'total_price': str(cart_item.get_total_price()) if quantity > 0 else '0'
                })
        else:
            # For anonymous users, item_id is the product_id
            update_session_cart_item(request, item_id, quantity)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if quantity > 0:
                    product = Product.objects.get(pk=item_id)
                    total_price = product.price * quantity
                else:
                    total_price = 0
                
                return JsonResponse({
                    'success': True,
                    'message': 'Quantity updated',
                    'item_id': item_id,
                    'quantity': quantity,
                    'total_price': str(total_price)
                })
    
    return redirect('cart')


def clear_cart(request):
    """
    Clear all items from the cart - supports both authenticated and anonymous users
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
    else:
        # For anonymous users, clear session cart
        clear_session_cart(request)
    
    return redirect('cart')


@login_required(login_url='login')
def address(request):
    """
    Address form view - collect delivery address before payment
    """
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')
    
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        
        # Check if user selected an existing address
        if selected_address_id:
            try:
                address_obj = Address.objects.get(id=selected_address_id, user=request.user)
                address_data = {
                    'first_name': address_obj.first_name,
                    'last_name': address_obj.last_name,
                    'email': address_obj.email,
                    'address': address_obj.address,
                    'address2': address_obj.address2,
                    'city': address_obj.city,
                    'postal_code': address_obj.postal_code,
                    'state': address_obj.state,
                    'country': address_obj.country,
                    'phone': address_obj.phone,
                }
                
                # Check if this is an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    request.session['delivery_address'] = address_data
                    return JsonResponse({
                        'success': True,
                        'message': 'Address selected successfully',
                        'redirect_url': '/cart/payment/'
                    })
                else:
                    request.session['delivery_address'] = address_data
                    return redirect('payment')
            except Address.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Address not found'
                    })
                return redirect('address')
        else:
            # Add new address
            address_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'address': request.POST.get('address'),
                'address2': request.POST.get('address2'),
                'city': request.POST.get('city'),
                'postal_code': request.POST.get('postal_code'),
                'state': request.POST.get('state'),
                'country': request.POST.get('country'),
                'phone': request.POST.get('phone'),
            }
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Validate required fields
                required_fields = ['first_name', 'last_name', 'email', 'address', 'city', 'postal_code', 'state', 'country', 'phone']
                if not all(address_data.get(field) for field in required_fields):
                    return JsonResponse({
                        'success': False,
                        'message': 'Please fill all required fields'
                    })
                
                # Check if identical address already exists for this user
                existing_address = Address.objects.filter(
                    user=request.user,
                    first_name=address_data['first_name'],
                    last_name=address_data['last_name'],
                    address=address_data['address'],
                    address2=address_data['address2'],
                    city=address_data['city'],
                    postal_code=address_data['postal_code'],
                    state=address_data['state'],
                    country=address_data['country'],
                    phone=address_data['phone'],
                ).first()
                
                if existing_address:
                    # Use existing address instead of creating duplicate
                    address_id = existing_address.id
                    message = 'Using existing address'
                    is_new = False
                else:
                    # Save new address to database
                    new_address = Address.objects.create(user=request.user, **address_data)
                    address_id = new_address.id
                    message = 'Address saved successfully'
                    is_new = True
                
                # Store address in session
                request.session['delivery_address'] = address_data
                
                return JsonResponse({
                    'success': True,
                    'message': message,
                    'address_id': address_id,
                    'is_new': is_new,
                    'redirect_url': '/cart/payment/'
                })
            else:
                # Store address in session and redirect
                request.session['delivery_address'] = address_data
                return redirect('payment')
    
    context = {
        'cart': cart,
        'cart_total': cart.get_total_price() if cart else 0,
        'existing_addresses': Address.objects.filter(user=request.user),
    }
    
    return render(request, 'shop/address.html', context)


def delete_address(request, address_id):
    """
    Delete address view - remove address from database
    """
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        address.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Address deleted successfully'
            })
        else:
            return redirect('address')
    except Address.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Address not found'
            })
        return redirect('address')


@login_required(login_url='login')
def get_address_data(request, address_id):
    """
    Get address data as JSON for editing
    """
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        return JsonResponse({
            'success': True,
            'data': {
                'id': address.id,
                'first_name': address.first_name,
                'last_name': address.last_name,
                'email': address.email,
                'address': address.address,
                'address2': address.address2 or '',
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country,
                'phone': address.phone,
            }
        })
    except Address.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Address not found'
        })


@login_required(login_url='login')
def update_address(request, address_id):
    """
    Update address view - modify existing address
    """
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Address not found'
        })
    
    if request.method == 'POST':
        # Update address fields
        address.first_name = request.POST.get('first_name', address.first_name)
        address.last_name = request.POST.get('last_name', address.last_name)
        address.email = request.POST.get('email', address.email)
        address.address = request.POST.get('address', address.address)
        address.address2 = request.POST.get('address2', '')
        address.city = request.POST.get('city', address.city)
        address.state = request.POST.get('state', address.state)
        address.postal_code = request.POST.get('postal_code', address.postal_code)
        address.country = request.POST.get('country', address.country)
        address.phone = request.POST.get('phone', address.phone)
        
        address.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Address updated successfully',
                'address_id': address.id
            })
        else:
            return redirect('profile')
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


@login_required(login_url='login')
def payment(request):
    """
    Payment view - collect payment method and process payment
    """
    # Check if address was provided
    if 'delivery_address' not in request.session:
        return redirect('address')
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')
    
    if request.method == 'POST':
        # Collect payment data
        payment_method = request.POST.get('payment_method')
        payment_data = {
            'method': payment_method,
            'cardholder': request.POST.get('cardholder', ''),
            'cardnumber': request.POST.get('cardnumber', ''),
            'expiry': request.POST.get('expiry', ''),
            'cvv': request.POST.get('cvv', ''),
        }
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Validate payment method
            if not payment_method:
                return JsonResponse({
                    'success': False,
                    'message': 'Please select a payment method'
                })
            
            # Validate card details if card/debit is selected
            if payment_method in ['card', 'debit']:
                required_fields = ['cardholder', 'cardnumber', 'expiry', 'cvv']
                if not all(payment_data.get(field) for field in required_fields):
                    return JsonResponse({
                        'success': False,
                        'message': 'Please fill all card details'
                    })
            
            # Store payment in session
            request.session['payment_data'] = payment_data
            
            return JsonResponse({
                'success': True,
                'message': 'Payment processed successfully',
                'order_id': f'#ORD{int(request.user.id)}{int(__import__("time").time())}'
            })
    
    context = {
        'cart': cart,
        'cart_total': cart.get_total_price() if cart else 0,
        'address': request.session.get('delivery_address', {}),
    }
    
    return render(request, 'shop/payment.html', context)


@login_required(login_url='home')
def profile(request):
    """
    User profile view - display and manage user profile information
    """
    # Get or create user profile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            date_of_birth = request.POST.get('date_of_birth', '')
            gender = request.POST.get('gender', '')
            phone_number = request.POST.get('phone_number', '')
            country_code = request.POST.get('country_code', '+1')
            
            # Update user info
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            # Update profile info
            user_profile.date_of_birth = date_of_birth if date_of_birth else None
            user_profile.gender = gender if gender else None
            user_profile.phone_number = phone_number
            user_profile.country_code = country_code
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            
            user_profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully!'
            })
        else:
            # Regular form submission
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            date_of_birth = request.POST.get('date_of_birth', '')
            gender = request.POST.get('gender', '')
            phone_number = request.POST.get('phone_number', '')
            country_code = request.POST.get('country_code', '+1')
            
            # Update user info
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            # Update profile info
            user_profile.date_of_birth = date_of_birth if date_of_birth else None
            user_profile.gender = gender if gender else None
            user_profile.phone_number = phone_number
            user_profile.country_code = country_code
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            
            user_profile.save()
            
            return redirect('profile')
    
    # Get user's saved addresses
    user_addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    
    # Get user's wishlist
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.items.all()
    except Wishlist.DoesNotExist:
        wishlist = None
        wishlist_items = []
    
    context = {
        'user': request.user,
        'profile': user_profile,
        'addresses': user_addresses,
        'wishlist': wishlist,
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'shop/profile.html', context)


def user_login(request):
    """
    User login view - authenticate user and create session
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email_or_username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')
        
        if not email_or_username or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'shop/login.html')
        
        # Try to authenticate with email or username
        user = None
        
        # If input contains @, treat it as email
        if '@' in email_or_username:
            try:
                # Get the first user with matching email (in case of duplicates)
                user_obj = User.objects.filter(email=email_or_username).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
                else:
                    messages.error(request, 'Invalid email or password. Please try again.')
                    return render(request, 'shop/login.html')
            except Exception as e:
                messages.error(request, 'Invalid email or password. Please try again.')
                return render(request, 'shop/login.html')
        else:
            # Treat as username
            user = authenticate(request, username=email_or_username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Merge session cart with user cart
            merge_session_cart_to_user(request, user)
            
            # Handle remember me
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser session
            
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to next page or home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'shop/login.html')
    
    context = {}
    return render(request, 'shop/login.html', context)


def user_signup(request):
    """
    User signup view - create new user account
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')
        
        # Validate form
        if not all([first_name, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'shop/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'shop/signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'shop/signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login or use a different email.')
            return render(request, 'shop/signup.html')
        
        # Create user
        try:
            # Use email as username
            username = email.split('@')[0]
            
            # Make username unique if it already exists
            if User.objects.filter(username=username).exists():
                counter = 1
                while User.objects.filter(username=f'{username}{counter}').exists():
                    counter += 1
                username = f'{username}{counter}'
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Auto-login the new user
            login(request, user)
            
            # Merge session cart with user cart
            merge_session_cart_to_user(request, user)
            
            messages.success(request, f'Welcome, {first_name}! Your account has been created successfully.')
            return redirect('home')
        
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'shop/signup.html')
    
    context = {}
    return render(request, 'shop/signup.html', context)


def user_logout(request):
    """
    User logout view - destroy session
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """
    Add product to user's wishlist
    """
    try:
        product = Product.objects.get(id=product_id)
        
        # Get or create wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Check if product already in wishlist
        wishlist_item, is_new = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Product added to wishlist!',
                'is_new': is_new,
                'total_items': wishlist.items.count()
            })
        else:
            messages.success(request, 'Product added to wishlist!')
            return redirect('product_detail', pk=product_id)
    
    except Product.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            })
        messages.error(request, 'Product not found')
        return redirect('home')


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    """
    Remove product from user's wishlist
    """
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_item = WishlistItem.objects.get(wishlist=wishlist, product_id=product_id)
        wishlist_item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Product removed from wishlist!',
                'total_items': wishlist.items.count()
            })
        else:
            messages.success(request, 'Product removed from wishlist!')
            return redirect('wishlist')
    
    except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Item not found in wishlist'
            })
        messages.error(request, 'Item not found')
        return redirect('wishlist')


@login_required(login_url='login')
def wishlist_view(request):
    """
    View user's wishlist
    """
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.items.all()
    except Wishlist.DoesNotExist:
        wishlist = None
        wishlist_items = []
    
    context = {
        'wishlist': wishlist,
        'wishlist_items': wishlist_items,
        'total_items': len(wishlist_items) if wishlist else 0,
    }
    
    return render(request, 'shop/wishlist.html', context)


@login_required(login_url='login')
def is_in_wishlist(request, product_id):
    """
    Check if product is in user's wishlist (AJAX)
    """
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        in_wishlist = WishlistItem.objects.filter(
            wishlist=wishlist,
            product_id=product_id
        ).exists()
        
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'total_items': wishlist.items.count()
        })
    except Wishlist.DoesNotExist:
        return JsonResponse({
            'success': True,
            'in_wishlist': False,
            'total_items': 0
        })


