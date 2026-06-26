class MessageBus:
    def __init__(self):
        self.paths = {}

    def publish_path(self, drone_id, path):
        self.paths[drone_id] = path

    def get_path(self, drone_id):
        return self.paths.get(drone_id, [])