from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import Registration, Log_in, Change_pass, UserForm
from django import forms
from .models import User, Topic, Category, Response

# Creating our index page
def index(request):
    # Access to all users and pass it to the page
    users = User.objects.exclude(id=request.user.id).order_by('date_joined').reverse()
    
    # Return just the index page or the main page
    return render(request, 'mismatch/index.html', {
        'users': users, 
    })


# Creating registration page
def register(request):
    if request.method == 'POST':
        # Call the class Registration to access the form data
        form = Registration(request.POST)

        # Check if the form submition is valid
        if form.is_valid():
            # Access to all filled forms
            username = form.cleaned_data['username']
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['confirmation']

            # Email existance checking
            if User.objects.filter(email=email):
                form = Registration()
                # Creating error message
                messages.error(request, "User with this email already existed")
                return render(request, 'mismatch/sign_in.html', {
                    'form': form
                })

            # Password validation checking by django build in validations
            try: 
                validate_password(password)
            except forms.ValidationError as error:
                form = Registration()
                # Joining the error list to one string error
                errors = ' '.join(error)
                # Creating error message to the user
                messages.error(request, errors)
                return render(request, 'mismatch/sign_in.html', {
                    'form': form
                })
            
            # Check password configuration
            if password != confirmation:
                form = Registration()
                messages.error(request, "Passwords must match.")
                return render(request, 'mismatch/sign_in.html', {
                    'form': form
                })

            # Saving the signed in user into the database
            try:
                user = User.objects.create_user(username, email, password)
                user.save
            except IntegrityError: # Checking about user existance
                form = Registration()
                messages.error(request, "Username already exists.")
                return render(request, 'mismatch/sign_in.html', {
                    'form': form
                })

            # Logging in the user; after signing in
            login(request, user)

            # Rendering to the index page with a success message
            messages.success(request, "You are signed in successfully.")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = Registration()
        return render(request, 'mismatch/sign_in.html', {
            "form": form
        })


# Creating for log in page
def log_in(request):
    if request.method == "POST":
        # Accessing to the created form
        form = Log_in(request.POST)

        # Checking form validation
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None: # Authentication success; loggin in
                login(request, user)
                messages.success(request, "You are logged in successfully.")
                return HttpResponseRedirect(reverse("index"))
            else:
                form = Log_in()
                messages.error(request, "Invalid username and/ or password")
                return render(request, 'mismatch/log_in.html', {
                    'form': form
                })
    else:
        form = Log_in()
        return render(request, 'mismatch/log_in.html', {
            'form': form
        })

@login_required
def log_out(request):
    # Logging out the user
    logout(request)
    messages.success(request, "You are logged out successfully.")
    return HttpResponseRedirect(reverse("index"))


@login_required()
def edit_profile(request):
    # Access to the current user data object
    usr = User.objects.get(id=request.user.id)

    # Define some initial data for the form with current user details
    initial_data = {
        'first_name': usr.first_name,
        'last_name': usr.last_name,
        'gender': usr.gender,
        'birthdate': usr.birthdate,
        'city': usr.city,
        'state': usr.state,
        'phone': usr.phone
    }

    # Check if the user is submitting the form
    if request.method == 'POST':
        # Access to the submitted form
        form = UserForm(request.POST, request.FILES)

        # Check if the submitted form is valid
        if form.is_valid():
            # Accessing all form data and storing to the database
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            gnr = form.cleaned_data['gender']
            bthd = form.cleaned_data['birthdate']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pic = form.cleaned_data['picture']
            phone = form.cleaned_data['phone']

            # Check if the user edited his/her profile
            if (usr.first_name == fname and usr.last_name == lname and usr.gender == gnr 
                and usr.birthdate == bthd and usr.city == city and usr.state == state and
                usr.phone == phone and not pic):

                # No changes are detected
                messages.warning(request, "No changes detected.")
                return HttpResponseRedirect(reverse("index"))

            # Storing all submitted data to the database
            usr.first_name = fname
            usr.last_name = lname
            usr.gender = gnr
            usr.birthdate = bthd
            usr.city = city
            usr.state = state

            # Check if the user has already a profile pic
            if not usr.picture:
                usr.picture = pic
            else:
                if pic:
                    # Delete the old image and save the new one
                    usr.picture.delete()
                    usr.picture = pic

            usr.phone = phone
            usr.save()

            # Passing the user to the main page with a success message
            messages.success(request, "Your profile edited successfully.")
            return HttpResponseRedirect(reverse("index"))
        else:
            # Create an error message and inform the user
            messages.error(request, form.errors.as_text())
        
            # Make instance of the form with initial data; or we can say create the form
            form = UserForm(initial=initial_data)

            # Render the form page
            return render(request, 'mismatch/edit_profile.html', {
                'form': form, 'usr_obj': usr
            })

    else:
        # Make instance of the form with initial data; or we can say create the form
        form = UserForm(initial=initial_data)

        # Render the form page
        return render(request, 'mismatch/edit_profile.html', {
            'form': form, 'usr_obj': usr
        })


@login_required
def view_profile(request):
    # Access to profile details of the user
    usr = User.objects.get(id=request.user.id)
    
    # Return it to the view page
    return render(request, 'mismatch/view_profile.html', {
        'usr': usr, 'usr_obj': usr
    })


def message(request): 
    # This rout is for log in url
    messages.error(request, "You have to log/ sign in first.")
    return HttpResponseRedirect(reverse("register"))


@login_required
def change_password(request):
    if request.method == "POST":
        # Accessing to the form
        form = Change_pass(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            new_password_conf = form.cleaned_data['new_pass_conf']

            # User password authentication
            username = request.user.username
            user = authenticate(request, username=username, password=current_password)
            if user is None:
                form = Change_pass()
                messages.error(request, "Invalid Password.")
                return render(request, 'mismatch/change_pass.html', {
                    'form': form
                })

            # New password validation by django build in password validation
            try:
                validate_password(new_password)
            except forms.ValidationError as error:
                form = Change_pass()
                # Joining the error list to one string error
                errors = ' '.join(error)
                # Creating error message to the user
                messages.error(request, errors)
                return render(request, 'mismatch/change_pass.html', {
                    'form': form
                })

            # New password confirmation
            if new_password != new_password_conf:
                form = Change_pass()
                messages.error(request, "New password must match.")
                return render(request, 'mismatch/change_pass.html', {
                    'form': form
                })

            # Password update
            usr = User.objects.get(username=username)
            usr.set_password(new_password)
            usr.save()

            # Logging in user with new password
            login(request, usr)
            messages.success(request, "Your password has changed successfully.")
            return HttpResponseRedirect(reverse("index"))

    else:
        form = Change_pass()
        return render(request, "mismatch/change_pass.html", {
            'form': form
        })


@login_required
def questionnaire(request):
    '''
    We have a reponse table that stores all responses with topic, id and category for users.
    Every time a user wants mismatch questionnaire form, we create the form from response table.
    '''
    # For creating a mismatch questionnaire form, we need to know whether the user has any responses or not
    rsp = Response.objects.filter(user=request.user)

    if not rsp:
        # The user has not any responses yet. So we insert to response table without any respons; just the user and topics
        topics = Topic.objects.all()
        # Looping for every topic and inserting it to the response table
        for tpc in topics:
            Response.objects.create(user=request.user, topic=tpc)

    # Now we create our questionnaire form from datas stored in response table
    response = Response.objects.filter(user=request.user)
    categories = Category.objects.all()
    if request.method == "POST":
        # Since the user submitted the form, here should be updated the reponse table
        for rsp_id in request.POST:
            if rsp_id.isdigit(): # It should be id; since inputs' names are responses id. If in request.POST object something exists apart from integer, ignore it
                # Updating the submitted data respectly
                rsp = Response.objects.get(id=int(rsp_id))
                # Updating                      
                rsp.response = int(request.POST[rsp_id])
                rsp.save()

        messages.success(request, "Your responses have successfully saved.")
        return HttpResponseRedirect(reverse('index'))
    else:
        # Render the user to the form page
        return render(request, 'mismatch/questionnaire.html', { 
            'responses': response, 'categories': categories
        })


@login_required
def my_mismatch(request):
    ''' This function is going to find the mismtach between
        tht logged in user and other users.
    '''
    # Defining a set for keeping track of mismatched topics
    msm_tps = set()

    # Defining mismatched number
    msm_num = 0

    # Defining an id for mismatch person; in the begining no mismatch so we set it to None
    msm_usr_id = None

    # Accessing to the current logged in user
    logged_user = request.user

    # Accessing to all other users except the current logged in user
    users = User.objects.exclude(id=request.user.id)

    # Looping for every other user and computing the mismatch
    for usr in users:
        # Now access to all responses of the looped user
        rpses = Response.objects.filter(user=usr)

        # Mismatch count
        i = 0

        # Mismatch topics
        mached_topics = set()

        # Now loop for every response of looped user and check for a mismatch
        for rsp in rpses:
           # Topic for mismatch
            tpc = rsp.topic

            # Accessing to logged in user response of the same topic
            lg_usr_rsp = Response.objects.filter(user=logged_user, topic=tpc)

            if lg_usr_rsp:
                # Check if responses are not empty
                if (rsp.response and lg_usr_rsp[0].response):
                    # Looking for mismatch
                    if (rsp.response + lg_usr_rsp[0].response) == 0:
                        # Now we have a mismatch
                        i += 1
                        mached_topics.add(tpc.name)

        # Check if we have foundd a better mismatch
        if i > msm_num:
            msm_num = i
            msm_tps = mached_topics
            msm_usr_id = usr.id

    if msm_usr_id:
        best_mismatched_user = User.objects.get(id=msm_usr_id)
        return render(request, 'mismatch/my_mismatch.html', {
            'best_mismatch': best_mismatched_user, 'topics': msm_tps, 'num_tps': len(msm_tps)
        })
    else:
        messages.error(request, "Sorry you don't have any mismatch yet. Please be sure to answer the questionnaire form")
        return render(request, 'mismatch/my_mismatch.html')


@login_required
def mismatch_prof(request, user_id):
    mismatch = User.objects.get(id=user_id)
    return render(request, 'mismatch/mismatch_prof.html', {
        'mismatch': mismatch
    })