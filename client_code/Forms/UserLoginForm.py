from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
import anvil.users


class UserLoginForm(FormBase):
    def __init__(self, **kwargs):
        print('UserLoginForm')
        kwargs['model'] = 'User'

        self.login = TextInput(name='login', label='User Login (email)', input_type='email', save=False)
        self.password = TextInput(name='password', label='Password', input_type='password', save=False)
        self.message = InlineMessage(name='message', label='Message', type='info')

        fields = [self.login, self.password, self.message]

        validation = {
            'rules': {
                self.login.el_id: {'required': True},
                self.password.el_id: {'required': True},
            }
        }

        super().__init__(fields=fields, validation=validation, button_save_label='Login', **kwargs)


    def form_save(self, args):
        print('Logging user...', args)
        try:
            user = anvil.users.login_with_email(self.login.value, self.password.value)
            print('Logged in user', user)
            self.form_cancel(args)
        except Exception as e:
            print('Login error', e)
            self.message.message = f'Invalid login details: {e}'
            self.message.type = 'e-error'
            return
