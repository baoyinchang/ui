from manticoresearch import Client, Search
from app.core.config import settings

class ManticoreClient:
    def __init__(self):
        self.client = Client(
            host=settings.MANTICORE_HOST,
            port=settings.MANTICORE_PORT
        )
        if settings.MANTICORE_USER:
            self.client.set_http_auth(
                settings.MANTICORE_USER,
                settings.MANTICORE_PASSWORD
            )

    def search_file_events(self, query: str, limit: int = 100):
        """查询文件事件日志"""
        search = Search(self.client, index='file_events')
        search.query('match', _all=query).limit(limit)
        return search.execute()

    def search_network_flows(self, src_ip: str = None, dest_ip: str = None, limit: int = 100):
        """查询网络流日志"""
        search = Search(self.client, index='network_flows')
        if src_ip:
            search.filter('equals', src_ip=src_ip)
        if dest_ip:
            search.filter('equals', dest_ip=dest_ip)
        search.limit(limit)
        return search.execute()

# 单例实例
manticore_client = ManticoreClient()