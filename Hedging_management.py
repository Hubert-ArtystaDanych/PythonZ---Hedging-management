#PythonZ PD2
#Program do zarządzania ryzykiem rynkowym w przedsiębiorstwie i rekomendacji hedgingu

from abc import ABC, abstractmethod
import random



#globalne parametry w programie

name = "Polskie_Srebro"
revenue = 2.5 * 10 ** 7
all_costs = 1.5 * 10 ** 7
debt = {
}

current_FX_rates = {
"USD": 3.5,
"EUR": 4.5,
"GBP": 5
}

current_metal_rates = {
"XAG": 70, #silver
"XAU": 4000, #gold
"XCU": 5 #copper
}

current_Interest_rates = [0.037, 0.037, 0.038, 0.038, 0.04, 0.044, 0.053, 0.057]
#[0: <1m,1: 1m,2: 3m,3: 6m,4: 1y,5: 2y,6: 5y,7: 10y,8: 10y<]

class company_data:

    DEFAULT_EXPOSURE = {k: 0 for k in {**current_FX_rates, **current_metal_rates}}

    def __init__(self, name, revenue, all_costs, revenue_exposure=None):
            self.name = name
            self.revenue = revenue
            self.all_costs = all_costs
            self.revenue_exposure = revenue_exposure or {
                **self.DEFAULT_FX,
                **self.DEFAULT_METALS
            }
            #enkapsulacja
            self._cur_volatility = 0.05
            self._metal_volatility = 0.2
    def helloworld(self):
        print(f"Dane dla firmy {self.name} o przychodzie {self.revenue/(10**6):.2f}M PLN")
        print(f"Ryzyko rynkowe dla jednostki: ")
        self.VaR = 0
        for asset in self.revenue_exposure:
            if self.revenue_exposure[asset] > 0:
                print(f"Wystepuje ekspozycja w {asset} w wysokosci {self.revenue_exposure[asset]*self.revenue:.2f} PLN")
                if asset in current_FX_rates:
                    self.VaR += self.revenue_exposure[asset]*self.revenue * self._cur_volatility
                else: 
                    self.VaR += self.revenue_exposure[asset]*self.revenue * self._metal_volatility
        print(f"Wstępne założenia wskazują na {self.VaR/(10**6):.2f}M PLN potencjalnej straty bez zabezpieczenia")
class Debt:
    def __init__(self, name, tenor, rate, rate_type):
        pass
    def duration_calculated():
        pass

#dziedziczenie =
class Loan(Debt):
    def __init__(self, name,amount, tenor, rate, rate_type):
        pass

class Bond(Debt):
    def __init__(self, name,amount, maturity, rate, rate_type, type = "coupon"):
        pass

#abstrakcja (klas i metod)
class Zalecenie_transakcji(ABC):
    @abstractmethod
    def analiza():
        pass
    
    @abstractmethod
    def rekomendacja():
        pass


class Hedge_currency(Zalecenie_transakcji):
    pass

class Hedge_commodity(Zalecenie_transakcji):
    pass

class Hedge_interest(Zalecenie_transakcji):
    pass




print(" Witaj w programie ".center(50,"*"))

print("\n")

#klasy i obiekty
firma1 = company_data("Polskie_Srebro",2.5 * 10 ** 7,1.5 * 10 ** 7, {
"USD": 1,
"EUR": 0,
"GBP": 0,
"XAG": 0.3, 
"XAU": 0.01,
"XCU": 0.1} )
firma1.helloworld()

obligacja = Loan()
kredyt = Bond()
dlugi = [obligacja, kredyt]

Interest_VaR = 0

for d in dlugi:
    #polimorfirzm 
    Interest_VaR += d.duration_calculated() * d.amount
