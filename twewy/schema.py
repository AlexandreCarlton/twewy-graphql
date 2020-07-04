import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from twewy.models import Pin as PinModel, Noise as NoiseModel


class Pin(SQLAlchemyObjectType):
    class Meta:
        model = PinModel
        exclude_fields = ("sdpp_yields_number", "mpp_yields_number", "bpp_yields_number")
        interfaces = (relay.Node,)


class Noise(SQLAlchemyObjectType):
    class Meta:
        model = NoiseModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_pins = SQLAlchemyConnectionField(Pin.connection)
    all_noise = SQLAlchemyConnectionField(Noise.connection)

schema = graphene.Schema(query=Query, types=[Pin])
