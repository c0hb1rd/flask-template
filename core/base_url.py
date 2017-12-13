from config import URL_MAP


class BaseUrl:
    def __init__(self, path, view_obj, view_name, note="no note"):
        self.note = note
        self.path = path
        self.view_obj = view_obj
        self.view_name = view_name

        URL_MAP.append({
            'note': self.note,
            'path': self.path,
            'view': view_obj,
            'view_name': self.view_name
        })
