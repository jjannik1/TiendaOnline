from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import date

app = Flask(__name__)

online = MongoClient("mongodb+srv://jjen527:35OpRHzih8l1N14m@jjannik.aliwych.mongodb.net/")

app.db = online.tienda

nombre_admin = "Jannik"
tienda = "TecnoMarket"
fecha = date.today()



@app.route("/")
def inicio():

    pagina = "indice"
    

    productos = [producto for producto in app.db.productos.find({})]
    clientes = [cliente for cliente in app.db.clientes.find({})]
    pedidos = [pedido for pedido in app.db.pedidos.find({})]

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

    return render_template("dashboard.html",nombre_admin=nombre_admin,tienda=tienda,fecha=fecha,productos=productos,clientes=clientes,pedidos=pedidos,total=total,cliente_pedido=cliente_pedido,clientes_activos=clientes_activos,total_stock=total_stock,pagina=pagina)


@app.route("/productos", methods=["GET", "POST"])
def productos():
    productos = [producto for producto in app.db.productos.find({})]

    pagina = "productos"
    
    if request.method == "POST":
        formulario = request.form.get("tipo_formulario")
        if formulario == "form_prod":
            prod = {
                "nombre": request.form.get("product"),
                "precio": float(request.form.get("price")),
                "stock": int(request.form.get("stock")),
                "categoria": request.form.get("category")
            }
            app.db.productos.insert_one(prod)
            return redirect(url_for("productos"))
        
        elif formulario == "elim_prod":
            eliprod = request.form.get("elproduct")
            app.db.productos.delete_one({"nombre": eliprod})
            return redirect(url_for("productos"))
        
        elif formulario == "cambio_stock":
            nombre_prod = request.form.get("prod_a_cambiar").strip()
            nuevo_stock = request.form.get("nuevo_stock")
            nuevo_precio = request.form.get("nuevo_precio")

            cambios = {}
            if nuevo_stock:
                cambios["stock"] = int(nuevo_stock)
            if nuevo_precio:
                cambios["precio"] = float(nuevo_precio)

            if cambios:
                app.db.productos.update_one({"nombre": nombre_prod}, {"$set": cambios})
            
            return redirect(url_for("productos"))


        """        elif formulario=="cambio_stock":
            elstock = request.form.get("prod_a_cambiar")
            new_stock = int(request.form.get("nuevo_stock"))
            app.db.productos.update_one({"nombre": elstock}, {"$set": {"stock": new_stock}})
            return redirect(url_for("productos"))
        """

    total_stock = 0
    for producto in productos:
        total_stock += producto["stock"]

    return render_template("dashboard.html", 
                           nombre_admin=nombre_admin, 
                           tienda=tienda, 
                           fecha=fecha, 
                           productos=productos,pagina=pagina,
                           total_stock=total_stock)



@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    clientes = [cliente for cliente in app.db.clientes.find({})]
    
    pagina = "clientes"

    if request.method == "POST":
        formulario = request.form.get("tipo_formulario")
        if formulario == "form_client":
            clid = {
                "nombre": request.form.get("clien"),
                "email": request.form.get("email"),
                "activo": request.form.get("act") == "True",
                "pedidos": int(request.form.get("pedidos"))
            }
            app.db.clientes.insert_one(clid)
            return redirect(url_for("clientes"))
        
        elif formulario == "elim_client":
            eliclient = request.form.get("elcliente")
            app.db.clientes.delete_one({"nombre": eliclient})
            return redirect(url_for("clientes"))


    clientes_activos = 0
    for cliente in clientes:
        if cliente["activo"]:
            clientes_activos += 1

    cliente_pedido = clientes[0]
    for cliente in clientes:
        if cliente["pedidos"] > cliente_pedido["pedidos"]:
            cliente_pedido = cliente

    return render_template("dashboard.html", 
                           nombre_admin=nombre_admin, 
                           tienda=tienda, 
                           fecha=fecha, 
                           clientes=clientes,pagina=pagina,
                           clientes_activos=clientes_activos,
                           cliente_pedido=cliente_pedido)


@app.route("/pedidos", methods=["GET", "POST"])
def pedidos():
    pedidos = [pedido for pedido in app.db.pedidos.find({})]

    pagina = "pedidos"
    
    if request.method == "POST":
        formulario = request.form.get("tipo_formulario")
        if formulario == "form_ped":
            pedid = {
                "cliente": request.form.get("nombr"),
                "total": float(request.form.get("compra")),
                "fecha": request.form.get("dia")
            }
            app.db.pedidos.insert_one(pedid)
            return redirect(url_for("pedidos"))
        elif formulario == "elim_ped":
            eliped = request.form.get("elpedido")
            app.db.pedidos.delete_one({"cliente": eliped})
            return redirect(url_for("pedidos"))


    total = 0
    for pedido in pedidos:
        total += pedido["total"]

    return render_template("dashboard.html", 
                           nombre_admin=nombre_admin, 
                           tienda=tienda, 
                           fecha=fecha, 
                           pedidos=pedidos,pagina=pagina,
                           total=total)



if __name__ == '__main__':
    app.run()
