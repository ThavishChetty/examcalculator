from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    courses: so.WriteOnlyMapped['Course'] = so.relationship(
        back_populates='student')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Course(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    coursename: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    assessment_number: so.Mapped[int] = so.mapped_column(sa.Integer())
    class_weight: so.Mapped[float] = so.mapped_column(sa.Float())
    exam_weight: so.Mapped[float] = so.mapped_column(sa.Float())



    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)


    student: so.Mapped[User] = so.relationship(back_populates='courses')

    assessments: so.WriteOnlyMapped['Assessment'] = so.relationship(
        back_populates='course')

    def __repr__(self):
        return '<Course {}>'.format(self.coursename)



class Assessment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    assessmentname:  so.Mapped[str] = so.mapped_column(sa.String(140))
    weight: so.Mapped[float] = so.mapped_column(sa.Float())
    mark: so.Mapped[float] = so.mapped_column(sa.Float())

    course_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Course.id), index=True)

    course: so.Mapped[Course] = so.relationship(back_populates='assessments')

    def __repr__(self):
        return '<Assessment {}>'.format(self.assessmentname)