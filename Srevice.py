from models import ToDoModel


class ToDoService:
    def __init__(self):
        self.model = ToDoModel()

    def create(self, *params):
        self.model.create(params[0], params[1], params[2])
