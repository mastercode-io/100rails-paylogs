from ..app.models import PayRateRule, PayRateTemplateItem, Timesheet
import json
from datetime import datetime, timedelta


WEEK_DAY_NAME = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def day_type(date):
    day_of_week = date.weekday()
    if day_of_week == 5 or day_of_week == 6:  # Saturday or Sunday
        return "Weekend", WEEK_DAY_NAME[day_of_week]
    else:
        return "Weekday", WEEK_DAY_NAME[day_of_week]



class PyaRateRuleAward(PayRateRule):
    def __init__(self, instance=None):
        self.__dict__.update(instance.__dict__)


    def allocate_time(self, date, start_time, end_time):
        units = 0
        unallocated_time = []
        allocated_start_time = allocated_end_time = start_time
        if self.time_scope in day_type(date):
            if self.unit_type == 'Day' or self.pay_rate_type == 'Fixed Amount':
                units = 1
                unallocated_time.append((start_time, end_time))
            elif self.unit_type == 'Hour':
                if end_time.time() <= self.start_time or start_time.time() >= self.end_time:
                    unallocated_time.append((start_time, end_time))
                elif start_time.time() < self.start_time:
                    unallocated_time.append((start_time, datetime.combine(start_time.date(), self.start_time)))
                    allocated_start_time = datetime.combine(start_time.date(), self.start_time)
                else:
                    allocated_start_time = start_time
                if end_time.time() > self.end_time:
                    unallocated_time.append((datetime.combine(end_time.date(), self.end_time), end_time))
                    allocated_end_time = datetime.combine(end_time.date(), self.end_time)
                else:
                    allocated_end_time = end_time
                units = (allocated_end_time - allocated_start_time).total_seconds() / 3600
                if units > self.max_hours:
                    units = self.max_hours
                    unallocated_time.append((allocated_start_time + timedelta(hours=self.max_hours), allocated_end_time))
        print('allocate_time', units, unallocated_time)
        return units, unallocated_time


class PayItemAward(PayRateTemplateItem):
    def __init__(self, instance=None):
        self.__dict__.update(instance.__dict__)


    def calculate_award(self, date, start_time, end_time, employee_base_rate=None):
        units, unallocated_time = PyaRateRuleAward(self.pay_rate_rule).allocate_time(date, start_time, end_time)
        payline_rate = self.pay_rate or employee_base_rate
        if self.pay_rate_rule.pay_rate_type == 'Multiplier':
            payline_rate *= self.pay_rate_multiplier
        if units:
            pay_line = PayLine(
                pay_rate_title=self.pay_rate_rule.title,
                pay_category=self.pay_category,
                date=date,
                pay_rate=payline_rate,
                unit_type=self.pay_rate_rule.unit_type,
                units=units,
            )
        else:
            pay_line = None
        return pay_line, unallocated_time



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
