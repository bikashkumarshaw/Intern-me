from   sqlalchemy.exc import IntegrityError
from constant.db import AUTH_ENGINE
import re

def is_valid_email(email):
    if not email:
        return False

    email = email.strip()
    exclusion_list = ['hmail.com','gamil.com','gmail.co','gmail.con']
    if not email:
        return False

    if email.startswith('-'):
        return False

    else:
        email = email.lower()
        if re.match(r'^[a-zA-Z0-9._%+\-\']+@[a-zA-Z0-9\-.]+\.[a-zA-Z0-9]+$',email) :
            if email.split('@')[1] in exclusion_list:
                return False
            else:
                return True
        else :
            return False

def get_degree_id(name):
    return get_enum_id(name, 'keeping.degree_enum')

def get_school_id(name):
    return get_enum_id(name, 'keeping.school_enum')

def get_enum_id(name, table_name, create=True):
    if name is None:
        return None

    q = "SELECT * FROM %s WHERE name = %%s" % (table_name, )
    with AUTH_ENGINE.connect() as conn:
        res = conn.execute(q, [name])
        for r in res:
            return int(r.id)

        if not create:
            return

        q = """
            INSERT INTO %s
            (name)
            VALUES
            (%%s)
            """ % (table_name, )
        try:
            res = conn.execute(q, [name])
            return int(res.lastrowid)
        except IntegrityError:
            enum_id = get_enum_id(name, table_name, create=False)
            if not enum_id:
                raise Exception('Unable to find %s in %s even after IntegrityError' % (name, table_name))
            else:
                return enum_id
