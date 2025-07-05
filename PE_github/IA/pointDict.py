class PointDict:
    def __init__(self):
        self.d = {0: {}, 1: {}}

    def get_groups(self, color, point):
        if not(point in self.d[color]):
            self.d[color][point] = []
        return self.d[color][point]

    def set_groups(self, color, point, groups):
        self.d[color][point] = groups

    def add_group(self, color, point, group):
        if not(group in self.d[color][point]):
            self.d[color][point].append(group)

    def remove_point(self, color, point):
        if point in self.d[color]:
            del self.d[color][point]

    def get_items(self, color):
        return self.d[color].items()