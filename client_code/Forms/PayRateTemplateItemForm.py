from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRateTemplateItemForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateItemForm')
        kwargs['model'] = 'PayRateTemplateItem'

        self.order_number = NumberInput(name='order_number', label='Order', format='##')
        self.pay_rate_title = TextInput(name='pay_rate_title', label='Title')
        self.pay_rate_rule = LookupInput(name='pay_rate_rule', label='Rule', model='PayRateRule')
        self.pay_rate = NumberInput(name='pay_rate', label='Rate', format='c2')
        self.pay_rate_multiplier = NumberInput(name='pay_rate_multiplier', label='Multiplier', format='p2')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        pay_rate_template_items_view = {
            'model': 'PayRateTemplateItem',
            'columns': [
                {'name': 'order_number', 'label': 'Order'},
                {'name': 'pay_rate_rule.name', 'label': 'Rule'},
                {'name': 'pay_rate_title', 'label': 'Title'},
                {'name': 'pay_rate', 'label': 'Rate'},
                {'name': 'pay_rate_multiplier', 'label': 'Multiplier'},
                {'name': 'status', 'label': 'Status'},
            ],
        }

        fields = [
            self.order_number,
            self.pay_rate_title,
            self.pay_rate_rule,
            self.pay_rate,
            self.pay_rate_multiplier,
            self.status,
        ]

        super().__init__(fields=fields, **kwargs)
