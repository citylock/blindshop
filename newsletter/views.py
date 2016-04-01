from django.shortcuts import render
from .forms import SignUpForm

# Create your views here.
def home(request):
    title = "Welcome" 
    form =  SignUpForm(request.POST or None)
    # if request.user.is_authenticated():
    #    title = "My Title %s" %(request.user)

    # add a form
    # print request
    #if request.method == "POST":
    #    print request.POST

    context = {
        "title": title,
        "form": form,
    }

    if form.is_valid():
        #form.save()
        print request.POST['email']    # not recommend because is not validated, it is raw data
        instance = form.save(commit=False)

        full_name = form.cleaned_data.get("full_name")
        if not full_name: 
            full_name = "New full_name"
        instance.full_name = full_name

        # if not instance.full_name: 
        #    instance.full_name = "Justin"
        instance.save()
        context = {
                "title": "Thank you", 
        }


    return  render(request,"home.html", context)

