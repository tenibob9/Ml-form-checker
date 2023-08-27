from templated_mail.mail import BaseEmailMessage
from os import path
from api.settings import BASE_DIR


class ResetPasswordMail(BaseEmailMessage):
    template_name = path.join(BASE_DIR,  "Ml-form-checker/api/accounts/templates/emails/rest_password_mail_notification.html")
    def get_context_data(self):
        context = super().get_context_data()
        return context
    
class ForgotPasswordMail(BaseEmailMessage):
    template_name = path.join(BASE_DIR,  "Ml-form-checker/api/accounts/templates/emails/forgot_password_mail.html")
    def get_context_data(self):
        context = super().get_context_data()
        return context