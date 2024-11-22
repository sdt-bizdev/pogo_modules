from .BaseProducer import BaseProducer

class SonyCollectionStatsProducer(BaseProducer):
        
    def format_date(self, date_str):
        return date_str.replace('_', '-')

    def format_message(self, data_obj):
        
        obj = {
            "server_id": data_obj.get("server_id"),  
            "server_instance": data_obj.get("server_instance"), 
            "data": {
                "project_name": data_obj.get("project_name"),  
                "scraping_type": data_obj.get("scraping_type"),  
                "feature_name": data_obj.get("feature_name"),  
                "date": self.format_date(data_obj.get("date")),  
                "count": data_obj.get("count", 0),  # Default count
                "file_creation_status": data_obj.get("file_creation_status", "0"),  # Default status
                "file_send_status": {
                    "HTTP_Status": data_obj.get("http_status", None),
                    "Error": data_obj.get("error", None),
                    "Message": data_obj.get("message", None)
                }
            }
        }
        
        return obj

if __name__ == "__main__":

    BOOTSTRAP_SERVERS = ""
    s_prod = SonyCollectionStatsProducer(BOOTSTRAP_SERVERS)
    s_prod.send_message(topic = 'legacy_sonyCollectionStats', data_sources = {'server_id': 2, 'project_name': 'nicovideo', 'feature_name': 'user', 'scraping_type': 'initial', 'date': '2024_02_11', 'count': -1})
