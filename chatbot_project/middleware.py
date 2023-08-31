from django_hosts.middleware import HostsRequestMiddleware, HostsResponseMiddleware


class SyncHostsRequestMiddleware(HostsRequestMiddleware):
    async_capable = False
    sync_capable = True


class SyncHostsResponseMiddleware(HostsResponseMiddleware):
    async_capable = False
    sync_capable = True