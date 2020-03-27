# ISPyB Backend prototype

[![Build Status](https://travis-ci.org/mxcube/mxcube.svg?branch=master)](https://travis-ci.org/IvarsKarpics/ispyb_backend_prototype)

```bash
sudo pip install -r requirements.txt
cd ..
gunicorn ispyb:server
```

## Create SQLAlchemy models from the existing db:
```bash
flask-sqlacodegen --flask --outfile models.py mysql://ispyb_api:password_1234@localhost/ispybtest
```

## Format code
```bash
autopep8 -a -r -j 0 -i --max-line-length 88 ./
black --safe ./
```

