from uuid import UUID

def version_uuid(uuid):
    try:
        return UUID(uuid).version
    except ValueError:
        return None