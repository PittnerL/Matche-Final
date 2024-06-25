from flask import Flask, request, jsonify

app = Flask(__name__)

mates = [
    {'Modelo': 'small', 'stock': 8},
    {'Modelo': 'medium', 'stock': 14},
    {'Modelo': 'large', 'stock': 21},
    {'Modelo': 'xlarge', 'stock': 18}
]

@app.route('/')
def home():
    return (
        'Nos enorgullece presentarles una innovadora manera de disfrutar nuestra tradición más querida: el mate. En MATECH, hemos fusionado lo mejor de la tecnología con la esencia del mate tradicional, creando el primer mate convencional con control de temperatura. Con nuestro producto, podrán disfrutar de un mate siempre a la temperatura perfecta, sin preocuparse por conseguir agua caliente, que se enfríe o por quemarse. Matech está diseñado para mantener viva la pasión y el ritual del mate, adaptándose a las necesidades de la vida moderna. Gracias por acompañarnos en este viaje. ¡Salud y buenos mates!'
    )


@app.route('/mates', methods=['POST'])
def matesPost():
    body = request.json
    modelo = body.get('Modelo')
    stock = body.get('stock')

    if not modelo or not isinstance(stock, int):
        return jsonify({'error': 'Datos inválidos', 'status': 'error'}), 400

    if any(p['Modelo'] == modelo for p in mates):
        return jsonify({'error': 'Modelo ya existe', 'status': 'error'}), 400

    newProd = {'Modelo': modelo, 'stock': stock}
    mates.append(newProd)
    return jsonify({'mates': mates, 'status': 'ok'}), 201

@app.route('/mates', methods=['GET'])
def matesGet():
    return jsonify({'mates': mates, 'status': 'ok'})

@app.route('/mates/<modelo>', methods=['GET'])
def matesGetx(modelo):
    mate = next((p for p in mates if p['Modelo'] == modelo), None)
    if mate:
        return jsonify({'mate': mate, 'status': 'ok'})
    else:
        return jsonify({'error': 'Mate no encontrado', 'status': 'error'}), 404

@app.route('/mates/<modelo>', methods=['PUT'])
def updateMate(modelo):
    body = request.json
    new_stock = body.get('stock')

    if not isinstance(new_stock, int):
        return jsonify({'error': 'Datos inválidos', 'status': 'error'}), 400

    mate = next((p for p in mates if p['Modelo'] == modelo), None)
    if mate:
        mate['stock'] = new_stock
        return jsonify({'mate': mate, 'status': 'ok'})
    else:
        return jsonify({'error': 'Mate no encontrado', 'status': 'error'}), 404

@app.route('/mates/<modelo>', methods=['DELETE'])
def deleteMate(modelo):
    global mates
    mates = [p for p in mates if p['Modelo'] != modelo]
    return jsonify({'mates': mates, 'status': 'ok'})


@app.route('/ventas', methods=['POST'])
def registrarVenta():
    body = request.json
    modelo = body.get('Modelo')
    cantidad = body.get('cantidad')

    if not modelo or not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({'error': 'Datos inválidos', 'status': 'error'}), 400

    mate = next((p for p in mates if p['Modelo'] == modelo), None)
    if mate:
        if mate['stock'] < cantidad:
            return jsonify({'error': 'Stock insuficiente', 'status': 'error'}), 400
        mate['stock'] -= cantidad
        return jsonify({'mate': mate, 'status': 'ok'})
    else:
        return jsonify({'error': 'Mate no encontrado', 'status': 'error'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
