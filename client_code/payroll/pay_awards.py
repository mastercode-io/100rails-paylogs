from ..app.models import PayRateRule, Timesheet
import json


class PyaRateRuleAward(PayRateRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pay_lines = []


    def apply_rule(self):
        pass


class PayLine:
    def __init__(self, **kwargs):
        self.pay_rate_title = kwargs.get('pay_rate_title')
        self.pay_category = kwargs.get('pay_category')
        self.date = kwargs.get('date')
        self.pay_rate = kwargs.get('pay_rate')
        self.unit_type = kwargs.get('unit_type')
        self.units = kwargs.get('units')
        self._pay_amount = None


    @property
    def pay_amount(self):
        if self.pay_rate is not None and self.units is not None:
            self._pay_amount = self.pay_rate * self.units
        return self._pay_amount


    def __str__(self):
        return f'{self.pay_amount} - @{self.pay_rate_title} {self.pay_rate} x {self.units} {self.unit_type}'


    def __repr__(self):
        return (f"PayLine("
                f"pay_rate_title='{self.pay_rate_title}', "
                f"pay_category='{self.pay_category}', "
                f"date='{self.date}', "
                f"pay_rate={self.pay_rate}, "
                f"unit_type='{self.unit_type}', "
                f"units={self.units}"
                f")")


    def to_dict(self):
        return {
            'pay_rate_title': self.pay_rate_title,
            'pay_category': self.pay_category,
            'date': self.date,
            'pay_rate': self.pay_rate,
            'unit_type': self.unit_type,
            'units': self.units,
            'pay_amount': self.pay_amount,
        }


    def to_json(self):
        return json.dumps(self.to_dict())


    def split(self, units):
        if units > self.units:
            raise ValueError('units to split is greater than units on pay line')
        self.units -= units
        return PayLine(
            pay_rate_title=self.pay_rate_title,
            pay_category=self.pay_category,
            date=self.date,
            pay_rate=self.pay_rate,
            unit_type=self.unit_type,
            units=units,
        )
