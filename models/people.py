class People:
    def __init__(self, name: str, email: str, phone: str, designation: str):
        self.name = name
        self.email = email
        self.phone = phone
        self.designation = designation
    

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "designation": self.designation
        }
