from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=False)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class ReferenceRangeSchema(Schema):
    test_name = fields.Str(required=True)
    min_value = fields.Float(required=True)
    max_value = fields.Float(required=True)
    units = fields.Str(required=True)
    department_id = fields.Int(required=True)
    source_id = fields.Int(required=False, allow_none=True)
    study_id = fields.Int(required=False, allow_none=True)
