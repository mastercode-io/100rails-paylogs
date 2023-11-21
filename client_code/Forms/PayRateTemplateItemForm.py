from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayRateTemplateItemForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateItemForm')
        kwargs['model'] = 'PayRateTemplateItem'

        self.order_number = NumberInput(name='order_number', label='Order', format='##')
        self.pay_rate_title = TextInput(name='pay_rate_title', label='Title')
        self.pay_rate_rule = LookupInput(name='pay_rate_rule', label='Rule', model='PayRateRule',
                                         on_change=self.pay_rate_rule_selected)
        self.pay_rate = NumberInput(name='pay_rate', label='Rate', format='c2')
        self.pay_rate_multiplier = NumberInput(name='pay_rate_multiplier', label='Multiplier', format='p2')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        fields = [
            self.pay_rate_rule,
            self.pay_rate_title,
            self.pay_rate,
            self.pay_rate_multiplier,
            self.order_number,
            self.status,
        ]

        super().__init__(fields=fields, **kwargs)


    def pay_rate_rule_selected(self, args):
        print('pay_rate_rule_selected', self.pay_rate_rule.value, args)
        if self.pay_rate_rule.value is None or args.get('value', None) is None:
            self.pay_rate.value = None
            self.pay_rate_multiplier.value = None
        else:
            self.pay_rate.value = self.pay_rate_rule.value['pay_rate']
            self.pay_rate_multiplier.value = self.pay_rate_rule.value['pay_rate_multiplier']
            self.pay_rate_title.value = self.pay_rate_rule.value['name']
