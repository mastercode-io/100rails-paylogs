from AnvilFusion.datamodel.particles import (
    model_type,
    Attribute,
    Relationship,
    Computed,
)
from AnvilFusion.datamodel import types
# from . import Employee, Job, PayRun


@model_type
class TimesheetType:
    _title = "short_code"

    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)

    configuration_schema = {
        "job_required": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "sick_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "annual_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_breaks": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "unpaid_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "worked_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "other": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_length": Attribute(field_type=types.FieldTypes.NUMBER),
    }
    configuration = Attribute(
        field_type=types.FieldTypes.OBJECT, schema=configuration_schema

    )


# @model_type
# class Timesheet:
#     _title = "employee"
#
#     timesheet_type = Relationship("TimesheetType")
#     employee = Relationship("Employee")
#     payrun = Relationship("PayRun")
#     job = Relationship("Job")
#     date = Attribute(field_type=types.FieldTypes.DATE)
#     start_time = Attribute(field_type=types.FieldTypes.DATETIME)
#     end_time = Attribute(field_type=types.FieldTypes.DATETIME)
#     status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
#     approved_by = Relationship("Employee")
#     notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
#     total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
#
#     @staticmethod
#     def calculate_total_hours(args):
#         if args["start_time"] is None or args["end_time"] is None:
#             return 0
#         return (args["end_time"] - args["start_time"]).total_seconds() / 3600
#     total_hours = Computed(("start_time", "end_time"), "calculate_total_hours")
