# encoding: utf-8
#
#  Project: py-ispyb
#  https://github.com/ispyb/py-ispyb
#
#  This file is part of py-ispyb software.
#
#  py-ispyb is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  py-ispyb is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.

"""Allows to run the webserver in dev env."""

import sys

from pyispyb import create_app


__license__ = "LGPLv3+"

if len(sys.argv) > 3:
    config_filename = sys.argv[1]
    run_mode = sys.argv[2]
    port = sys.argv[3]
else:
    config_filename = "ispyb_core_config.yml"
    run_mode = "dev"
    port = 5000

debug = run_mode == "dev"

app = create_app(config_filename, run_mode)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=port, debug=debug)
