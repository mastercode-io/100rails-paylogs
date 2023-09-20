from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv, init_user_session
import anvil.users


class UserLoginForm(FormBase):
    def __init__(self, **kwargs):
        print('UserLoginForm')
        kwargs['model'] = 'User'
        # anvil.users.signup_with_email('alex@100email.co', '!X!SnRGgr8Gzk56')

        self.login = TextInput(name='login', label='User Login (email)', input_type='email', save=False)
        self.password = TextInput(name='password', label='Password', input_type='password', save=False)
        self.error = InlineMessage(name='message', label='', type='')

        fields = [self.login, self.password, self.error]

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
            AppEnv.logged_user = init_user_session()
            self.form_cancel(args)
        except Exception as e:
            print('Login error', e)
            self.error.message = f'Invalid login details: {e}'
            self.error.type = 'e-error'
            return
