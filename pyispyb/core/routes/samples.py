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
import io
import os
from flask import request, send_file, current_app, abort
from pyispyb.flask_restx_patched import Resource, HTTPStatus


from pyispyb.app.utils import download_pdb_file
from pyispyb.app.extensions.api import api_v1, Namespace
from pyispyb.app.extensions.auth.decorators import token_required, role_required


from pyispyb.core.schemas import sample as sample_schemas
from pyispyb.core.schemas import crystal as crystal_schemas
from pyispyb.core.schemas import protein as protein_schemas
from pyispyb.core.schemas import diffraction_plan as diffraction_plan_schemas
from pyispyb.core.modules import sample, crystal, diffraction_plan, protein


__license__ = "LGPLv3+"


api = Namespace(
    "Samples", description="Sample related namespace", path="/samples")
api_v1.add_namespace(api)


@api.route("", endpoint="samples")
@api.doc(security="apikey")
class Sample(Resource):
    """Sample resource"""

    @token_required
    @role_required
    def get(self):
        """Returns all sample items"""
        # TODO implement authorization
        return sample.get_samples_by_request(request)

    @token_required
    @role_required
    @api.expect(sample_schemas.f_schema)
    @api.marshal_with(sample_schemas.f_schema, code=201)
    def post(self):
        """Adds a new sample item"""
        # TODO implement authorization
        return sample.add_sample(api.payload)


@api.route("/<int:sample_id>", endpoint="sample_by_id")
@api.param("sample_id", "Sample id (integer)")
@api.doc(security="apikey")
@api.response(code=HTTPStatus.NOT_FOUND, description="Sample not found.")
class SampleById(Resource):
    """Allows to get/set/delete a sample item"""

    @token_required
    @role_required
    @api.doc(description="sample_id should be an integer ")
    @api.marshal_with(sample_schemas.f_schema, skip_none=False, code=HTTPStatus.OK)
    def get(self, sample_id):
        """Returns a sample by sampleId"""
        # TODO implement authorization
        return sample.get_sample_by_id(sample_id)

    @token_required
    @role_required
    @api.expect(sample_schemas.f_schema)
    @api.marshal_with(sample_schemas.f_schema, code=HTTPStatus.CREATED)
    def put(self, sample_id):
        """Fully updates sample with sample_id"""
        # TODO implement authorization
        return sample.update_sample(sample_id, api.payload)

    @token_required
    @role_required
    @api.expect(sample_schemas.f_schema)
    @api.marshal_with(sample_schemas.f_schema, code=HTTPStatus.CREATED)
    def patch(self, sample_id):
        """Partially updates sample with id sampleId"""
        # TODO implement authorization
        return sample.patch_sample(sample_id, api.payload)

    @token_required
    @role_required
    def delete(self, sample_id):
        """Deletes a sample by sampleId"""
        # TODO implement authorization
        return sample.delete_sample(sample_id)


@api.route("/crystals", endpoint="crystals")
@api.doc(security="apikey")
class Crystals(Resource):
    """Crystal resource"""

    @token_required
    @role_required
    def get(self):
        """Returns all crystal items"""
        # TODO implement authorization
        query_dict = request.args.to_dict()
        return crystal.get_crystals_by_query(query_dict)

    @token_required
    @role_required
    @api.expect(crystal_schemas.f_schema)
    @api.marshal_with(crystal_schemas.f_schema, code=201)
    def post(self):
        """Adds a new crystal item"""
        # TODO implement authorization
        return crystal.add_crystal(api.payload)


@api.route("/crystals/<int:crystal_id>", endpoint="crystal_by_id")
@api.param("crystal_id", "Crystal id (integer)")
@api.doc(security="apikey")
@api.response(code=HTTPStatus.NOT_FOUND, description="Crystal not found.")
class CrystalById(Resource):
    """Allows to get/set/delete a crystal item"""

    @token_required
    @role_required
    @api.doc(description="crystal_id should be an integer ")
    @api.marshal_with(crystal_schemas.f_schema, skip_none=False, code=HTTPStatus.OK)
    def get(self, crystal_id):
        """Returns a crystal by crystalId"""
        # TODO implement authorization
        return crystal.get_crystal_by_id(crystal_id)

    @token_required
    @role_required
    @api.expect(crystal_schemas.f_schema)
    @api.marshal_with(crystal_schemas.f_schema, code=HTTPStatus.CREATED)
    def put(self, crystal_id):
        """Fully updates crystal with crystal_id"""
        # TODO implement authorization
        return crystal.update_crystal(crystal_id, api.payload)

    @token_required
    @role_required
    @api.expect(crystal_schemas.f_schema)
    @api.marshal_with(crystal_schemas.f_schema, code=HTTPStatus.CREATED)
    def patch(self, crystal_id):
        """Partially updates crystal with id crystalId"""
        # TODO implement authorization
        return crystal.patch_crystal(crystal_id, api.payload)

    @token_required
    @role_required
    def delete(self, crystal_id):
        """Deletes a crystal by crystalId"""
        # TODO implement authorization
        return crystal.delete_crystal(crystal_id)


@api.route("/crystals/<int:crystal_id>/pdb", endpoint="crystal_pdb_by_id")
@api.param("crystal_id", "Crystal id (integer)")
@api.doc(security="apikey")
@api.response(code=HTTPStatus.NOT_FOUND, description="Crystal not found.")
class CrystalPdbById(Resource):
    """Allows to get/set/delete crystal pdb item"""

    # @token_required
    # @role_required
    @api.doc(description="crystal_id should be an integer ")
    def get(self, crystal_id):
        """Returns pdb file by crystalId"""
        # TODO implement authorization
        query_dict = request.args.to_dict()

        pdb_file_path, pdb_file_name = crystal.get_crystal_pdb_by_id(
            crystal_id)
        if pdb_file_path and pdb_file_name:
            if os.path.exists(
                os.path.join(
                    pdb_file_path,
                    pdb_file_name
                )
            ):
                return send_file(
                    os.path.join(
                        pdb_file_path,
                        pdb_file_name
                    ),
                    as_attachment=True)
        if pdb_file_name:
            query_dict["pdbFileName"] = pdb_file_path

        # If no pdb file in the data base exists, then try to get one from pdb
        if "pdbFileName" in query_dict:
            if not query_dict["pdbFileName"].endswith(".pdb"):
                query_dict["pdbFileName"] += ".pdb"
            pdb_file = download_pdb_file(query_dict["pdbFileName"])
            if pdb_file:
                return send_file(
                    io.BytesIO(pdb_file),
                    mimetype="text/plain",
                    as_attachment=True,
                    attachment_filename=query_dict["pdbFileName"],
                )
            else:
                abort(
                    HTTPStatus.NOT_FOUND,
                    "Pdb entry %s not found in %s"
                    % (
                        query_dict["pdbFileName"],
                        current_app.config["PDB_URI"],
                    ),
                )

        else:
            abort(
                HTTPStatus.NOT_FOUND,
                "No pdb file or entry associated with crystal %d" % crystal_id,
            )

    @token_required
    @role_required
    def patch(self, crystal_id):
        """Fully updates crystal with crystal_id"""
        # TODO implement authorization
        query_dict = request.args.to_dict()

        if "file" not in request.files:
            # No file submitted. Check if the pdb entry name exists
            return crystal.patch_crystal_pdb_by_id(crystal_id, query_dict)
        else:
            request_file = request.files["file"]
            if request_file.filename.endswith(".pdb"):
                if "pdbFileName" not in query_dict:
                    query_dict["pdbFileName"] = request_file.filename
                query_dict["pdbFilePath"] = current_app.config["UPLOAD_FOLDER"]
                request_file.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"], request_file.filename
                    )
                )
                return crystal.patch_crystal_pdb_by_id(crystal_id, query_dict)
            else:
                return abort(
                    HTTPStatus.FORBIDDEN, "Pdb file should end with extension .pdb"
                )
        # return crystal.update_crystal_pdb(crystal_id, api.payload)

    @token_required
    @role_required
    def delete(self, crystal_id):
        """Deletes a crystal pdb file by crystalId"""
        # TODO implement authorization
        # return crystal.delete_crystal_pdb(crystal_id)


@api.route("/proteins", endpoint="proteins")
@api.doc(security="apikey")
class Proteins(Resource):
    """Proteins resource"""

    @token_required
    @role_required
    def get(self):
        """Returns all protein items"""
        # TODO implement authorization
        return protein.get_proteins_by_request(request)

    @token_required
    @role_required
    @api.expect(protein_schemas.f_schema)
    @api.marshal_with(protein_schemas.f_schema, code=201)
    def post(self):
        """Adds a new protein item"""
        # TODO implement authorization
        return protein.add_protein(api.payload)


@api.route("/proteins/<int:protein_id>", endpoint="protein_by_id")
@api.param("protein_id", "protein id (integer)")
@api.doc(security="apikey")
@api.response(code=HTTPStatus.NOT_FOUND, description="protein not found.")
class ProteinById(Resource):
    """Allows to get/set/delete a protein"""

    @token_required
    @role_required
    @api.doc(description="protein_id should be an integer ")
    @api.marshal_with(protein_schemas.f_schema, skip_none=False, code=HTTPStatus.OK)
    def get(self, protein_id):
        """Returns a protein by proteinId"""
        # TODO implement authorization
        return protein.get_protein_by_id(protein_id)

    @token_required
    @role_required
    @api.expect(protein_schemas.f_schema)
    @api.marshal_with(protein_schemas.f_schema, code=HTTPStatus.CREATED)
    def put(self, protein_id):
        """Fully updates protein with proteinId"""
        # TODO implement authorization
        return protein.update_protein(protein_id, api.payload)

    @token_required
    @role_required
    @api.expect(protein_schemas.f_schema)
    @api.marshal_with(protein_schemas.f_schema, code=HTTPStatus.CREATED)
    def patch(self, protein_id):
        """Partially updates protein with proteinId"""
        # TODO implement authorization
        return protein.patch_protein(protein_id, api.payload)

    @token_required
    @role_required
    def delete(self, protein_id):
        """Deletes a protein by proteinId"""
        # TODO implement authorization
        return protein.delete_protein(protein_id)


@api.route("/diffraction_plans", endpoint="diffraction_plans")
@api.doc(security="apikey")
class DiffractionPlans(Resource):
    """Allows to get all diffraction_plans and insert a new one"""

    @token_required
    @role_required
    def get(self):
        """Returns list of diffraction_plans"""
        # TODO implement authorization
        return diffraction_plan.get_diffraction_plans(request)

    @token_required
    @role_required
    @api.expect(diffraction_plan_schemas.f_schema)
    @api.marshal_with(diffraction_plan_schemas.f_schema, code=201)
    def post(self):
        """Adds a new diffraction_plan"""
        # TODO implement authorization
        return diffraction_plan.add_diffraction_plan(api.payload)


@api.route(
    "/diffraction_plans/<int:diffraction_plan_id>", endpoint="diffraction_plan_by_id"
)
@api.param("diffraction_plan_id", "diffraction_plan id (integer)")
@api.doc(security="apikey")
@api.response(code=HTTPStatus.NOT_FOUND, description="diffraction_plan not found.")
class DiffractionPlanById(Resource):
    """Allows to get/set/delete a diffraction_plan"""

    @token_required
    @role_required
    @api.doc(description="diffraction_plan_id should be an integer ")
    @api.marshal_with(
        diffraction_plan_schemas.f_schema, skip_none=False, code=HTTPStatus.OK
    )
    def get(self, diffraction_plan_id):
        """Returns a diffraction_plan by diffraction_planId"""
        # TODO implement authorization
        return diffraction_plan.get_diffraction_plan_by_id(diffraction_plan_id)

    @token_required
    @role_required
    @api.expect(diffraction_plan_schemas.f_schema)
    @api.marshal_with(diffraction_plan_schemas.f_schema, code=HTTPStatus.CREATED)
    def put(self, diffraction_plan_id):
        """Fully updates diffraction_plan with diffraction_plan_id"""
        # TODO implement authorization
        return diffraction_plan.update_diffraction_plan(
            diffraction_plan_id, api.payload
        )

    @token_required
    @role_required
    @api.expect(diffraction_plan_schemas.f_schema)
    @api.marshal_with(diffraction_plan_schemas.f_schema, code=HTTPStatus.CREATED)
    def patch(self, diffraction_plan_id):
        """Partially updates diffraction_plan with id diffraction_planId"""
        # TODO implement authorization
        return diffraction_plan.patch_diffraction_plan(diffraction_plan_id, api.payload)

    @token_required
    @role_required
    def delete(self, diffraction_plan_id):
        """Deletes a diffraction_plan by diffraction_planId"""
        # TODO implement authorization
        return diffraction_plan.delete_diffraction_plan(diffraction_plan_id)
