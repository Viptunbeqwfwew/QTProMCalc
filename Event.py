class Event:
    method: list = list()

    def invoke(self, *args, **kwargs):
        for i in self.method:
            i(args, kwargs)

    def __iadd__(self, method):
        self.method.append(method)

    def __isub__(self, method):
        self.method.remove(method)
