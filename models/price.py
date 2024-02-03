class Price:
    def __init__(self, inr: float, usd: float, aed: float, eur: float, gbp: float):
        self.inr = inr
        self.usd = usd
        self.aed = aed
        self.eur = eur
        self.gbp = gbp
    
    def to_dict(self):
        return {
            "inr": self.inr,
            "usd": self.usd,
            "aed": self.aed,
            "eur": self.eur,
            "gbp": self.gbp
        }