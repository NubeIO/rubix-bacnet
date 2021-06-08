import re

from sqlalchemy.orm import validates

from src import db
from src.bacnet_server.interfaces.point.points import PointType, Units, BACnetEventState
from src.bacnet_server.models.model_point_store import BACnetPointStoreModel
from src.bacnet_server.models.model_priority_array import PriorityArrayModel


class BACnetPointModel(db.Model):
    __tablename__ = 'bac_points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    object_type = db.Column(db.Enum(PointType), nullable=False)
    object_name = db.Column(db.String(80), nullable=False, unique=True)
    use_next_available_address = db.Column(db.Boolean(), nullable=False, default=False)
    address = db.Column(db.Integer(), nullable=True, unique=True)
    relinquish_default = db.Column(db.Float(), nullable=False)
    priority_array_write = db.relationship('PriorityArrayModel',
                                           backref='point',
                                           lazy=False,
                                           uselist=False,
                                           cascade="all,delete")
    event_state = db.Column(db.Enum(BACnetEventState), nullable=False)
    units = db.Column(db.Enum(Units), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    data_round = db.Column(db.Integer(), nullable=True)
    data_offset = db.Column(db.Float(), nullable=True)
    point_store = db.relationship('BACnetPointStoreModel',
                                  backref='point',
                                  lazy=False,
                                  uselist=False,
                                  cascade="all,delete")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"BACnetPointModel({self.uuid})"

    @validates('object_name')
    def validate_object_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("object_name should be alphanumeric and can contain '_', '-'")
        return value

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def filter_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_object_id(cls, object_type, address):
        return cls.query.filter(
            (BACnetPointModel.object_type == object_type) & (BACnetPointModel.address == address)).first()

    @classmethod
    def find_by_object_name(cls, object_name):
        return cls.query.filter(BACnetPointModel.object_name == object_name).first()

    @classmethod
    def get_next_available_address(cls, current_address):
        addresses = cls.query.filter().with_entities(BACnetPointModel.address).all()
        sorted_addresses = sorted({address[0] for address in addresses} - {current_address})
        available_address = 1
        for address in sorted_addresses:
            if address == available_address:
                available_address += 1
            else:
                break
        return available_address

    @classmethod
    def delete_all_from_db(cls):
        cls.query.delete()
        db.session.commit()

    def save_to_db(self, priority_array_write: dict):
        self.priority_array_write = PriorityArrayModel(point_uuid=self.uuid, **priority_array_write)
        self.point_store = BACnetPointStoreModel.create_new_point_store_model(self.uuid)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
