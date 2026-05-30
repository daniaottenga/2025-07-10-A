import datetime
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._categoria = None
        self._partenza = None
        self._arrivo = None

    def fillDDCategory(self):
        categorie = self._model.getAllCategories()
        for c in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(
                key=c.category_id, #oppure data=x, key=category_name
                text=c.category_name,
                on_click=self.choiceDD
            ))


    def handleCreaGrafo(self, e):
        self._view.txt_result.clean()

        if self._view._ddcategory.value is None:
            self._view.create_alert("Errore, seleziona una categoria")
            self._view.update()
            return

        if self._view._dp1.value is None:
            self._view.create_alert("Errore, seleziona un giorno di inizio")
            self._view.update()
            return

        if self._view._dp2.value is None:
            self._view.create_alert("Errore, seleziona un giorno di fine")
            self._view.update()
            return

        nodi = self._model.creaGrafo(self._categoria, self._view._dp1.value, self._view._dp2.value)

        self._view.txt_result.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {self._view._dp1.value.date()}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {self._view._dp2.value.date()}"))

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        for n in nodi:
            self._view._ddProdStart.options.append(ft.dropdown.Option(
                key=n,
                text=n.product_name,
                on_click=self.choiceDD2
            ))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(
                key=n,
                text=n.product_name,
                on_click=self.choiceDD3
            ))

        self._view.update_page()


    def handleBestProdotti(self, e):
        best5 = self._model.getBest5()

        self._view.txt_result.controls.append(ft.Text("I 5 prodotti più venduti sono:"))

        for n in best5:
            self._view.txt_result.controls.append(ft.Text(f"{n[0]} with score {n[1]}"))

        self._view.update_page()


    def handleCercaCammino(self, e):
        try:
            lunghezza = int(self._view._txtInLun.value)
        except ValueError:
            self._view.create_alert("Errore, seleziona una lunghezza valida")
            self._view.update()
            return

        if self._view._ddProdStart.value is None:
            self._view.create_alert("Errore, seleziona una partenza")
            self._view.update()
            return

        if self._view._ddProdEnd.value is None:
            self._view.create_alert("Errore, seleziona un arrivo")
            self._view.update()
            return

        cammino = self._model.getCammino(self._partenza, self._arrivo, lunghezza)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato"))

        else:
            self._view.txt_result.controls.append(ft.Text("Cammino trovato:"))

            for n in cammino:
                self._view.txt_result.controls.append(ft.Text(n))

        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)


    def choiceDD(self, e):
        self._categoria = e.control.key


    def choiceDD2(self, e):
        self._partenza = e.control.key


    def choiceDD3(self, e):
        self._arrivo = e.control.key