from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
# from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class UserRoleForm(FormBase):
    def __init__(self, **kwargs):
        print('UserRoleForm')
        kwargs['model'] = 'UserRole'

        # name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
        # type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
        # status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
        # permissions_schema = {
        #     "administrator": Attribute(field_type=types.FieldTypes.BOOLEAN),
        # }
        # permissions = Attribute(field_type=types.FieldTypes.OBJECT, schema=permissions_schema)
        # access_permissions_schema = {
        #     "app_menu": Attribute(field_type=types.FieldTypes.OBJECT),
        #     "special_menus": Attribute(field_type=types.FieldTypes.OBJECT),
        #     "components": Attribute(field_type=types.FieldTypes.OBJECT),
        # }
        # access_permissions = Attribute(field_type=types.FieldTypes.OBJECT)

        self.name = TextInput(name='name', label='Name')
        self.type = DropdownInput(name='type', label='Type',
                                  options=AppEnv.enum_constants['USER_ROLE_TYPES'])
        self.description = MultiLineInput(name='description', label='Description')
        self.permissions = MultiLineInput(name='permissions', label='Permissions', rows=3, is_object=True)
        self.access_permissions = MultiLineInput(name='access_permissions', label='Access Permissions',
                                                 rows=5, is_object=True)

        sections = [
            {
                'name': '_', 'cols': [
                    [self.name, self.type],
                    [self.description],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.permissions],
                    [self.access_permissions],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
