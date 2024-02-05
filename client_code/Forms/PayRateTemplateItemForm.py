from AnvilFusion.components.FormBase import FormBase, SubformBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from ..app.models import PayRateRule


class PayRateTemplateItemForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateItemForm')
        kwargs['model'] = 'PayRateTemplateItem'

        self.order_number = NumberInput(name='order_number', label='Order', format='##')
        self.default_pay_rate_title = TextInput(name='default_pay_rate_title', label='Default Title')
        self.pay_rate_rule = LookupInput(name='pay_rate_rule', label='Rule', model='PayRateRule',
                                         on_change=self.pay_rate_rule_selected)
        self.default_pay_category = LookupInput(name='default_pay_category', label='Default Pay Category',
                                                model='PayCategory', on_change=self.pay_category_selected)
        self.default_pay_rate = NumberInput(name='default_pay_rate', label='Default Rate', format='c2')
        self.pay_rate_multiplier = NumberInput(name='pay_rate_multiplier', label='Multiplier', format='p2')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        specific_roles_columns = [
            TextInput(name='name', label='Name'),
            LookupInput(name='employee_role', label='Employee Role', model='EmployeeRole'),
            LookupInput(name='pay_category', label='Pay Category', model='PayCategory'),
            NumberInput(name='pay_rate', label='Pay Rate'),
        ]
        specific_roles_view = {
            'model': 'PayRateTemplateSpecificRole',
            # 'columns': [col.grid_column for col in specific_roles_columns],
            'columns': [
                {'name': 'name', 'label': 'Name'},
                {'name': 'employee_role.name', 'label': 'Employee Role'},
                {'name': 'pay_category.name', 'label': 'Payroll Category'},
                {'name': 'pay_rate', 'label': 'Rate'},
            ],
        }
        self.specific_roles = SubformGrid(
            name='specific_roles', label='Pay Rate Specific Roles', model='PayRateTemplateSpecificRole',
            link_model='PayRateTemplateItem', link_field='pay_rate_template_item',
            add_edit_form='PayRateTemplateSpecificRoleForm', form_container_id=kwargs.get('target'),
            view_config=specific_roles_view,
            # edit_mode='inline',
        )

        self.subform_base = SubformBase(
            name='subform_base', model='PayRateTemplateSpecificRole', fields=specific_roles_columns,
            link_model='PayRateTemplateItem', link_field='pay_rate_template_item',
        )

        sections = [
            {
                'name': '_', 'cols': [
                    [
                        self.pay_rate_rule,
                        self.order_number,
                        self.status,
                    ],
                    [
                        self.default_pay_category,
                        self.default_pay_rate_title,
                        self.default_pay_rate,
                        self.pay_rate_multiplier,
                    ],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.specific_roles],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.subform_base],
                ]
            }
        ]

        super().__init__(sections=sections, subforms=self.subform_base, **kwargs)
        self.fullscreen = True

    def pay_rate_rule_selected(self, args):
        print('pay_rate_rule_selected', self.pay_rate_rule.value, args)
        if self.pay_rate_rule.value is None or args.get('value', None) is None:
            self.default_pay_rate.value = None
            self.pay_rate_multiplier.value = None
        else:
            pay_rate_rule = PayRateRule.get(self.pay_rate_rule.value['uid'])
            self.default_pay_rate.value = pay_rate_rule['pay_rate']
            self.pay_rate_multiplier.value = pay_rate_rule['pay_rate_multiplier']
            self.default_pay_rate_title.value = pay_rate_rule['name']

    def pay_category_selected(self, args):
        print('pay_category_selected', self.default_pay_category.value, args)
        if self.default_pay_category.value is None or args.get('value', None) is None:
            self.default_pay_rate_title.value = None
        else:
            self.default_pay_rate_title.value = self.default_pay_category.value['name']
