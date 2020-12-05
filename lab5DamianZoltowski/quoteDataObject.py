from dataclasses import dataclass

@dataclass
class QuoteDataObject:
    date: str
    price: float
    interpolation: bool
