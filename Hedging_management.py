#PythonZ PD2
#Program do zarządzania ryzykiem rynkowym w przedsiębiorstwie i rekomendacji hedgingu.
#
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
current_Interest_rates_tenors = [0, 0.08, 0.25, 0.5, 1, 2, 5, 10, 30]
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
            #enkapsulacja (ukrywamy przed klientami, ze nasze wyliczenia nie sa rynkowe)
            self._cur_volatility = 0.05 + random.random()*0.05
            self._metal_volatility = 0.2 + random.random()*0.2
    def helloworld(self):
        print(f"Dane dla firmy {self.name} o przychodzie {self.revenue/(10**6):.2f}M PLN")     
        print("\n")
        print(f"Ryzyko rynkowe dla jednostki: ")
        self.VaR = 0
        self.VaR_fx = 0
        self.VaR_metals = 0
        for asset in self.revenue_exposure:
            if self.revenue_exposure[asset] > 0:
                print(f"Wystepuje ekspozycja w {asset} w wysokosci {self.revenue_exposure[asset]*self.revenue:.2f} PLN")
                if asset in current_FX_rates:
                    self.VaR += self.revenue_exposure[asset]*self.revenue * self._cur_volatility
                    self.VaR_fx += self.revenue_exposure[asset]*self.revenue * self._cur_volatility   
                else: 
                    self.VaR += self.revenue_exposure[asset]*self.revenue * self._metal_volatility
                    self.VaR_metals += self.revenue_exposure[asset]*self.revenue * self._cur_volatility
        print(f"Wstępne założenia wskazują na {self.VaR/(10**6):.2f}M PLN potencjalnej straty bez zabezpieczenia")
        return (self.VaR_fx, self.VaR_metals)
class Debt:
    def __init__(self, name, amount, tenor, rate, rate_type):
        self.name = name
        self.amount = amount
        self.tenor = tenor
        self.rate = rate
        self.rate_type = rate_type
    def duration_calculated(self):
        if self.rate == 0:
            return self.tenor
        else:
            return self.tenor * 0.9

#dziedziczenie =
class Loan(Debt):
    def __init__(self, name, amount, tenor, rate, rate_type):
        self.name = name
        self.amount = amount
        self.tenor = tenor
        self.rate = rate
        self.rate_type = rate_type

class Bond(Debt):
    def __init__(self, name, amount, maturity, rate, rate_type):
        self.name = name
        self.amount = amount
        self.tenor  = maturity
        self.rate = rate
        self.rate_type = rate_type

def calculate_int_var(amount, rate, rate_type, duration):
    if rate_type == "fixed":
        return 0
    elif rate > 0.12 :
        return 0
    else:
        var = amount * (0.12 - rate) * duration
        #print(f"Zobowiazanie o wartosci {amount/(10**6):.2f}M PLN stanowi zagrozenie w wysokosci {var/(10**3):.2f}K PLN")
        return var 
        #policzyć var dla kredytów
        


#abstrakcja, abstrakcyjne (klasy i metody)
class Zalecenie_transakcji(ABC):
    
    def __init__(self, nazwa_ryzyka, var_kwota):
        self.nazwa_ryzyka = nazwa_ryzyka
        self.var_kwota = var_kwota          # VaR w PLN
        self.rekomendacja_text = None       # wypełni 

    @abstractmethod
    def analiza():
        pass
    
    @abstractmethod
    def rekomendacja():
        pass

    
    def raport(self):
            print(f"\n{'='*50}")
            print(f"  RAPORT: {self.nazwa_ryzyka}")
            print(f"{'='*50}")
            print(f"  Analiza:       {self.analiza()}")
            print(f"  Rekomendacja:  {self.rekomendacja()}")
            print(f"  VaR:           {self.var_kwota/(10**3):.1f}K PLN")
            print(f"{'='*50}")



class Hedge_currency(Zalecenie_transakcji):
    def __init__(self, waluta, var_kwota):
        super().__init__(f"FX: {waluta}", var_kwota)
        self.waluta = waluta

    def analiza(self):
        if self.var_kwota > 500_000:
            return f"WYSOKIE ryzyko walutowe w {self.waluta}"
        return f"Umiarkowane ryzyko walutowe w {self.waluta}"

    def rekomendacja(self):
        if self.var_kwota > 500_000:
            return f"Forward na {self.waluta}/PLN (zablokuj kurs)"
        return f"Opcja PUT na {self.waluta}/PLN (ochrona z upside)"


class Hedge_commodity(Zalecenie_transakcji):
    
    def __init__(self, metal, var_kwota):
        super().__init__(f"Commodity: {metal}", var_kwota)
        self.metal = metal

    def analiza(self):
        if self.var_kwota > 300_000:
            return f"WYSOKIE ryzyko cenowe na {self.metal}"
        return f"Umiarkowane ryzyko cenowe na {self.metal}"

    def rekomendacja(self):
        if self.var_kwota > 500_000:
            return f"Futures na {self.metal} (COMEX/LME)"
        return f"Collar na {self.metal} (zero-cost hedge)"


class Hedge_interest(Zalecenie_transakcji):
    
    def __init__(self, instrument_name, var_kwota, rate_type):
            super().__init__(f"IR: {instrument_name}", var_kwota)
            self.rate_type = rate_type

    def analiza(self):
        if self.rate_type == "fixed":
            return "Brak ryzyka stopy — fixed rate"
        return f"Ryzyko stopy procentowej (floating)"

    def rekomendacja(self):
        if self.rate_type == "fixed":
            return "Brak potrzeby hedgingu"
        if self.var_kwota > 500_000:
            return "IRS (Interest Rate Swap) — zamień float na fixed"
        return "Cap na WIBOR — ogranicz max koszt odsetkowy"




print(f"{'='*50}")
print(" Witaj w programie ".center(50))
print(f"{'='*50}")
print("\n")

#klasy i obiekty
pozyczka =   Debt("Loan A", 1000000, 3, 0.06, "fixed")
obligacja1 = Bond("Bond A", 1000000, 5, 0.05, "fixed")
obligacja2 = Bond("Bond B", 10000000, 3, 0.04, "floating")
kredyt1 =    Loan("Loan B", 2000000, 5, 0.07, "floating")
kredyt2 =    Loan("Loan C", 15000000, 2, 0.055, "fixed")

dlugi = [pozyczka, obligacja1, obligacja2, kredyt1, kredyt2]

interest_VaR = 0
total_Var = 0

firma1 = company_data("Polskie_Srebro",2.5 * 10 ** 7,1.5 * 10 ** 7, {
"USD": 1,
"EUR": 0,
"GBP": 0,
"XAG": 0.3, 
"XAU": 0.01,
"XCU": 0.1} )
market_VAR = firma1.helloworld()

print("\n")

for d in dlugi:
    # polimorfirzm 
    duration = d.duration_calculated()
    interest_VaR += calculate_int_var(d.amount, d.rate, d.rate_type, duration)


print(f"Wstępne założenia wskazują na {interest_VaR/(10**6):.2f}M PLN potencjalnej straty na stopach procentowych bez zabezpieczenia")


hedges = []

market_VAR = market_VAR + (interest_VaR,)

if market_VAR[0] > 0:
    hedges.append(Hedge_currency("USD", market_VAR[0]))

if market_VAR[1] > 0:
    hedges.append(Hedge_commodity("XAG", market_VAR[1]))

if market_VAR[2] > 0:
    for d in dlugi:
        var_ir = calculate_int_var(d.amount, d.rate, d.rate_type, d.duration_calculated())
        if var_ir > 0:
            hedges.append(Hedge_interest(d.name, var_ir, d.rate_type))

#polimorfizm znowu 
for h in hedges:
    h.raport()  



