class Comparison:
    def __init__(self, title: str, table_data: list[list], summary: str):
        self.title = title
        self.table_data = table_data  # Inner lists represent rows
        self.summary = summary
    
    def to_dict(self):
        return {
            "title": self.title,
            "table_data": self.table_data,
            "summary": self.summary
        }