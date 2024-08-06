from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
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

        self.name = TextInput(name='name', label='Name (ID)')
        self.description = MultiLineInput(name='description', label='Description')
        self.options = MultiLineInput(name='options', label='Options', rows=5, is_object=True)

        sections = [
            {
                'name': '_', 'cols': [
                    [
                         self.name,
                         self.description,
                    ],
                    [
                         self.options,
                    ],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
