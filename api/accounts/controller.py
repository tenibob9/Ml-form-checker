from datetime import date
from api.settings import DEFAULT_FROM_MAIL
from .mail import ResetPasswordMail, ForgotPasswordMail

logo=""
class UserController():
    def send_reset_password_mail(user):
        DEFAULT_TO_EMAIL = user.email
        current_year = date.today().year

        mail = ResetPasswordMail(
          
            context={
                "email": user.email,
                "name": user.full_name,
                "logo_url": logo,
                "year": current_year,
            }
        )
        to_emails = [DEFAULT_TO_EMAIL]
       
        mail.send(to_emails, from_email=DEFAULT_FROM_MAIL)

    def send_forgot_password_mail(user, new_password):
        DEFAULT_TO_EMAIL = user.email
        current_year = date.today().year

        mail = ForgotPasswordMail(
        
            context={
                "password": new_password,
                "name": user.full_name,
                "logo_url": logo,
                "year": current_year,
            }
        )
        to_emails = [DEFAULT_TO_EMAIL]
    
        mail.send(to_emails, from_email=DEFAULT_FROM_MAIL)