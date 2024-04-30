from ninja import Schema
from ninja.orm import create_schema

from shortener.models import Organization
from django.contrib.auth.models import User


OrganizationSchema = create_schema(Organization)
UserSchema = create_schema(User, exclude=['password'])


class Users(Schema):
    id: int
    full_name: str = None
    user: UserSchema = None
    organization: OrganizationSchema = None


class TelegramUpdateSchema(Schema):
    username: str
