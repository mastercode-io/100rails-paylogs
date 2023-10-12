from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput

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
        self.enabled = CheckboxInput(name='enabled', label='Enabled')
        self.user_roles = LookupInput(name='user_roles', label='Roles', model='UserRole', multiple=True)
        self.permissions = MultiFieldInput(name='permissions', model='User', label='Permissions')

        buttons = [
            {'buttonModel': {'isPrimary': True, 'content': FORM_ACTION_HEADER[action]}, 'click': self.save_user},
            {'buttonModel': {'isPrimary': True, 'content': 'Cancel'}, 'click': self.form_cancel},
        ]

        fields = [
            self.email,
            self.password,
            self.first_name,
            self.last_name,
            self.enabled,
            self.user_roles,
            self.permissions,
        ]

        super().__init__(
            header=f"{FORM_ACTION_HEADER[action]} User",
            fields=fields,
            buttons=buttons,
            **kwargs
        )


    def save_user(self, args):
        pass


    def form_cancel(self, args):
        super().form_cancel(args)
