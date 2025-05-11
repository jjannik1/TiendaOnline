from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import date

app = Flask(__name__)

online = MongoClient("mongodb+srv://jjen527:9wv0F9F00KrexmAU@jjannik.aliwych.mongodb.net/")

app.db = online.tienda



@app.route('/dashboard', methods = ["GET", "POST"])
def dashboard():
    global productos, clientes, pedidos
    nombre_admin = "Francisco"
    tienda = "TecnoMarket"
    fecha = date.today()

    productos = [producto for producto in app.db.productos.find({})]
    clientes = [cliente for cliente in app.db.clientes.find({})]
    pedidos = [pedido for pedido in app.db.pedidos.find({})]


    clid = {}
    prod={}
    pedid = {}
    if request.method == "POST":
        formulario = request.form.get("tipo_formulario")

        if formulario == "form_prod":
            prod = {
                "nombre": request.form.get("product"),
                "precio": float(request.form.get("price")),
                "stock": int(request.form.get("stock")),
                "categoria": request.form.get("category")
            }
            productos.append(prod)
            app.db.productos.insert_one(prod)

        elif formulario =="form_client":
            clid = {
                "nombre": request.form.get("clien"),
                "email": request.form.get("email"),
                "activo": request.form.get("act") == "True",
                "pedidos": int(request.form.get("pedidos"))
            }
            clientes.append(clid)
            app.db.clientes.insert_one(clid)

        elif formulario=="form_ped":
            pedid = {
                "cliente": request.form.get("nombr"),
                "total": float(request.form.get("compra")),
                "fecha": request.form.get("dia")
            }
            pedidos.append(pedid)
            app.db.pedidos.insert_one(pedid)



    total_stock = 0
    for producto in productos:
        total_stock += producto["stock"]

    clientes_activos = 0
    for cliente in clientes:
        if cliente["activo"]:
            clientes_activos += 1

    cliente_pedido = clientes[0]
    for cliente in clientes:
        if cliente["pedidos"] > cliente_pedido["pedidos"]:
            cliente_pedido = cliente


    total = 0
    for pedido in pedidos:
        total += pedido["total"]

    return render_template("dashboard.html",nombre_admin=nombre_admin,tienda=tienda,fecha=fecha,productos=productos,clientes=clientes,pedidos=pedidos,total=total,cliente_pedido=cliente_pedido,clientes_activos=clientes_activos,total_stock=total_stock)


if __name__ == '__main__':
    app.run()