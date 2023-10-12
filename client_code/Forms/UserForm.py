from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class UserForm(FormBase):
    def __init__(self, **kwargs):
        print('UserForm')
        kwargs['model'] = 'User'

        self.first_name = TextInput(name='first_name', label='First Name', required=True)
        self.last_name = TextInput(name='last_name', label='Last Name', required=True)
        self.email = TextInput(name='email', label='Email', required=True)
        self.enabled = CheckboxInput(name='enabled', label='Enabled')
        self.user_roles = LookupInput(name='user_roles', label='Roles', model='UserRole', multiple=True)
        self.permissions = MultiFieldInput(name='permissions', model='User', label='Permissions')

        fields = [
            self.first_name,
            self.last_name,
            self.email,
            self.enabled,
            self.user_roles,
            self.permissions,
        ]

        super().__init__(fields=fields, **kwargs)
        # self.fullscreen = True
