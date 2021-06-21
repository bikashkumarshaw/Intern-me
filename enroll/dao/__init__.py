from constant.db import AUTH_ENGINE
from sqlalchemy.exc import IntegrityError
from keeping.dao import get_school_id, get_degree_id

def enroll_candidates(name, education, phone_number, emails, work_env, linkedin_profiile):
    if type(emails) != list:
        emails = [emails]

    if type(phone_number) != list:
        phone_number = [phone_number]

    res = candidate_already_exists(email=emails, phone_number=phone_number)
    if res["result"]:
        return {"result": False, "message": "A Candidate with the same {}  already exists".format(res['conflict_element'])}

    candidate_id = create_candidate(name, linkedin_profiile, work_env)
    patch_candidate_preferred_time(name, work_env.get('preferred_time'))
    patch_candidate_email(candidate_id, emails)
    patch_candidate_phone_number(candidate_id, phone_number)
    patch_candidate_education(candidate_id, education)

    return {"result": True}

def patch_candidate_preferred_time(candidate_id, preferred_time):
    q1 = """
         DELETE FROM intern_me.candidate_preferred_time
         WHERE candidate_id = %s
         """

    q2 = """
         INSERT INTO intern_me.candidate_preferred_time
         (candidate_id, preferred_time_id)
         VALUES (%s, %s)
         """

    with AUTH_ENGINE.connect() as conn:
        conn.execute(q1, [candidate_id])

    with AUTH_ENGINE.connect() as conn:
        for each in preferred_time:
            conn.execute(q2, [candidate_id, each])

def create_candidate(name, linkedin_profiile, work_env):
    q = """
        INSERT INTO intern_me.candidate
        (name, linkedin_profile, preferred_env)
        VALUES (%s, %s, %s)
        """

    with AUTH_ENGINE.connect() as conn:
        res = conn.execute(q, [name, linkedin_profiile, work_env.get('preferred_env')])

        return int(res.lastrowid)

def patch_candidate_email(candidate_id, emails):
    if type(emails) != list:
        emails = [emails]

    with AUTH_ENGINE.connect() as conn:
        for eml in emails:
            if eml is not None and eml.strip():
                eml = eml.strip()
            else:
                continue
            q = """
                INSERT INTO intern_me.candidate_email
                (candidate_id, email)
                VALUES
                (%s, %s)
                """
            try:
                conn.execute(q, [candidate_id, eml])
            except IntegrityError:
                pass

def patch_candidate_phone_number(candidate_id, phone_number):
    if type(phone_number) != list:
        phone_number = [phone_number]

    with AUTH_ENGINE.connect() as conn:
        for phn in phone_number:
            if phn is not None and phn.strip():
                phn = phn.strip()
            else:
                continue

            q = """ 
                INSERT INTO intern_me.candidate_phone_number
                (candidate_id, phone_number)
                VALUES
                (%s, %s)
                """
            try:
                conn.execute(q, [candidate_id, phn])
            except IntegrityError:
                pass

def patch_candidate_education(candidate_id, education):
    if education is None: return
    q = """
        DELETE FROM intern_me.candidate_education
        WHERE candidate_id = %s
        """

    qi = """
         INSERT INTO intern_me.candidate_education
         (candidate_id, school_id, start_month, start_year, end_month, end_year, degree_id, rank)
         VALUES
         """
    clauses = [] 
    values  = [] 
    for idx, rec in enumerate(education):
        rank = idx + 1
        if 'start_date' in rec: 
            from_month = rec['start_date'][0] if rec['start_date'][0] else None
            from_year  = rec['start_date'][1] if rec['start_date'][1] else None 
        else:
            from_month = None
            from_year  = None
        if 'end_date' in rec:
            to_month   = rec['end_date'][0] if rec['end_date'][0] else None
            to_year    = rec['end_date'][1] if rec['end_date'][1] else None
        else:
            to_month   = None
            to_year    = None

        school_id  = get_school_id(rec['institute'])
        if rec['degree']:
            degree_id = get_degree_id(rec['degree'])
        else:
            degree_id = None

        clauses.append("(%s, %s, %s, %s, %s, %s, %s, %s)")
        values.extend([candidate_id, school_id, from_month, from_year, to_month, to_year, degree_id, rank])

    with AUTH_ENGINE.connect() as conn:
        conn.execute(q, [candidate_id])
        if clauses:
            conn.execute(qi + ','.join(clauses), values)

def candidate_already_exists(**kwargs):
    if 'email' in kwargs and kwargs['email']:
        for eml in kwargs['email']:
            if not eml: continue
            if not eml.strip(): continue
            q = """
                SELECT ce.*
                FROM intern_me.candidate_email ce
                WHERE email = %s
                """
            with AUTH_ENGINE.connect() as conn:
                res = conn.execute(q, [eml.strip()])
                for r in res:
                    return {
                            'result' : True,
                            'conflict_element' : 'email',
                            'candidate_id' : r.candidate_id,
                           }

    if 'phone_number' in kwargs and kwargs['phone_number']:
        for phn in kwargs['phone_number']:
            if not phn:
                continue
            if not phn.strip():
                continue
            q = """
                SELECT cpn.*
                FROM intern_me.candidate_phone_number cpn
                WHERE phone_number = %s
                """
            with AUTH_ENGINE.connect() as conn:
                res = conn.execute(q, [phn.strip()])
                for r in res:
                    return {
                            'result' : True,
                            'conflict_element' : 'phone_number',
                            'candidate_id' : r.candidate_id
                           }

    return {
            'result': False
           }
