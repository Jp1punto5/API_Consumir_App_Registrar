from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

profesores = [
    {
        "id": 1,
        "nombre": "Juan Perez",
        "cursos": 
        [
            {
                "id": 1,
                "nombre": "Matemáticas",
                "codigo": "PGY0000",
                "seccion": "013V",
                "alumnos": [
                    {"id": 1, "nombre": "Luis Gonzalez","correo":"luis.gonzalez@alumno.com","status":0},
                    {"id": 2, "nombre": "Rocio del Carmen Fuentes","correo":"rocio.fuentes@alumno.com","status":0},
                    {"id": 3, "nombre": "Juan Pablo Berrios","correo":"juan.berrios@alumno.com","status":0}
                ]
            },
            {
                "id": 2,
                "nombre": "Fisica",
                "codigo": "PGY0000",
                "seccion": "015V",
                "alumnos": []
            },
            {
                "id": 3,
                "nombre": "Quimica",
                "codigo": "PGY0000",
                "seccion": "018V",
                "alumnos": []
            }
        ]
    },
    {
        "id": 3,
        "nombre": "Juan Pablo Leyton",
        "cursos": 
        [
            {
                "id": 1,
                "nombre": "Ingles Elemental",
                "codigo": "INU",
                "seccion": "0V30",
                "alumnos":
                [
                    {"id":1,"nombre": "Juan Pablo Berrios","correo":"juan.berrios@alumno.com", "status": 0},
                    {"id":2,"nombre": "Rocio del Carmen Fuentes","correo":"rocio.fuentes@alumno.com", "status": 0}
                ]
            }
        ]
    }
]


usuarios = [
    {
        "id": 1,
        "user": "docente",
        "password": "123456",
        "nombre": "Juan Perez",
        "perfil":  1,
        "correo": "juan.perez@docente.com"
    },
    {
        "id": 2,
        "user": "alumno",
        "password": "123456",
        "nombre": "Luis Gonzalez",
        "perfil": 2,
        "correo": "luis.gonzalez@alumno.com"
    },

    {
        "id": 3,
        "user":"docente",
        "password": "123456",
        "nombre": "Juan Pablo Leyton",
        "perfil": 1,
        "correo": "juan.leyton@docente.com"
    },
    {
        "id":4,
        "user":"alumno",
        "password":"123456",
        "nombre":"Juan Pablo Berrios",
        "perfil": 2,
        "correo": "juan.berrios@alumno.com"
    },
    {
        "id":5,
        "user":"alumno",
        "password":"123456",
        "nombre":"Rocio del Carmen Fuentes",
        "perfil": 2,
        "correo":"rocio.fuentes@alumno.com"
    }
]



@app.after_request
def aplicar_cors(response):
    # Permitir origen cruzado
    response.headers['Access-Control-Allow-Origin'] = '*'
    # Métodos permitidos
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    # Encabezados permitidos
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = jsonify({"message": "Preflight request successful"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response, 204



@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('correo')
    password = request.json.get('password')
    
    usuario = next((u for u in usuarios if u["correo"] == username and u["password"] == password), None)
    
    if usuario:
        return jsonify({
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "user": usuario["user"],
            "correo": usuario["correo"],
            "tipoPerfil": usuario["perfil"]
        }), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(usuarios), 200

@app.route('/profesores', methods=['GET'])
def obtener_profesores():
    return jsonify(profesores), 200

@app.route('/profesores/<int:profesor_id>/cursos', methods=['GET','OPTIONS'])
def obtener_cursos_profesor(profesor_id):
    # Lógica para solicitudes GET
    profesor = next((p for p in profesores if p["id"] == profesor_id), None)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404
    return jsonify(profesor["cursos"]), 200

@app.route('/profesores/<int:profesor_id>/cursos/<int:curso_id>/alumnos', methods=['GET'])
def obtener_alumnos_curso(profesor_id, curso_id):
    profesor = next((p for p in profesores if p["id"] == profesor_id), None)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404
    curso = next((c for c in profesor["cursos"] if c["id"] == curso_id), None)
    if not curso:
        return jsonify({"message": "Curso no encontrado"}), 404
    return jsonify(curso["alumnos"]), 200

@app.route('/registrar_asistencia', methods=['POST'])
def registrar_asistencia():
    alumno_id = request.json.get('alumno_id')
    codigo = request.json.get('codigo')
    seccion = request.json.get('seccion')
    fecha = request.json.get('fecha')
    
    # Aquí buscarías el curso y al alumno y actualizarías su estado.
    for profesor in profesores:
        for curso in profesor["cursos"]:
            if curso["codigo"] == codigo and curso["seccion"] == seccion:
                for alumno in curso["alumnos"]:
                    if alumno["id"] == alumno_id:
                        alumno["status"] = 1  # 1 es para presente
                        return jsonify({"message": "Asistencia registrada"}), 200
    
    return jsonify({"message": "No se pudo registrar la asistencia"}), 400



@app.route('/regis_asistencia/<string:codigo_curso>/<string:codigo_seccion>/<string:correo_a>',methods=['POST'])
def registrar_(codigo_curso,codigo_seccion,correo_a):

    curso_encontraro = False # bandera
    for profesor in profesores:
        for curso in profesor['cursos']:
            if curso['codigo'] == codigo_curso and curso['seccion'] == codigo_seccion:
                curso_encontraro = True # Maramos el curso existente
                for alumno in curso['alumnos']:
                    if alumno['correo'] == correo_a:
                        if alumno['status'] == 1: #aqui se valida que el alumno ya se haya registrado antes
                            return jsonify({"message":"El Alumno ya se encuentra presente"}), 401
                        else:
                            alumno['status'] = 1 # aqui se registra la asistencia
                            return jsonify({"message":"Asistencia registrada exitosamente"}), 200
            
    # Si no se encontro el curso despues de recorrer todos
    if not curso_encontraro:
        return jsonify({"message":"El curso ingresado no existe"}),401 # este error no deberia ocurrir
                

    return jsonify({"message":"No se registro la asistencia!"}), 400


#este metodo recetea al final mi asistencia
@app.route('/eliminar_asistencia',methods=['POST'])
def eliminar_asistencia():
    curso_c = request.json.get('codigo')
    seccion = request.json.get('seccion')
    alumno_id = request.json.get('alumno_id')

    for profesor in profesores:
        for curso in profesor['cursos']:
            if curso['codigo'] == curso_c and curso['seccion'] == seccion:
                for alumno in curso['alumnos']:
                    if alumno['id'] == alumno_id:
                        alumno['status'] = 0 # aqui reseteo la asistencia
                        return jsonify({"message":"asistencia receteada"}),200
    return jsonify({"message":"No se pudo realizar el reseteo de asistencia"}),400



if __name__ == '__main__':
    app.run(debug=True)
