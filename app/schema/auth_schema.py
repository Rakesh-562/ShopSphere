from marshmallow import Schema, fields, validate, validates, ValidationError


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters"),
    )
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(load_default=None, validate=validate.Length(max=20))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UpdateProfileSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=100))
    last_name = fields.Str(validate=validate.Length(min=1, max=100))
    phone = fields.Str(validate=validate.Length(max=20))


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters"),
    )
