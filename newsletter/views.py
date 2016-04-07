from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm, SignUpForm


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


    return  render(request,"example_fluid.html", context)


def contact(request):
    form =  ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        #     # print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name") 
        # print email, message, full_name

        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@gmail.com']
        contact_message = "%s: %s via %s" % (
                form_full_name, 
                form_message, 
                form_email)
        some_html_message = """
        <h1>hello</h1>
        """

        send_mail(subject
                ,contact_message
                ,from_email
                ,to_email
                ,html_message = some_html_message
                ,fail_silently=False
        )

    context = {
            "form": form,
    }
    return render(request, "forms.html", context)







