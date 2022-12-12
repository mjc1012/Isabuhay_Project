from django.urls import path
from .views import *

urlpatterns = [
    path('adminuserlist/delete/<str:id>/', DeleteUser.as_view(), name='DeleteUser'),
    path('adminpaylist/', DisplayPaymentList.as_view(), name='DisplayPaymentList'),
    path('adminmain/', DisplayAdminPage.as_view(), name='DisplayAdminPage'),
    path('adminrev/', DisplayRevenueMonth.as_view(), name='DisplayRevenueMonth'),
    path('adminuserlist/', DisplayAllUsers.as_view(), name='DisplayAllUsers'),
    path('adminmonthlyusers/', DisplayUsersMonthly.as_view(), name='DisplayUsersMonthly'),
    path('', DisplayLandingPage.as_view(), name='DisplayLandingPage'),
    path('analytics/', DisplayAnalytics.as_view(), name='DisplayAnalytics'),
    path('clientSide/', DisplayClientSide.as_view(), name='DisplayClientSide'),
    path('register/', CreateAccountPage.as_view(), name='CreateAccountPage'),
    path('login/', DisplayLoginPage.as_view(), name='DisplayLoginPage'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
    path('reset_password/', PasswordResetPage.as_view(), name='reset_password'),
    path('reset_password_sent/', PasswordResetEmailSentPage.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmPage.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('account/', DisplayAccountPage.as_view(), name='DisplayAccountPage'),
    path('account/update', UpdateAccountPage.as_view(), name='UpdateAccountPage'),
    path('account/update/change_password', UpdatePasswordPage.as_view(), name='UpdatePasswordPage'),
    path('account/update/change_photo', UpdatePhotoPage.as_view(), name='UpdatePhotoPage'),
    path('account/delete', DeleteAccountPage.as_view(), name='DeleteAccountPage'),
    path('cbc-test-result/all', DisplayAllCBCTestResult.as_view(), name='DisplayAllCBCTestResult'),
    path('cbc-test-result/<str:id>/', DisplayCBCTestResult.as_view(), name='DisplayCBCTestResult'),
    path('adding-options/', AddingCBCTestResultOptions.as_view(), name='AddingCBCTestResultOptions'),
    path('payment-method/<str:type>/<str:id>/', PaymentMethod.as_view(), name='PaymentMethod'),
    path('promo-options/<str:type>/', PromoOptions.as_view(), name='PromoOptions'),
    path('upload-image/', UploadCBCTestResultImage.as_view(), name='UploadCBCTestResultImage'),
    path('upload-pdf/', UploadCBCTestResultPDF.as_view(), name='UploadCBCTestResultPDF'),
    path('upload-document/', UploadCBCTestResultDocument.as_view(), name='UploadCBCTestResultDocument'),
    path('capture-image/', CaptureCBCTestResultImage.as_view(), name='CaptureCBCTestResultImage'),
    path('cbc-test-result/create/<str:type>/<str:id>/', CreateCBCTestResult.as_view(), name='CreateCBCTestResult'),
    path('cbc-test-result/update/<str:id>/', UpdateCBCTestResult.as_view(), name='UpdateCBCTestResult'),
    path('cbc-test-result/delete/<str:id>/', DeleteCBCTestResult.as_view(), name='DeleteCBCTestResult'),
    path('image/delete/<str:type>/<str:id>/', DeleteCBCTestResultImage.as_view(), name='DeleteCBCTestResultImage'),
    path('pdf/delete/<str:id>/', DeleteCBCTestResultPDF.as_view(), name='DeleteCBCTestResultPDF'),
    path('docx/delete/<str:id>/', DeleteCBCTestResultDocument.as_view(), name='DeleteCBCTestResultDocument'),
    path('payment-completion/<str:type>/<str:id>/', PaymentCompletion.as_view(), name="PaymentCompletion"),
    path('show-chat-room', ShowChatRoom.as_view(), name='ShowChatRoom'),
    path('enter-chat-room', EnterChatRoom.as_view(), name='EnterChatRoom'),
    path('chat-room/<str:id>', ChatRoom.as_view(), name='ChatRoom'),
    path('send-message', SendMessage.as_view(), name='SendMessage'),
    path('contacts', Contacts.as_view(), name='Contacts'),
    path('unread-messages', UnreadMessages.as_view(), name='UnreadMessages'),
    path('get-messages/<str:id>', GetMessages.as_view(), name='GetMessages'),
    path('delete-message/<str:id>', DeleteMessage.as_view(), name='DeleteMessage'),
]

# class PasswordResetPage(aviews.PasswordResetView):
#     pass

# class PasswordResetEmailSentPage(aviews.PasswordResetDoneView):
#     pass

# class PasswordResetConfirmPage(aviews.PasswordResetConfirmView):
#     pass

# class PasswordResetCompleteView(aviews.PasswordResetCompleteView):
