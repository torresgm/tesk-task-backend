from marshmallow import fields, Schema

class ArticleSchema(Schema):
    id = fields.UUID(required=False)
    title = fields.String(required=True)
    content = fields.String(required=True)
    summary = fields.String()
    

class ArticleCreateSchema(Schema):
    title = fields.String(required=True, error_messages={"required": "Title is required."})
    content = fields.String(required=True, error_messages={"required": "Content is required."})
