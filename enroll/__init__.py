from flask import Flask, request, jsonify
from flask_cors import CORS

from args import _define_args
from enroll.dao import enroll_candidates
from flasgger import Swagger
from keeping.dao import is_valid_email
from constant.db import AUTH_ENGINE

# Swagger config
swagger_config = { 
    "headers": [], 
    "specs": [{
               "endpoint": "", 
               "route": "/swagger.yml",
               "model_filter": lambda tag: True
             }], 
    "swagger_ui": True,
    "static_url_path": "/flasgger_static",
    "specs_route": "/api",
    "openapi": "3.0.0"
}

app = Flask(__name__)
CORS(app)

swagger = Swagger(app, config=swagger_config)

ARGS = _define_args()

@app.route("/api/enrol", methods=["POST"])
def enrol():
    """
    Enroll candidates.

    ---
    tags:
      - Enroll APIs
    parameters:
      - name: content-type
        in: header
        required: false
        style: simple
        explode: false
        schema:
          type: string
        example: application/json
    requestBody:
     content:
      application/json:
        schema:
          type: object
          properties:
            linkedin_profile:
              type: string
            name:
              type: string
            phone_number:
              type: string
            education:
              type: Array
              items:
                type: object
                properties:
                  institute:
                    type: string
                  degree:
                    type: integer
                  batch:
                    type: integer
            email:
              type: string
            work_env:
                type: object
                properties:
                  preferred_time:
                    type: Array
                    items:
                        type: integer
                  preferred_env:
                    type: integer

        examples:
          '0':
            value: |-
              {
                "name"              : "candidate",
                "email"             : "swagger@mail.com",
                "phone_number"      : "98768990",
                "linkedin_profile"  : "https://www.linkedin.com/in/abhishek-bachchan/",
                "education": [{
                                "institute": "x",
                                "degree": 2,
                                "batch": 2012
                            }],
                "work_environment": {
                                     "preferred_env": 1,
                                     "preferred_time": [1, 2]
                                    }
              }
    responses:
        "200":
            "description": Auto generated using Swagger Inspector
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            RESULT:
                                type: string
                            data:
                                type: object
                                properties:
                                    id:
                                        type: integer
                    example:
                        {'RESULT': 'SUCCESS'}
    """
    params = request.get_json()

    name = params.get("name", "")
    linkedin_profile = params.get("linkedin_url", "")

    # In future
    '''
    zip_code = params.get("zip_code", "")
    country = params.get("country", "")
    city = params.get("city")
    state = params.get("state", "")
    dob = params.get("dob", "")
    certifications = params.get("certifications", [])
    '''

    education = params.get("education", [])

    phone_number = params.get("phone")
    emails = params.get("email")

    if not is_valid_email(emails):
        return (jsonify({"message": "Please enter a valid email."})), 400

    if (not name) or (not emails) or (not phone_number) or not (linkedin_profile):
        return (jsonify({"message": "Please fill in all required inputs first."})), 400

    work_environment = params.get("work_env", {})

    res = enroll_candidates(name, education, phone_number, emails, work_environment, linkedin_profile)

    if not res["result"]:
        return (jsonify(res)), 400

    return jsonify({"message": "Thanks {} for enroling with us, we shall approach you soon.".format(name)})

@app.route("/api/preferred-env/list")
def get_preferred_env(*args, **kwargs):
    """ 
    ---
    tags:
      - Reference APIs
    responses:
      "200":
        description: Auto generated using Swagger Inspector
        content:
            application/json:
                schema:
                        type: array
                        items:
                            type: object
                            properties:
                                value:
                                    type: integer
                                label:
                                    type: string
    """
    q = """ 
        SELECT * FROM
        keeping.preferred_mode_enum
        """

    data = []
    with AUTH_ENGINE.connect() as conn:
        res = conn.execute(q)

        for r in res:
            data.append({
                         "value": r.id,
                         "label": r.name
                        })  

    return jsonify({"data": data})

@app.route("/api/preferred-time/list")
def get_preferred_time(*args, **kwargs):
    """ 
    ---
    tags:
      - Reference APIs
    responses:
      "200":
        description: Auto generated using Swagger Inspector
        content:
            application/json:
                schema:
                        type: array
                        items:
                            type: object
                            properties:
                                value:
                                    type: integer
                                label:
                                    type: string
    """
    q = """ 
        SELECT * FROM
        keeping.preferred_time_enum
        """

    data = []
    with AUTH_ENGINE.connect() as conn:
        res = conn.execute(q)

        for r in res:
            data.append({
                         "value": r.id,
                         "label": r.name
                        })

    return jsonify({"data": data})

@app.route("/api/degree/list")
def get_degree_list(*args, **kwargs):
    """ 
    ---
    tags:
      - Reference APIs
    responses:
      "200":
        description: Auto generated using Swagger Inspector
        content:
            application/json:
                schema:
                        type: array
                        items:
                            type: object
                            properties:
                                value:
                                    type: integer
                                label:
                                    type: string
    """
    q = """ 
        SELECT * FROM
        keeping.degree_enum
        """

    data = []
    with AUTH_ENGINE.connect() as conn:
        res = conn.execute(q)

        for r in res:
            data.append({
                         "value": r.id,
                         "label": r.name
                        })

    return jsonify({"data": data})

if __name__=="__main__":
    app.run(debug=True, host=ARGS.ip, port=ARGS.port)
