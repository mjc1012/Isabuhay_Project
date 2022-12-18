import docx2txt as d2t
from urllib.request import urlopen
from django.contrib.auth import logout
from django.contrib.auth import views as aviews
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import *
from isabuhaywebapp.models import *
from django.shortcuts import *
from .forms import *
from datetime import datetime
from django.utils import timezone
import pytz
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.mixins import LoginRequiredMixin
from IsabuhayWebsite import settings
from isabuhaywebapp.models import User
from django.contrib import messages
from datetime import date
from isabuhaywebapp.models import CBCTestResult
import os
import pandas as pd
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from pdfminer.high_level import extract_text
from google.cloud import vision
from smart_open import smart_open
from google.oauth2 import service_account
import json


class DisplayAdminPage(LoginRequiredMixin, TemplateView):
    template_name = 'displayAdminPage.html'

class DisplayRevenueMonth(LoginRequiredMixin, View):
    def get(self, request):
        payments = Payment.objects.all()
        return render(request, 'displayRevenueMonth.html',{'payments': payments})

class DisplayPaymentList(LoginRequiredMixin, View):
    def get(self, request,):
        users = User.objects.all()
        users_count = users.count()
        object = Payment.objects.all()
        object_count = object.count()
        context = { 
            'users' : users,
            'users_count': users_count,
            'object': object,
            'object_count': object_count,
        }
        return render(request, 'displayPaymentList.html', context)
     
class DisplayAllUsers(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        users_count = users.count()
        object = Payment.objects.all()
        object_count = object.count()
        context = {
            'users' : users,
            'users_count': users_count, 
            'object': object,
            'object_count': object_count,
        }
        return render(request, 'displayAllUsers.html',context )

class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, id):
        users = User.objects.get(pk = id)
        users.delete()
        users = User.objects.all()
        return render(request, 'displayAllUsers.html',{'users': users} )

class DisplayUsersMonthly(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'displayUsersMonthly.html',{'users': users} )

        
class DisplayLandingPage(TemplateView):
    template_name = 'displayLandingPage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'), )
        return super().get(request, *args, **kwargs)

class CreateAccountPage(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'createAccountPage.html'
    success_url = reverse_lazy('DisplayLoginPage')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['date_today'] = datetime.strftime(date.today(), "%Y-%m-%d")
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))
        return super().get(request, *args, **kwargs)
        
class DisplayLoginPage(LoginView):
    template_name = 'loginPage.html'
    next_page = 'DisplayClientSide'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))
        return super().get(request, *args, **kwargs)

class LogoutView(LoginRequiredMixin, View):
    redirect_url = settings.LOGIN_URL
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.redirect_url)

class PasswordResetPage(aviews.PasswordResetView):
    template_name = 'resetPassword.html'
    email_template_name = 'email_template.html'
    subject_template_name = "email_subject.txt"

    def post(self, request, *args, **kwargs):
        user = User.objects.all().filter(email=request.POST['email'])
        if len(user) == 0:
            messages.error(request, "The email you entered is not associated with any account.")
            return HttpResponseRedirect(reverse_lazy('reset_password'))
        return super().post(request, *args, **kwargs)

class PasswordResetEmailSentPage(aviews.PasswordResetDoneView):
    template_name = 'resetPasswordSent.html'

class PasswordResetConfirmPage(aviews.PasswordResetConfirmView):
    template_name = 'resetPasswordConfirm.html'

class PasswordResetCompleteView(aviews.PasswordResetCompleteView):
    template_name = 'resetPasswordComplete.html'
 
class DisplayClientSide(LoginRequiredMixin, TemplateView):
    template_name = 'displayClientSide.html'

class DisplayAccountPage(LoginRequiredMixin, TemplateView):
    template_name = 'displayAccountPage.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        CBCList = self.request.user.cbctestresult_set.all().order_by('dateRequested').values()
        if len(CBCList) > 0:
            latestCBC = CBCList[len(CBCList)-1]
            context['latestCBC'] = datetime.strftime(latestCBC.get('dateRequested'), "%Y-%m-%d")
        else:
            context['latestCBC'] = 'None'
            
        self.request.user.birthdate = None if self.request.user.birthdate is None else datetime.strftime(self.request.user.birthdate, "%Y-%m-%d")
        return self.render_to_response(context)

   
class UpdateAccountPage(LoginRequiredMixin, UpdateView):
    template_name = 'updateAccountPage.html'
    model = User
    form_class = UpdateAccountForm
    success_url = reverse_lazy('DisplayAccountPage')

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            CBCList = self.request.user.cbctestresult_set.all().order_by('dateRequested').values()
            if len(CBCList) > 0:
                latestCBC = CBCList[len(CBCList)-1]
                context['latestCBC'] = datetime.strftime(latestCBC.get('dateRequested'), "%Y-%m-%d")
            else:
                context['latestCBC'] = 'None'
            return context

    def get_object(self, queryset = None):
        userObject = self.request.user
        userObject.birthdate = None if self.request.user.birthdate is None else datetime.strftime(self.request.user.birthdate, "%Y-%m-%d")
        return userObject

class UpdatePasswordPage(LoginRequiredMixin, PasswordChangeView):
    template_name = 'updatePasswordPage.html'
    success_url = reverse_lazy('UpdateAccountPage')

class UpdatePhotoPage(LoginRequiredMixin, UpdateView):
    template_name = 'updatePhotoPage.html'
    model = User
    form_class = UpdatePhotoForm
    success_url = reverse_lazy('UpdateAccountPage')

    def get_object(self, queryset = None):
        return self.request.user

class DeleteAccountPage(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('DisplayLoginPage')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))

    def get_object(self, queryset = None):
        return self.request.user

class DisplayAllCBCTestResult(LoginRequiredMixin, View):
    template_name = 'displayAllCBCTestResult.html'
    model = User

    def get(self, request, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        object_list = user.cbctestresult_set.all()
        context = {'object_list': object_list}
        return render(request, self.template_name, context)

class DisplayCBCTestResult(LoginRequiredMixin, View):
    template_name = 'displayCBCTestResult.html'
    redirect_template_name = 'DisplayAllCBCTestResult'
    error_message = 'The record was not found.'
    model = User

    def get(self, request, id, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        try:
            object = user.cbctestresult_set.get(id=id)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        
        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        context = {'object': object}
        return render(request, self.template_name, context)


# Marc John Corral

class AddingCBCTestResultOptions(LoginRequiredMixin, View):
    template_name = 'AddingCBCTestResultOptions.html'
    redirect_template_name = 'LogoutView'
    error_message = 'The user was not found.'
    model = User

    def getUser(self, request):
        return self.model.objects.get(id=request.user.id)
    
    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
        return render(request, template_name, context)

    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.error_message)
            return self.redirectTemplate(self.redirect_template_name)
        
        
        context = {'user': user}
        return self.renderTemplate(request, self.template_name, context)

class PaymentCompletion(LoginRequiredMixin, View):
    redirect_payment_template_name = 'PaymentMethod'
    redirect_logout_template_name = 'LogoutView'
    redirect_image_template_name = 'UploadCBCTestResultImage'
    redirect_picture_template_name = 'CaptureCBCTestResultImage'
    redirect_pdf_template_name = 'UploadCBCTestResultPDF'
    redirect_docx_template_name = 'UploadCBCTestResultDocument'
    redirect_pay_template_name = 'AddingCBCTestResultOptions'
    promo_error_message = 'The promo was not found.'
    user_error_message = 'The user was not found.'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    success_message = 'Payment Successful!'
    user_model = User
    promo_model = Promo
    payment_model = Payment
    
    def getPromo(self, id):
        return self.promo_model.objects.get(id=id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def addUserUploads(self, user, promo):
        user.uploads = user.uploads + promo.uploads
        user.save()
    
    def savePayment(self, user, promo):
        new_payment = self.payment_model.objects.create( promo=promo, user=user, date=self.payment_model.current_time())
        new_payment.save()

    def redirectTemplate(self, template_name):
        return redirect(template_name)

    def get(self, request, type, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        try:
            promo = self.getPromo(id)
        except:
            self.sendErrorMessage(request, self.promo_error_message)
            return self.redirectTemplate(self.redirect_payment_template_name)

        try:
            self.addUserUploads(user, promo)
            self.savePayment(user, promo)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            return self.redirectTemplate(self.redirect_payment_template_name)
        
        self.sendSuccessMessage(request, self.success_message)

        if type == 'image':
            return self.redirectTemplate(self.redirect_image_template_name)
        elif type == 'picture':
            return self.redirectTemplate(self.redirect_picture_template_name)
        elif type == 'pdf':
            return self.redirectTemplate(self.redirect_pdf_template_name)
        elif type == 'docx':
            return self.redirectTemplate(self.redirect_docx_template_name)
        elif type == 'pay':
            return self.redirectTemplate(self.redirect_pay_template_name)

class PaymentMethod(LoginRequiredMixin, View):
    template_name = 'PaymentMethod.html'
    redirect_tests_template_name = 'DisplayAllCBCTestResult'
    redirect_logout_template_name = 'LogoutView'
    user_error_message = 'The user was not found!'
    promo_error_message = 'The promo was not found!'
    type_error_message = 'There was something wrong with the URL!'
    user_model = User
    promo_model = Promo

    def getPromo(self, id):
        return self.promo_model.objects.get(id=id)

    def getUser(self, request):
        self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
        return render(request, template_name, context)

    def get(self, request, type, id):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        if type != 'pdf' and type != 'docx' and type != 'picture' and type != 'image' and type != 'pay':
            self.sendErrorMessage(request, self.type_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        try:
            object = self.getPromo(id)
        except:
            self.sendErrorMessage(request, self.promo_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        context = {'type': type, 'object': object}
        return self.renderTemplate(request, self.template_name, context)

class PromoOptions(LoginRequiredMixin, View):
    template_name = 'PromoOptions.html'
    redirect_tests_template_name = 'DisplayAllCBCTestResult'
    redirect_logout_template_name = 'LogoutView'
    type_error_message = 'There was something wrong with the URL!'
    user_error_message = 'The user was not found!'
    promo_error_message = 'Their was something wrong with the promos!'
    user_model = User
    promo_model = Promo

    def getUser(self, request):
        self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def getPromos(self):
        return self.promo_model.objects.all()
    
    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
        return render(request, template_name, context)

    def get(self, request, type):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        if type != 'pdf' and type != 'docx' and type != 'picture' and type != 'image' and type != 'pay':
            self.sendErrorMessage(request, self.type_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        try:
            object_list = self.getPromos()
        except:
            self.sendErrorMessage(request, self.promo_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        context = {'type': type, 'object_list': object_list}
        return self.renderTemplate(request, self.template_name, context)
       

class UploadCBCTestResultPDF(LoginRequiredMixin, View):
    template_name = 'UploadCBCTestResultFile.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'PromoOptions'
    redirect_logout_template_name = 'LogoutView'
    upload_error_message = 'You have no more uploads!'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    user_error_message = 'The user was not found!'
    success_message = 'Upload PDF Successful!'
    user_model = User
    pdf_model = CBCTestResultPDF

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def deductAvailableUploads(self, user):
        user.uploads = user.uploads - 1
        user.save()

    def savePDF(self, request):
        object = self.pdf_model()
        object.set_testPDF(request.FILES.get('testPDF'))
        object.save()
        return object.get_id()

    def redirectTemplate(self, template_name, type = None, id = None):
        if id == None:
            if type == None:
                return redirect(template_name)
            else:
                return redirect(template_name, type = type)
        else:
            return redirect(template_name, type = type, id = id)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def post(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        try:
            self.deductAvailableUploads(user)
            pdf_id = self.savePDF(request)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            context = {'type': 'pdf'}
            return self.renderTemplate(request, self.template_name, context)
        
        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_create_template_name, 'pdf', pdf_id)

    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        if user.uploads <= 0:
            self.sendErrorMessage(request, self.upload_error_message)
            return self.redirectTemplate(self.redirect_promo_template_name, 'pdf')

        context = {'type': 'pdf'}
        return self.renderTemplate(request, self.template_name, context)

class UploadCBCTestResultDocument(LoginRequiredMixin, View):
    template_name = 'UploadCBCTestResultFile.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'PromoOptions'
    redirect_logout_template_name = 'LogoutView'
    upload_error_message = 'You have no more uploads!'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    user_error_message = 'The user was not found!'
    success_message = 'Upload Docx Successful!'
    user_model = User
    docx_model = CBCTestResultDocument

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def deductAvailableUploads(self, user):
        user.uploads = user.uploads - 1
        user.save()

    def saveDocument(self, request):
        object = self.docx_model()
        object.set_testDocx(request.FILES.get('testDocx'))
        object.save()
        return object.get_id()

    def redirectTemplate(self, template_name, type = None, id = None):
        if id == None:
            if type == None:
                return redirect(template_name)
            else:
                return redirect(template_name, type = type)
        else:
            return redirect(template_name, type = type, id = id)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def post(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        try:
            self.deductAvailableUploads(user)
            docx_id = self.saveDocument(request)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            context = {'type': 'docx'}
            return self.renderTemplate(request, self.template_name, context)
        
        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_create_template_name, 'docx', docx_id)
    
    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        if user.uploads <= 0:
            self.sendErrorMessage(request, self.upload_error_message)
            return self.redirectTemplate(self.redirect_promo_template_name, 'docx')

        context = {'type': 'docx'}
        return self.renderTemplate(request, self.template_name, context)

class UploadCBCTestResultImage(LoginRequiredMixin, View):
    template_name = 'UploadCBCTestResultFile.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'PromoOptions'
    redirect_logout_template_name = 'LogoutView'
    upload_error_message = 'You have no more uploads!'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    user_error_message = 'The user was not found!'
    success_message = 'Upload Image Successful!'
    user_model = User
    image_model = CBCTestResultImage

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def deductAvailableUploads(self, user):
        user.uploads = user.uploads - 1
        user.save()

    def saveImage(self, request):
        object = self.image_model()
        object.set_testImage(request.FILES.get('testImage'))
        object.save()
        return object.get_id()

    def redirectTemplate(self, template_name, type = None, id = None):
        if id == None:
            if type == None:
                return redirect(template_name)
            else:
                return redirect(template_name, type = type)
        else:
            return redirect(template_name, type = type, id = id)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def post(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        try:
            self.deductAvailableUploads(user)
            image_id = self.saveImage(request)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            context = {'type': 'image'}
            return self.renderTemplate(request, self.template_name, context)
        
        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_create_template_name, 'image', image_id)

    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        if user.uploads <= 0:
            self.sendErrorMessage(request, self.upload_error_message)
            return self.redirectTemplate(self.redirect_promo_template_name, 'image')

        context = {'type': 'image'}
        return self.renderTemplate(request, self.template_name, context)

class CaptureCBCTestResultImage(LoginRequiredMixin, View):
    template_name = 'CaptureCBCTestResultImage.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'PromoOptions'
    redirect_logout_template_name = 'LogoutView'
    upload_error_message = 'You have no more uploads!'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    user_error_message = 'The user was not found!'
    success_message = 'Capture Image Successful!'
    user_model = User
    image_model = CBCTestResultImage

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)
    
    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def deductAvailableUploads(self, user):
        user.uploads = user.uploads - 1
        user.save()

    def saveImage(self, request):
        image_path = request.POST["src"] 
        image_temp_file = NamedTemporaryFile()
        image_temp_file.write(urlopen(image_path).read())
        file_name = 'cbc.jpg'
        image_temp_file.flush()
        temp_file = File(image_temp_file, name=file_name)
        object = self.image_model() 
        object.set_testImage(temp_file)
        object.save()
        return object.get_id()

    def redirectTemplate(self, template_name, type=None, id = None):
        if id == None:
            if type == None:
                return redirect(template_name)
            else:
                return redirect(template_name, type = type)
        else:
            return redirect(template_name, type = type, id = id)
    
    def renderTemplate(self, request, template_name):
         return render(request, template_name)

    def post(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        self.deductAvailableUploads(user)
        image_id = self.saveImage(request)


        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_create_template_name, 'picture', image_id)
    
    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        
        if user.uploads <= 0:
            self.sendErrorMessage(request, self.upload_error_message)
            return self.redirectTemplate(self.redirect_promo_template_name, 'picture')

        return self.renderTemplate(request, self.template_name)

class CreateCBCTestResult(LoginRequiredMixin, View):
    test_model = CBCTestResult
    docx_model = CBCTestResultDocument
    image_model = CBCTestResultImage
    pdf_model = CBCTestResultPDF
    user_model = User
    redirect_adding_template_name = 'AddingCBCTestResultOptions'
    redirect_test_template_name = 'DisplayCBCTestResult'
    redirect_docx_template_name = 'UploadCBCTestResultDocument'
    redirect_pdf_template_name = 'UploadCBCTestResultPDF'
    redirect_image_template_name = 'UploadCBCTestResultImage'
    redirect_picture_template_name = 'CaptureCBCTestResultImage'
    redirect_tests_template_name = 'DisplayAllCBCTestResult'
    redirect_logout_template_name = 'LogoutView'
    file_error_message = 'Could not find the file uploaded!'
    url_error_message = 'There was something wrong with the url!'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    values_error_message = 'There was something wrong with your file or you uploaded the wrong file. Please try another one.'
    picture_error_message = 'Your image maybe unclear. Use a camera with higher quality. Or maybe you uploaded the wrong image.'
    user_error_message = 'The user was not found!'
    template_name = 'CreateCBCTestResult.html'
    success_message = 'Create CBC Test Result Successful!'


    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def redirectTemplate(self, template_name, id = None):
        if id == None:
            return redirect(template_name)
        else:
            return redirect(template_name, id = id)
        
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)
    
    def saveTest(self, request, type, id):
        object = self.test_model()
        if type == 'docx':
            try:
                object.set_testDocx(self.docx_model.objects.get(id=id)) 
            except:
                self.sendErrorMessage(request, self.file_error_message)
                return self.redirectTemplate(self.redirect_adding_template_name)
        elif type == 'pdf':
            try: 
                object.set_testPDF(self.pdf_model.objects.get(id=id))
            except:
                self.sendErrorMessage(request, self.file_error_message)
                return self.redirectTemplate(self.redirect_adding_template_name)
        elif type == 'image' or type == 'picture':
            try:
                object.set_testImage(self.image_model.objects.get(id=id))
            except:
                self.sendErrorMessage(request, self.file_error_message)
                return self.redirectTemplate(self.redirect_adding_template_name)
        else:
            self.sendErrorMessage(request, self.file_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        date_time_str = request.POST.get('dateRequested')
        try:
            unaware_date = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M')
            object.set_dateRequested(pytz.utc.localize(unaware_date)) 
        except:
            object.set_dateRequested(None)
        
        date_time_str = request.POST.get('dateReceived')
        try:
            unaware_date = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M')
            object.set_dateReceived(pytz.utc.localize(unaware_date)) 
        except:
            object.set_dateReceived(None)

        object.set_user(User.objects.get(id=request.user.id))
        object.set_source(request.POST.get('source')) 
        object.set_labNumber(request.POST.get('labNumber')) 
        object.set_pid(request.POST.get('pid')) 
        object.set_whiteBloodCells(request.POST.get('whiteBloodCells')) 
        object.set_redBloodCells(request.POST.get('redBloodCells')) 
        object.set_hemoglobin(request.POST.get('hemoglobin')) 
        object.set_hematocrit( request.POST.get('hematocrit')) 
        object.set_meanCorpuscularVolume(request.POST.get('meanCorpuscularVolume')) 
        object.set_meanCorpuscularHb(request.POST.get('meanCorpuscularHb')) 
        object.set_meanCorpuscularHbConc(request.POST.get('meanCorpuscularHbConc')) 
        object.set_rbcDistributionWidth(request.POST.get('rbcDistributionWidth')) 
        object.set_plateletCount(request.POST.get('plateletCount')) 
        object.set_neutrophils(request.POST.get('neutrophils')) 
        object.set_lymphocytes(request.POST.get('lymphocytes')) 
        object.set_monocytes(request.POST.get('monocytes')) 
        object.set_eosinophils(request.POST.get('eosinophils')) 
        object.set_basophils(request.POST.get('basophils')) 
        object.set_bands(request.POST.get('bands')) 
        object.set_absoluteNeutrophilsCount(request.POST.get('absoluteNeutrophilsCount')) 
        object.set_absoluteLymphocyteCount(request.POST.get('absoluteLymphocyteCount')) 
        object.set_absoluteMonocyteCount(request.POST.get('absoluteMonocyteCount')) 
        object.set_absoluteEosinophilCount(request.POST.get('absoluteEosinophilCount')) 
        object.set_absoluteBasophilCount(request.POST.get('absoluteBasophilCount')) 
        object.set_absoluteBandCount(request.POST.get('absoluteBandCount')) 
        object.save()
        return object.get_id()
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)
    
    def getDocument(self, id):
        return self.docx_model.objects.get(id=id)

    def getDocxInitialValues(self, docxObject, id):
        data = {}
        data['object'] = docxObject
        FILE_PATH = docxObject.testDocx.url
        txt = d2t.process(smart_open(FILE_PATH, 'rb'))

        values = txt.split()

        data['pid'] = values[5]

        data['source'] = values[11]

        data['labNumber'] = values[14]

        data['dateRequested'] = values[23]+" "+values[24]+" "+values[25]
        if "PM" in data['dateRequested']:
            dateArr = data['dateRequested'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateRequested'] = data['dateRequested'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateRequested'] = finalDate

        elif "AM" in data['dateRequested']:
            data['dateRequested'] = data['dateRequested'][:-3]

        data['dateReceived'] = values[27]+" "+values[28]+" "+values[29]
        if "PM" in data['dateReceived']:
            dateArr = data['dateReceived'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateReceived'] = data['dateReceived'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateReceived'] = finalDate

        elif "AM" in data['dateReceived']:
            data['dateReceived'] = data['dateReceived'][:-3]

        data['whiteBloodCells'] = values[42]

        data['redBloodCells'] = values[48]

        data['hemoglobin'] = values[52]

        data['hematocrit'] = values[56]

        data['meanCorpuscularVolume'] = values[62]

        data['meanCorpuscularHb'] = values[68]

        data['meanCorpuscularHbConc'] = values[75]

        data['rbcDistributionWidth'] = values[81]

        data['plateletCount'] = values[86]

        data['neutrophils'] = values[93]

        data['lymphocytes'] = values[97]

        data['monocytes'] = values[101]

        data['eosinophils'] = values[105]

        data['basophils'] = values[109]

        data['bands'] = values[113]

        data['absoluteNeutrophilsCount'] = values[122]

        data['absoluteLymphocyteCount'] = values[128]

        data['absoluteMonocyteCount'] = values[134]

        data['absoluteEosinophilCount'] = values[140]

        data['absoluteBasophilCount'] = values[146]

        data['absoluteBandCount'] = values[152]
        
        return data
    
    def addUserUploads(self, user):
        user.uploads = user.uploads + 1
        user.save()

    def getPDF(self, id):
        return self.pdf_model.objects.get(id=id)
    
    def getPDFInitialValues(self, pdfObject, id):
        data = {}
        data['object'] = pdfObject
        FILE_PATH = pdfObject.testPDF.url

        txt = extract_text(smart_open(FILE_PATH, 'rb'))

        values = txt.split()

        data['pid'] = values[7]

        data['source'] = values[5]

        data['labNumber'] = values[14]

        data['dateRequested'] = values[23]+" "+values[24]+" "+values[25]
        if "PM" in data['dateRequested']:
            dateArr = data['dateRequested'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateRequested'] = data['dateRequested'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateRequested'] = finalDate

        elif "AM" in data['dateRequested']:
            data['dateRequested'] = data['dateRequested'][:-3]

        data['dateReceived'] = values[27]+" "+values[28]+" "+values[29]
        if "PM" in data['dateReceived']:
            dateArr = data['dateReceived'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateReceived'] = data['dateReceived'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateReceived'] = finalDate

        elif "AM" in data['dateReceived']:
            data['dateReceived'] = data['dateReceived'][:-3]

        data['whiteBloodCells'] = values[53]

        data['redBloodCells'] = values[54]

        data['hemoglobin'] = values[55]

        data['hematocrit'] = values[56]

        data['meanCorpuscularVolume'] = values[57]

        data['meanCorpuscularHb'] = values[58]

        data['meanCorpuscularHbConc'] = values[63]

        data['rbcDistributionWidth'] = values[99]

        data['plateletCount'] = values[100]

        data['neutrophils'] = values[101]

        data['lymphocytes'] = values[102]

        data['monocytes'] = values[103]

        data['eosinophils'] = values[104]

        data['basophils'] = values[105]

        data['bands'] = values[106]

        data['absoluteNeutrophilsCount'] = values[107]

        data['absoluteLymphocyteCount'] = values[108]

        data['absoluteMonocyteCount'] = values[109]

        data['absoluteEosinophilCount'] = values[110]

        data['absoluteBasophilCount'] = values[111]

        data['absoluteBandCount'] = values[112]
        
        return data

    def getImage(self, id):
        return self.image_model.objects.get(id=id)

    def getImageInitialValues(self, imgObject, id):
        data = {}
        data['object'] = imgObject
        FILE_PATH = imgObject.testImage.url

        # the json credentials stored as env variable
        json_str = os.environ.get('GOOGLE_CREDENTIALS')
        # project name
        gcp_project = os.environ.get('Isabuhay_Project') 

        # generate json - if there are errors here remove newlines in .env
        json_data = json.loads(json_str)
        # the private_key needs to replace \n parsed as string literal with escaped newlines
        json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')

        # use service_account to generate credentials object
        credentials = service_account.Credentials.from_service_account_info(
            json_data)

        # pass credentials AND project name to new client object (did not work wihout project name)
        client = vision.ImageAnnotatorClient(credentials=credentials)

        with smart_open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)  
        df = pd.DataFrame(columns=['locale', 'description'])

        texts = response.text_annotations
        for text in texts:
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description
                ),
                ignore_index=True
            )
        
        data['labNumber'] = df['description'][114]
        data['source'] = df['description'][110]
        data['pid'] = df['description'][9]

        data['dateRequested'] = df['description'][18] + ' ' + df['description'][19] + ' ' + df['description'][20]
        if "PM" in data['dateRequested']:
            dateArr = data['dateRequested'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateRequested'] = data['dateRequested'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateRequested'] = finalDate

        elif "AM" in data['dateRequested']:
            data['dateRequested'] = data['dateRequested'][:-3]

        data['dateReceived'] = df['description'][126] + ' ' + df['description'][127] + ' ' + df['description'][128] 
        if "PM" in data['dateReceived']:
            dateArr = data['dateReceived'].split()
            
            newHour = int(dateArr[1][:2]) + 12
            
            if newHour > 23:
                data['dateReceived'] = data['dateReceived'][:-3]
            else:
                dateArr[1] = str(newHour) + dateArr[1][2:]
                finalDate = dateArr[0] + " " + dateArr[1]
                data['dateReceived'] = finalDate

        elif "AM" in data['dateReceived']:
            data['dateReceived'] = data['dateReceived'][:-3]
        
        data['whiteBloodCells'] = df['description'][87]
        data['redBloodCells'] = df['description'][88]
        data['hemoglobin'] = df['description'][89]
        data['hematocrit'] = df['description'][90]
        data['meanCorpuscularVolume'] = df['description'][91]
        data['meanCorpuscularHb'] = df['description'][92]
        data['meanCorpuscularHbConc'] = df['description'][93]
        data['rbcDistributionWidth'] = df['description'][94]
        data['plateletCount'] = df['description'][95]
        data['neutrophils'] = df['description'][96]
        data['lymphocytes'] = df['description'][97]
        data['monocytes'] = df['description'][98]
        data['eosinophils'] = df['description'][99]
        data['basophils'] = df['description'][100]
        data['bands'] = df['description'][101]
        data['absoluteNeutrophilsCount'] = df['description'][102]
        data['absoluteLymphocyteCount'] = df['description'][103]
        data['absoluteMonocyteCount'] = df['description'][104]
        data['absoluteEosinophilCount'] = df['description'][105]
        data['absoluteBasophilCount'] = df['description'][106]
        data['absoluteBandCount'] = df['description'][107]

        return data
    
    def deleteTest(self, object):
        object.delete()

    def post(self, request, type, id):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            test_id = self.saveTest(request, type, id)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            if type == 'docx':
                _, data = self.getDocxInitialValues(id)
            elif type == 'pdf':
                _, data = self.getPDFInitialValues(id)
            elif type == 'image' or type == 'picture':
                _, data = self.getImageInitialValues(id)

            data['type'] = type
            return self.renderTemplate(request, self.template_name, data)
        
        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_test_template_name, test_id)

    def get(self, request, type, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        if type == 'docx':
            try: 
                docxObject = self.getDocument(id)
                data = self.getDocxInitialValues(docxObject, id)
                
                if (data['source'] != "APPCARE" and data['source'] != "WEBCARE") or data['labNumber'].isnumeric() == False: 
                    self.deleteTest(docxObject)
                    self.sendErrorMessage(request, self.values_error_message)
                    self.addUserUploads(user)
                    return self.redirectTemplate(self.redirect_docx_template_name)
            except:
                self.deleteTest(docxObject)
                self.sendErrorMessage(request, self.values_error_message)
                self.addUserUploads(user)
                return self.redirectTemplate(self.redirect_docx_template_name)
        elif type == 'pdf':
            try: 
                pdfObject = self.getPDF(id)
                data = self.getPDFInitialValues(pdfObject, id)
                
                if (data['source'] != "APPCARE" and data['source'] != "WEBCARE") or data['labNumber'].isnumeric() == False: 
                    self.deleteTest(pdfObject)
                    self.sendErrorMessage(request, self.values_error_message)
                    self.addUserUploads(user)
                    return self.redirectTemplate(self.redirect_pdf_template_name)
            except:
                self.deleteTest(pdfObject)
                self.sendErrorMessage(request, self.values_error_message)
                self.addUserUploads(user)
                return self.redirectTemplate(self.redirect_pdf_template_name)
        elif type == 'image' or type == 'picture':
            try: 
                imgObject = self.getImage(id)
                data = self.getImageInitialValues(imgObject, id)
                
                if (data['source'] != "APPCARE" and data['source'] != "WEBCARE") or data['labNumber'].isnumeric() == False: 
                    self.deleteTest(imgObject)
                    self.sendErrorMessage(request, self.picture_error_message)
                    self.addUserUploads(user)
                    if type == 'image':
                        return self.redirectTemplate(self.redirect_image_template_name)
                    elif type == 'picture':
                        return self.redirectTemplate(self.redirect_picture_template_name)
            except:
                self.deleteTest(imgObject)
                self.sendErrorMessage(request, self.picture_error_message)
                self.addUserUploads(user)
                if type == 'image':
                        return self.redirectTemplate(self.redirect_image_template_name)
                elif type == 'picture':
                    return self.redirectTemplate(self.redirect_picture_template_name)
        else:
            self.sendErrorMessage(request, self.url_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        data['type'] = type

        return self.renderTemplate(request, self.template_name, data)

class UpdateCBCTestResult(LoginRequiredMixin, View):
    template_name = 'UpdateCBCTestResult.html'
    redirect_tests_template_name = 'DisplayAllCBCTestResult'
    redirect_test_template_name = 'DisplayCBCTestResult'
    redirect_logout_template_name = 'LogoutView'
    user_error_message = 'The user was not found!'
    record_error_message = 'The record was not found.'
    saving_error_message = 'Something went wrong with the saving process. Please try again!'
    succes_message = 'Update CBC Test Result Successful!'
    test_model = CBCTestResult
    user_model = User

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name, id = None):
        if id == None:
            return redirect(template_name)
        else:
            return redirect(template_name, id = id)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def updateTest(self, request, object):
        date_time_str = request.POST.get('dateRequested')
        try:
            unaware_date = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M')
            object.set_dateRequested(pytz.utc.localize(unaware_date)) 
        except:
            object.set_dateRequested(None)
        
        date_time_str = request.POST.get('dateReceived')
        try:
            unaware_date = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M')
            object.set_dateReceived(pytz.utc.localize(unaware_date)) 
        except:
            object.set_dateReceived(None)

        object.set_user(User.objects.get(id=request.user.id))
        object.set_source(request.POST.get('source')) 
        object.set_labNumber(request.POST.get('labNumber')) 
        object.set_pid(request.POST.get('pid')) 
        object.set_whiteBloodCells(request.POST.get('whiteBloodCells')) 
        object.set_redBloodCells(request.POST.get('redBloodCells')) 
        object.set_hemoglobin(request.POST.get('hemoglobin')) 
        object.set_hematocrit( request.POST.get('hematocrit')) 
        object.set_meanCorpuscularVolume(request.POST.get('meanCorpuscularVolume')) 
        object.set_meanCorpuscularHb(request.POST.get('meanCorpuscularHb')) 
        object.set_meanCorpuscularHbConc(request.POST.get('meanCorpuscularHbConc')) 
        object.set_rbcDistributionWidth(request.POST.get('rbcDistributionWidth')) 
        object.set_plateletCount(request.POST.get('plateletCount')) 
        object.set_neutrophils(request.POST.get('neutrophils')) 
        object.set_lymphocytes(request.POST.get('lymphocytes')) 
        object.set_monocytes(request.POST.get('monocytes')) 
        object.set_eosinophils(request.POST.get('eosinophils')) 
        object.set_basophils(request.POST.get('basophils')) 
        object.set_bands(request.POST.get('bands')) 
        object.set_absoluteNeutrophilsCount(request.POST.get('absoluteNeutrophilsCount')) 
        object.set_absoluteLymphocyteCount(request.POST.get('absoluteLymphocyteCount')) 
        object.set_absoluteMonocyteCount(request.POST.get('absoluteMonocyteCount')) 
        object.set_absoluteEosinophilCount(request.POST.get('absoluteEosinophilCount')) 
        object.set_absoluteBasophilCount(request.POST.get('absoluteBasophilCount')) 
        object.set_absoluteBandCount(request.POST.get('absoluteBandCount')) 
        object.save()

    def getTest(self, id):
        return self.test_model.objects.get(id=id)

    def getUser(self, request):
        self.user_model.objects.get(id=request.user.id)

    def getCorrectDateFormat(self, object):
        date_time_str = object
        dateArr = date_time_str.split()
        yearArr = dateArr[0].split('-')
        return yearArr[1]+ '-' + yearArr[2]+ '-' + yearArr[0] + ' ' + dateArr[1]
        
    def post(self, request, id):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)
        try:
            object = self.getTest(id)
        except:
            self.sendErrorMessage(request, self.record_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        try:
            self.updateTest(request, object)
        except:
            self.sendErrorMessage(request, self.saving_error_message)
            context = {'object': object}
            return self.renderTemplate(request, self.template_name, context)

        messages.success(request, self.succes_message)
        return self.redirectTemplate(self.redirect_test_template_name, id)

    def get(self, request, id):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            object = self.getTest(id)
        except:
            self.sendErrorMessage(request, self.record_error_message)
            return self.redirectTemplate(self.redirect_tests_template_name)

        dateRequestedStr = self.getCorrectDateFormat(str(object.dateRequested)[:-9])
        dateReceivedStr = self.getCorrectDateFormat(str(object.dateReceived)[:-9])

        context = {'object': object, 'dateRequestedStr': dateRequestedStr, 'dateReceivedStr': dateReceivedStr}
        return self.renderTemplate(request, self.template_name, context)

class DeleteCBCTestResult(LoginRequiredMixin, View):
    template_name = 'DeleteCBCTestResult.html'
    redirect_template_name = 'DisplayAllCBCTestResult'
    record_error_message = 'The record was not found!'
    deletion_error_message = 'Something went wrong with the deletion process!'
    success_message = 'Delete CBC Test Result Successful!'
    model = CBCTestResult

    def getTest(self, id):
        return self.model.objects.get(id=id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def deleteTest(self, object):
        object.delete()

    def post(self, request, id):
        try:
            object = self.getTest(id)
        except:
            self.sendErrorMessage(request, self.record_error_message)
            return self.redirectTemplate(self.redirect_template_name)

        try:
            self.deleteTest(object)
        except:
            self.sendErrorMessage(request, self.deletion_error_message)
            return self.redirectTemplate(self.redirect_template_name)

        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_template_name)

class DeleteCBCTestResultImage(LoginRequiredMixin, View):
    template_name = 'DeleteCBCTestResultFile.html'
    redirect_logout_template_name = 'LogoutView'
    redirect_adding_template_name = 'AddingCBCTestResultOptions'
    redirect_image_template_name = 'UploadCBCTestResultImage'
    redirect_picture_template_name = 'CaptureCBCTestResultImage'
    image_error_message = 'The image was not found.'
    user_error_message = 'The user was not found.'
    deletion_error_message = 'Something went wrong with the deletion process!'
    success_message = 'Delete Image Successful!'
    image_model = CBCTestResultImage
    user_model = User

    def getImage(self, id):
        return self.image_model.objects.get(id=id)
    
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name, type=None, id=None):
        if type == None and id == None:
            return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def addUserUploads(self, user):
        user.uploads = user.uploads + 1
        user.save()
    
    def deleteImage(self, object):
        object.delete()

    def post(self, request, type, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            object = self.getImage(id)
        except:
            self.sendErrorMessage(request, self.image_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        try:
            self.deleteImage(object)
            self.addUserUploads(user)
        except:
            self.sendErrorMessage(request, self.deletion_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        self.sendSuccessMessage(request, self.success_message)

        if type == 'image':
            return self.redirectTemplate(self.redirect_image_template_name)
        elif type == 'picture':
            return self.redirectTemplate(self.redirect_picture_template_name)

class DeleteCBCTestResultPDF(LoginRequiredMixin, View):
    template_name = 'DeleteCBCTestResultFile.html'
    redirect_logout_template_name = 'LogoutView'
    redirect_adding_template_name = 'AddingCBCTestResultOptions'
    redirect_upload_template_name = 'UploadCBCTestResultPDF'
    pdf_error_message = 'The pdf was not found.'
    user_error_message = 'The user was not found.'
    deletion_error_message = 'Something went wrong with the deletion process!'
    success_message = 'Delete PDF Successful!'
    pdf_model = CBCTestResultPDF
    user_model = User

    def getPDF(self, id):
        return self.pdf_model.objects.get(id=id)
    
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def addUserUploads(self, user):
        user.uploads = user.uploads + 1
        user.save()
    
    def deletePDF(self, object):
        object.delete()

    def post(self, request, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        try:
            object = self.getPDF(id)
        except:
            self.sendErrorMessage(request, self.pdf_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)
                
        try:
            self.deletePDF(object)
            self.addUserUploads(user)

        except:
            self.sendErrorMessage(request, self.deletion_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        self.sendSuccessMessage(request, self.success_message)

        return self.redirectTemplate(self.redirect_upload_template_name)

class DeleteCBCTestResultDocument(LoginRequiredMixin, View):
    template_name = 'DeleteCBCTestResultFile.html'
    redirect_logout_template_name = 'LogoutView'
    redirect_adding_template_name = 'AddingCBCTestResultOptions'
    redirect_upload_template_name = 'UploadCBCTestResultDocument'
    docx_error_message = 'The document was not found.'
    user_error_message = 'The user was not found.'
    deletion_error_message = 'Something went wrong with the deletion process!'
    success_message = 'Delete Docx Successful!'
    docx_model = CBCTestResultDocument
    user_model = User
    
    def getDocument(self, id):
        return self.docx_model.objects.get(id=id)
    
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def addUserUploads(self, user):
        user.uploads = user.uploads + 1
        user.save()
    
    def deleteDocument(self, object):
        object.delete()

    def post(self, request, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            object = self.getDocument(id)
        except:
            self.sendErrorMessage(request, self.docx_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        try:
            self.deleteDocument(object)
            self.addUserUploads(user)
        except:
            self.sendErrorMessage(request, self.deletion_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        self.sendSuccessMessage(request, self.success_message)

        return self.redirectTemplate(self.redirect_upload_template_name)

    def get(self, request, id):
        try:
            object = self.getDocx(id)
        except:
            self.sendErrorMessage(request, self.docx_error_message)
            return self.redirectTemplate(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'docx'}
        return self.renderTemplate(request, self.template_name, context)

class ShowChatRoom(LoginRequiredMixin, View):
    redirect_logout_template_name = 'LogoutView'
    redirect_contacts_template_name = 'Contacts'
    redirect_chat_template_name = 'EnterChatRoom'
    error_message = 'The user is not found.'
    model = User

    def getUser(self, request):
        return self.model.objects.get(id=request.user.id)

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        if user.is_admin:
            return self.redirectTemplate(self.redirect_contacts_template_name)
        else:
            return self.redirectTemplate(self.redirect_chat_template_name)

class EnterChatRoom(LoginRequiredMixin, View):
    redirect_logout_template_name = 'LogoutView'
    template_name = 'EnterChatRoom.html'
    redirect_chat_template_name = 'ChatRoom'
    error_message = 'The user is not found.'
    user_model = User
    room_model = Room

    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def renderTemplate(self, request, template_name):
        return render(request, template_name)
    
    def redirectTemplate(self, template_name, id = None):
        if id == None:
            return redirect(template_name)
        else:
            return redirect(template_name, id)
        
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def getRoom(self, user):
        room = user.room_set.first()
        return room.get_id()
    
    def newRoom(self, user):
        new_room = self.room_model.objects.create()
        new_room.set_owner(user)
        new_room.save()
        return new_room.get_id()

    def get(self, request):
        try:
            self.getUser(request)
        except:
            self.sendErrorMessage(request, self.error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        return self.renderTemplate(request, self.template_name)

    def post(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        if user.room_set.first():
            room_id = self.getRoom(user)
            return self.redirectTemplate(self.redirect_chat_template_name, id = room_id)
        else:
            new_room_id = self.newRoom(user)
            return self.redirectTemplate(self.redirect_chat_template_name, id = new_room_id)

class ChatRoom(LoginRequiredMixin, View):
    redirect_logout_template_name = 'LogoutView'
    template_name = 'ChatRoom.html'
    redirect_room_template_name = 'ShowChatRoom'
    user_error_message = 'The user was not found!'
    room_error_message = 'The chat room was not found!'
    read_error_message = 'Something went wrong with the reading process!'
    user_model = User
    room_model = Room

    def getRoom(self, id):
        return self.room_model.objects.get(id=id)
    
    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)
    
    def readMessages(self, room_details, user):
        room_details.message_set.filter(~Q(user__username=user.username)&Q(read=False)).update(read=True)
    
    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
        return render(request, template_name, context)
        
    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def get(self, request, id):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            room_details = self.getRoom(id)
        except:
            self.sendErrorMessage(request, self.room_error_message)
            return self.redirectTemplate(self.redirect_room_template_name)
        
        try:
             self.readMessages(room_details, user)
        except:
            self.sendErrorMessage(request, self.read_error_message)
            return self.redirectTemplate(self.redirect_room_template_name)

        context = {'room_details': room_details}
        return self.renderTemplate(request, self.template_name, context)

class Contacts(LoginRequiredMixin, View):
    redirect_test_template_name = 'DisplayAllCBCTestResult'
    redirect_logout_template_name = 'LogoutView'
    user_error_message = 'The user was not found!'
    rooms_error_message = 'Something is wrong with the Chat Rooms!'
    template_name = 'Contacts.html'
    user_model = User
    room_model = Room

    def redirectTemplate(self, template_name):
        return redirect(template_name)
    
    def renderTemplate(self, request, template_name, context):
         return render(request, template_name, context)

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)
    
    def getRooms(self, user):
        return self.room_model.objects.filter(~Q(owner__username=user.username))
    
    def sendErrorMessage(self, request, message):
        messages.error(request, message)

    def get(self, request):
        try:
            user = self.getUser(request)
        except:
            self.sendErrorMessage(request, self.user_error_message)
            return self.redirectTemplate(self.redirect_logout_template_name)

        try:
            rooms = self.getRooms(user)
        except:
            self.sendErrorMessage(request, self.rooms_error_message)
            return self.redirectTemplate(self.redirect_test_template_name)

        context = {'rooms': rooms}
        return self.renderTemplate(request, self.template_name, context)

class UnreadMessages(LoginRequiredMixin, View):
    user_model = User
    room_model = Room
    admin_name = 'admin'

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def getRooms(self, user):
        return self.room_model.objects.filter(~Q(owner__username=user.username))
    
    def countNotification(self, room, user):
        return room.message_set.filter(~Q(user__username=user.username)&Q(read=False)).count()
    
    def getAdminNotifications(self, user):
        context = {}
        rooms = self.getRooms(user)
        queue = []
        i = 0
        for room in rooms:
            count = self.countNotification(room, user)
            i += 1
            if count == 0:
                queue.append(str(i))
            
            if count > 0 and queue:
                zero_position = queue.pop(0)
                temp_username = context[zero_position][0]
                temp_count = context[zero_position][1]
                temp_room_id = context[zero_position][2]
                context[zero_position] = [room.get_owner().username, count, room.get_id()]
                context[str(i)] = [temp_username, temp_count, temp_room_id]
            else: 
                context[str(i)] = [room.get_owner().username, count, room.get_id()]
        
        return context

    def getUserNotifications(self, user):
        context = {}
        room = user.room_set.first()
        count = self.countNotification(room, user)
        context['0'] = [self.admin_name, count]
        return context

    def get(self, request):
        context = {}
        user = self.getUser(request)
        if user.is_admin:
            context = self.getAdminNotifications(user)
        else:
            if user.room_set.first():
                context = self.getUserNotifications(user)

        return JsonResponse({"messages":context})      

class SendMessage(LoginRequiredMixin, View):
    user_model = User
    room_model = Room
    message_model = Message


    def getUser(self, id): 
        return self.user_model.objects.get(id=id)

    def getRoom(self, id):
        return self.room_model.objects.get(id=id)

    def saveMessage(self, message, user, room):
        new_message = self.message_model.objects.create(value=message, user=user, room=room, date=self.message_model.current_time())
        new_message.save()

    def post(self, request):
        user = self.getUser(request.user.id)

        message = request.POST.get('message')
        room_id = request.POST.get('room_id')

        room = self.getRoom(room_id)

        self.saveMessage(message, user, room)
        
        return HttpResponse('Message sent successfully')

class GetMessages(LoginRequiredMixin, View):
    user_model = User
    room_model = Room

    def getUser(self, request):
        return self.user_model.objects.get(id=request.user.id)

    def getRoom(self, id):
        return self.room_model.objects.get(id=id)
    
    def getMessages(self, room):
        return room.message_set.all()

    def readMessages(self, room, user):
        room.message_set.filter(~Q(user__username=user.username)&Q(read=False)).update(read=True)
    
    def getUserName(self, user):
        return user.username

    def get(self, request, id):
        user = self.getUser(request)
        room = self.getRoom(id)
        messages = self.getMessages(room)
        self.readMessages(room, user)
        username = self.getUserName(user)
        return JsonResponse({"messages":list(messages.values('user__username', 'value', 'date', 'read', 'id')), "username": username})

class DeleteMessage(LoginRequiredMixin, View):
    redirect_chat_template_name = 'ChatRoom'
    redirect_room_template_name = 'ShowChatRoom'
    deletion_error_message = 'Something went wrong with the deletion process!'
    user_error_message = 'User is not the same with the message owner!'
    success_message = 'Message is deleted!'
    message_model = Message

    def getMessage(self, id):
        return self.message_model.objects.get(id=id)
    
    def deleteMessage(self, message):
        message.delete()

    def getRoomId(self, message):
        return message.room.get_id()

    def sendErrorMessage(self, request, message):
        messages.error(request, message)
    
    def sendSuccessMessage(self, request, message):
        messages.success(request, message)
    
    def redirectTemplate(self, template_name, id=None):
        if id == None:
            return  redirect(template_name)
        else:
            return redirect(template_name, id)
    
    def get(self, request, id):
        try:
            message = self.getMessage(id)
            room_id = self.getRoomId(message)
            if message.user.id == request.user.id:
                    self.deleteMessage(message)
            else:
                self.sendErrorMessage(request, self.user_error_message)
                return self.redirectTemplate(self.redirect_chat_template_name, room_id)
        except:
            self.sendErrorMessage(request, self.deletion_error_message)
            return self.redirectTemplate(self.redirect_room_template_name)
        
        self.sendSuccessMessage(request, self.success_message)
        return self.redirectTemplate(self.redirect_chat_template_name, room_id)
        

# Marc John Corral

class DisplayAnalytics(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        object_list = user.cbctestresult_set.all()
        context = {'object_list': object_list}
        return render(request, 'displayAnalytics.html', context)