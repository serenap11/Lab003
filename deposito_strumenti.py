import csv

class Strumento:
    def __init__(self, codice, tipo, marca, anno, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno = anno
        self.valore = valore

    def __str__(self):
        return f"{self.codice} {self.tipo} {self.marca} {self.anno} {self.valore}"

class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.id_prestito} {self.data} {self.id_strumento}"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self._responsabile = responsabile
        self._strumento = {}
        self._prestito = {}
        self._counter_strumenti = 0
        self._counter_prestito = 0

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding = "utf-8") as file:
                reader = csv.reader(file)
                for r in reader:
                    if not r or len(r) < 5:
                        continue

                    codice = r[0].strip()
                    tipo = r[1].strip()
                    marca = r[2].strip()
                    anno = int(r[3].strip())
                    valore = float(r[4].strip())

                    strumento = Strumento(codice, tipo, marca, anno, valore)
                    self._strumento[codice] = strumento

                    if codice.startswith("S"):
                        try:
                            num = int(codice[1:])
                            if num > self._counter_strumenti:
                                self._counter_strumenti = num
                        except ValueError:
                            pass
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: Impossibile trovare il file '{file_path}'.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self._counter_strumenti += 1
        codice = f"S{self._counter_strumenti}"

        while codice in self.strumenti:
            self._counter_strumenti += 1
            codice = f"S{self._counter_strumenti}"

        strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[codice] = strumento
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: Lo strumento '{id_strumento}' non esiste nel deposito.")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: Lo strumento '{id_strumento}' risulta già in prestito.")

        self._counter_prestiti += 1
        id_prestito = f"P{self._counter_prestiti}"

        prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = prestito
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Il codice prestito '{id_prestito}' non esiste.")

        del self.prestiti[id_prestito]
