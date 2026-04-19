from Ecom_App.models import AdminLogin

username = 'vamsi'
password = 'vamsi123'

obj, created = AdminLogin.objects.update_or_create(Username=username, defaults={'Password': password})
if created:
    print('AdminLogin created for', username)
else:
    print('AdminLogin updated for', username)
