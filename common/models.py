from axf_api.extension import db


class BaseModelNoPrimaryKey(db.Model):
    __abstract__ = True

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True

class BaseModel(BaseModelNoPrimaryKey):
    __abstract__ = True

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)