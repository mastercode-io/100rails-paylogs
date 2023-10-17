from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
import anvil.users

FORM_ACTION_HEADER = {
    'add': 'Signup',
    'edit': 'Update',
}


class UserForm(FormBase):
    def __init__(self, **kwargs):
        print('UserForm')
        kwargs['model'] = 'User'
        action = kwargs.get('action', 'add')

        self.first_name = TextInput(name='first_name', label='First Name', required=True)
        self.last_name = TextInput(name='last_name', label='Last Name', required=True)
        self.email = TextInput(name='email', label='Login (email)', required=True)
        self.password = TextInput(name='password', label='Password', input_type='password', required=True, save=False)
        self.confirm_pwd = TextInput(name='confirm_password', label='Confirm Password', input_type='password', required=True, save=False)
        self.enabled = CheckboxInput(name='enabled', label='Enabled', value=True)
        self.user_roles = LookupInput(name='user_roles', label='Roles', model='UserRole', multiple=True)
        self.permissions = MultiFieldInput(name='permissions', model='User', label='Permissions')
        self.alert = InlineMessage(name='message')

        buttons = [
            {'buttonModel': {'isPrimary': True, 'content': FORM_ACTION_HEADER[action]}, 'click': self.save_user},
            {'buttonModel': {'isPrimary': True, 'content': 'Cancel'}, 'click': self.form_cancel},
        ]

        fields = [
            self.email,
            self.password,
            self.confirm_pwd,
            self.first_name,
            self.last_name,
            self.enabled,
            self.user_roles,
            self.permissions,
            self.alert,
        ]

        super().__init__(
            header=f"{FORM_ACTION_HEADER[action]} User",
            fields=fields,
            buttons=buttons,
            **kwargs
        )


    def form_open(self, args):
        super().form_open(args)
        print('UserForm.form_show', self.action)
        print('source', self.source)
        source_value = getattr(self.source, 'value', None)
        print('source value', source_value)
        if source_value is not None:
            print('tenant_uid', getattr(source_value, 'tenant_uid'))
        if self.action == 'edit':
            self.password.hide()
            self.confirm_pwd.hide()


    def form_validate(self):
        if self.action == 'add':
            if self.password.value != self.confirm_pwd.value:
                return False
            else:
                return super().form_validate()


    def save_user(self, args):
        self.alert.hide()
        if self.form_validate():
            if not self.data.uid:
                try:
                    user_instance = anvil.users.signup_with_email(self.email.value, self.password.value)
                    print('user_instance', user_instance, dir(user_instance))
                except Exception as e:
                    print('error', e)
                    self.alert.show()
                    self.alert.message = str(e)


    def form_cancel(self, args):
        super().form_cancel(args)
