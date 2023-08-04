import yaml
from marshmallow import Schema, fields, validates_schema, ValidationError, RAISE
from marshmallow.validate import Length


class MetaSchema(Schema):
    title = fields.Str(validate=Length(min=1), allow_none=False)
    published = fields.Bool(missing=False, allow_none=False)
    publish_date = fields.Date(allow_none=False)
    tags = fields.List(fields.Str(allow_none=False))

    intro_override = fields.Str(allow_none=True, missing=None)  # optional

    @validates_schema(skip_on_field_errors=True)
    def validate_publish_date(self, data, partial, many):
        if data['published']:
            if 'publish_date' not in data or not data['publish_date']:
                raise ValidationError("Published date must be set when the post is published")

    class Meta:
        unknown = RAISE


_meta_schema_inst = MetaSchema(many=False)


def load_meta_file(filename: str):
    with open(filename, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        parsed_data = _meta_schema_inst.load(data)
        return parsed_data
