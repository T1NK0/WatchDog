from pysnmp import hlapi
import sharedTools


# Our get method, where only 3 variables is required (Target, Oids, Credentials)
def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    # Defines our handler.
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        # This star does, so it's able to be a single "string" or a list of "oids"
        *sharedTools.construct_object_types(oids)
    )
    return sharedTools.fetch(handler, 1)[0]