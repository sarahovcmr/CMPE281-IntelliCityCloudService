from pymongo import MongoClient

class DBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient('mongodb://adminUser:adminPassword@54.177.184.253:27017/')
        self.db = self.client['smartcity']
        self.camera_collection = self.db['iot']

        #sql connection

    # get
    def get_camera_info(self, camera_id):
        camera_info = self.camera_collection.find_one({'camera_id': camera_id})
        
