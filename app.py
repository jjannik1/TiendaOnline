from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route("/dashboard")
def tienda():
    nombre_admin = "Francisco"
    tienda = "TecnoMarket"
    fecha = date.today()

    productos = [
        {"nombre": "Monitor",
         "precio": 25.99,
         "stock": 3,
         "catagoria": "Monitores"},
         {"nombre": "Raton",
          "precio": 12.87,
          "stock": 6,
          "categoria": "perifericos"}
    ]


if __name__=="__main__":
    app.run()