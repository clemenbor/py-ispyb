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

from flask import request, current_app
from flask_restx._http import HTTPStatus

from pyispyb.flask_restx_patched import Resource

from pyispyb.app.extensions.api import api_v1, Namespace
from pyispyb.app.extensions.auth.decorators import token_required, role_required

# from pyispyb.core.schemas import phasing_program_run as phasing_program_run_schemas
from pyispyb.core.modules import phasing


api = Namespace(
    "Phasing", description="Phasing related namespace", path="/phasing")
api_v1.add_namespace(api)


@api.route("", endpoint="phasing_results")
@api.doc(security="apikey")
class PhasingResults(Resource):
    """Allows to get all phasing_results"""

    @token_required
    @role_required
    def get(self):
        """Returns phasing_results based on query parameters"""
        # TODO implement authorization

        api.logger.info("Get all phasing_results")
        return phasing.get_phasing_results(request)

    @token_required
    @role_required
    # @api.expect(phasing_result_schemas.f_schema)
    # @api.marshal_with(phasing_result_schemas.f_schema, code=201)
    # @api.errorhandler(FakeException)
    def post(self):
        """Adds a new phasing_result"""
        # TODO implement authorization

        api.logger.info("Inserts a new phasing_result")
        return phasing.add_phasing_results(api.payload)
