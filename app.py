from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

productos = [
        {"nombre": "Portátil Lenovo", "precio": 750.00, "stock": 5, "categoria": "Computadoras"},
        {"nombre": "Ratón Logitech", "precio": 25.50, "stock": 0, "categoria": "Accesorios"},
        {"nombre": "Monitor Samsung", "precio": 199.99, "stock": 3, "categoria": "Pantallas"},
        {"nombre": "Teclado Mecánico", "precio": 45.00, "stock": 10, "categoria": "Accesorios"}
    ]
clientes = [
        {"nombre": "Ana Torres", "email": "ana@correo.com", "activo": True, "pedidos": 3},
        {"nombre": "Luis Rivas", "email": "luis@correo.com", "activo": False, "pedidos": 1},
        {"nombre": "Marta López", "email": "marta@correo.com", "activo": True, "pedidos": 5}
    ]
pedidos = [
        {"cliente": "Ana Torres", "total": 120.00, "fecha": "2025-05-01"},
        {"cliente": "Marta López", "total": 340.50, "fecha": "2025-05-03"},
        {"cliente": "Luis Rivas", "total": 75.00, "fecha": "2025-05-04"}
    ]


@app.route('/dashboard', methods = ["GET", "POST"])
def dashboard():
    global productos, clientes, pedidos
    nombre_admin = "Francisco"
    tienda = "TecnoMarket"
    fecha = date.today()

    



    clid = {}
    prod={}
    pedid = {}
    if request.method == "POST":
        formulario = request.form.get("tipo_formulario")
        if formulario == "producto":
            prod1 = request.form.get("product")
            prod2 = request.form.get("price")
            prod3 = request.form.get("category")
            prod4 = request.form.get("stock")
            prod = {
                "nombre": prod1,
                "precio": float(prod2),
                "stock": int(prod4),
                "categoria": prod3
            }
            productos.append(prod)
        elif formulario =="cliente":
            cli1 = request.form.get("clien")
            cli2 = request.form.get("email")
            cli3 = request.form.get("act")
            cli4 = request.form.get("pedidos")

            if cli3 == "True":
                cli3 = True
            else:
                cli3 = False

            clid = {
                "nombre": cli1,
                "email": cli2,
                "activo": cli3,
                "pedidos": cli4
            }

            clientes.append(clid)
        elif formulario=="pedidos":
            ped1 = request.form.get("nombr")
            ped2 = request.form.get("compra")
            ped3 = request.form.get("dia")

            pedid = {
                "cliente": ped1,
                "total": ped2,
                "fecha": ped3
            }

            pedidos.append(pedid)


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

    return render_template("dashboard.html",nombre_admin=nombre_admin,tienda=tienda,fecha=fecha,productos=productos,clientes=clientes,pedidos=pedidos,total_stock=total_stock,clientes_activos=clientes_activos,cliente_pedido=cliente_pedido,total=total)


if __name__ == '__main__':
    app.run()