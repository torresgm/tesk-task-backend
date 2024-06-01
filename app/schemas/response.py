from marshmallow import fields, Schema

class ResponseSchema(Schema):
    timestamp = fields.DateTime()
    status = fields.Number()
    message = fields.Str()