class Entry:
   
    def __init__(self, name, price, unit, measurement):
        self.name = name
        self.price = float(price)
        self.unit = float(unit) if unit else None
        self.measurement = measurement
        
    
    def unitPrice(self):
        if self.measurement and self.unit:
            try: 
                return round(self.price / self.unit, 2)
            except ZeroDivisionError:
                return None
        return None

    def formatMeasurement(self):
        if not self.measurement:
            return ""
        
        m = self.measurement.strip().lower()

        perUnits = {
            "lb", "oz", "fl oz", "gal", "pound", "pt", "qt", #imp
            "ct", "pc", "pk",                                #specific
            "ml", "l"                                        #metric
            }
        
        suffixConvert = {
            "ea": " each",
            "count": " each",
            "ct": " each",
            "pk": " pack",
            "lb": " lb",
            "pound": " lb",
            "quart": "qt",
            "gallon": "gal",
            "pc": "piece",
            "gram": "g",
            "eighth": "⅛",
            "quarter": "¼"
        }
        
        if m in perUnits:
            return (f" per {m}")
        if m in suffixConvert:
            return suffixConvert[m]
        if "/" in m:
            return (f"({self.measurement.strip()})")
        
        return (f" {m}")
    
    def display(self):
        pricePer = self.unitPrice()
        if pricePer:
            return (f"{self.name} (${pricePer:.2f}) per {self.formatMeasurement}")
        else:
            return (f"{self.name}: {self.price}")
    
    def __str__(self):
        return self.display()
    
class Link:
    def __init__(self, url, store):
        self.url = url
        self.store = store
    
    def display(self):
        return (f"{self.store}: {self.url}")
    
    def __str__(self):
        return self.display()