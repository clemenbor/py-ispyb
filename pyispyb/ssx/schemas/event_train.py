"""
Project: py-ispyb.

https://github.com/ispyb/py-ispyb

This file is part of py-ispyb software.

py-ispyb is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-ispyb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.
"""


__license__ = "LGPLv3+"



from marshmallow import Schema, fields as ma_fields
from flask_restx import fields as f_fields
from marshmallow_jsonschema import JSONSchema

from pyispyb.app.extensions.api import api_v1 as api

dict_schema = {
        'eventTrainId': f_fields.Integer(required=True, description=''),
        'name': f_fields.String(required=False, description=''),
        'timeOn': f_fields.Float(required=False, description='sec'),
        'duration': f_fields.Float(required=False, description='sec'),
        'period': f_fields.Float(required=False, description=''),
        'numberOfRepetitions': f_fields.Float(required=False, description=''),
        'nameInEventLog': f_fields.String(required=False, description=''),
        'triggerDevice': f_fields.String(required=False, description=''),
        }

class EventTrainSchema(Schema):
    """Marshmallows schema class representing EventTrain table"""

    eventTrainId = ma_fields.Integer()
    name = ma_fields.String()
    timeOn = ma_fields.Float()
    duration = ma_fields.Float()
    period = ma_fields.Float()
    numberOfRepetitions = ma_fields.Float()
    nameInEventLog = ma_fields.String()
    triggerDevice = ma_fields.String()

f_schema = api.model('EventTrain', dict_schema)
ma_schema = EventTrainSchema()
json_schema = JSONSchema().dump(ma_schema)
