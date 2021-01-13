from dataclasses import dataclass

@dataclass
class SalesDataObject:
    date: str
    usdSalesValue: float
    plnSalesValue: float
