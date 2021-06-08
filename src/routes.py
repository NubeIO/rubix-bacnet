from flask import Blueprint
from flask_restful import Api

from src.bacnet_master.resources.device import Device, DeviceList, PointWritePresentValue, \
    DeviceObjectList, BuildPointsList
from src.bacnet_master.resources.network import Network, NetworkList, NetworksIds
from src.bacnet_master.resources.network_whois import Whois, UnknownDeviceObjects, \
    UnknownReadPointPv
from src.bacnet_master.resources.point import Point, PointList, PointBACnetRead, PointBACnetWrite

from src.system.resources.ping import Ping

bp_bacnet_server = Blueprint('bacnet_server', __name__, url_prefix='/api/bacnet')
api_bacnet_server = Api(bp_bacnet_server)

# master
api_bacnet_server.add_resource(Device, '/master/device/<string:uuid>')
api_bacnet_server.add_resource(DeviceList, '/master/devices')
api_bacnet_server.add_resource(Network, '/master/network/<string:uuid>')
api_bacnet_server.add_resource(NetworkList, '/master/networks')
api_bacnet_server.add_resource(NetworksIds, '/master/networks/ids')
api_bacnet_server.add_resource(Point, '/master/point/<string:uuid>')
api_bacnet_server.add_resource(PointList, '/master/points')

# bacnet bac0 api calls
api_bacnet_server.add_resource(Whois, '/master/b/network/whois/<string:net_uuid>')
api_bacnet_server.add_resource(PointBACnetRead, '/master/b/points/read/pv/<string:pnt_uuid>')  # read point pv
api_bacnet_server.add_resource(PointBACnetWrite, '/master/b/points/write/pv/<string:pnt_uuid>/<string:value>/<string:priority>')  # write point pv
api_bacnet_server.add_resource(BuildPointsList, '/master/b/points/point_list/<string:dev_uuid>')  # build points list
api_bacnet_server.add_resource(DeviceObjectList, '/master/b/device/objects/<string:dev_uuid>')


api_bacnet_server.add_resource(UnknownReadPointPv, '/master/b/point/unknown/point_pv/<string:net_uuid>')
api_bacnet_server.add_resource(UnknownDeviceObjects, '/master/b/device/unknown/objects/<string:net_uuid>')


api_bacnet_server.add_resource(PointWritePresentValue,
                               '/master/point/write/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string'
                               ':value>/<string:priority>')

bp_sync = Blueprint('sync_bp_gp', __name__, url_prefix='/api/sync')
api_sync = Api(bp_sync)
# api_sync.add_resource(BPToGPSync, '/bp_to_gp')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
