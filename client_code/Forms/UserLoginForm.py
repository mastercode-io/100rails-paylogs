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
        self.remember = CheckboxInput(name='remember', label='Remember Me', value=True, save=False)
        self.error = InlineMessage(name='message', label='', type='')

        fields = [self.login, self.password, self.remember, self.error]

        validation = {
            'rules': {
                self.login.el_id: {'required': True},
                self.password.el_id: {'required': True},
            }
        }

        buttons = [
            {'buttonModel': {'isPrimary': True, 'content': 'LOGIN'}, 'click': self.login_user},
            {'buttonModel': {'content': 'Forgot Password'}, 'click': self.forgot_password},
        ]

        super().__init__(
            fields=fields,
            validation=validation,
            header='Sign In',
            modal=True,
            buttons=buttons,
            **kwargs
        )
        self.form.showCloseIcon = False


    def login_user(self, args):
        print('Logging user...', args)
        try:
            user = anvil.users.login_with_email(self.login.value, self.password.value, remember=self.remember.value)
            print('Logged in user', user)
            AppEnv.logged_user = init_user_session()
            self.form_cancel(args)
        except Exception as e:
            print('Login error', e)
            self.error.message = f'Invalid login details: {e}'
            self.error.type = 'e-error'
            return


    def forgot_password(self, args):
        print('Forgot password', args)
        anvil.users.send_password_reset_email(self.login.value)
        self.error.message = f'Password reset email sent to {self.login.value}'
        self.error.type = 'e-info'
        return
