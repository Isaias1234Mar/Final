from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)
# configurar el objeto que se usara
# app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:12345@localhost:5432/db"
app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://pfvgdfodrelbar:5c35a63a837ce64bc27cf3ad37fb89ed4736be988f512b938180058e289cbd13@ec2-54-147-107-18.compute-1.amazonaws.com:5432/d732br82sceecj"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#Modelos de la tablas 
class Usuarios(db.Model):
    __tablename__="usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __int__(self, email, password):
        self.nombre_usuario=nombre_usuario
        self.email=email
        self.password= password

#Tabla editorial
class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial= nombre_editorial

#Tabla genero
class  Genero(db.Model):
    __tablename__="genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    tipo_genero = db.Column(db.String(100))

    def __init__(self,  tipo_genero ):
        self.tipo_genero = tipo_genero 

#Tabla autor
class  Autor(db.Model):
    __tablename__="autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor= db.Column(db.String(100))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))

    def __init__(self, nombre_autor,fecha_nac,nacionalidad):
        self.nombre_autor= nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad =nacionalidad

#Tabla libro
class Libro(db.Model):
    __tablename__="libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    #Relación
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial,id_autor, id_genero):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_editorial = id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero
#Tabla MisFavoritos
class  MisFavoritos(db.Model):
    __tablename__="misfavoritos"
    id_lista_favoritos = db.Column(db.Integer, primary_key=True)

    #Relación
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    consulta_usuario = Usuarios.query.filter_by(email = email).first()
    print(consulta_usuario)
    bcrypt.check_password_hash(consulta_usuario.password, password)
    return render_template("inicio.html")

@app.route("/registro")
def registrar():
    return render_template("registrar.html")

@app.route("/registro_usuario", methods=['POST'])
def register_user():
    nombre_usuario = request.form["nombre_usuario"]
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)

    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)

    usuario = Usuarios(nombre_usuario=nombre_usuario,email = email, password = password_cifrado)
    db.session.add(usuario)
    db.session.commit()
    return redirect("/")

@app.route("/iniciar_sesion")
def iniciar_sesion():
    redirect("/")


# Para registar Libros
@app.route("/libro")
def libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_genero = Genero.query.all()
    consulta_autor = Autor.query.all()
    return render_template("libro.html", consulta_editorial=consulta_editorial,consulta_genero=consulta_genero,consulta_autor=consulta_autor)

@app.route("/registrarLibro", methods=["POST"])
def registroLibro():
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]

    id_editorial = request.form["editorial"]
    id_autor = request.form["autor"]
    id_genero = request.form["genero"]
    numero_paginas_int = int(numero_paginas)

    libro_nuevo = Libro(titulo_libro=titulo_libro, fecha_publicacion=fecha_publicacion,numero_paginas=numero_paginas,formato=formato,volumen=volumen,id_editorial=id_editorial,id_autor=id_autor,id_genero=id_genero,)
    db.session.add(libro_nuevo)
    db.session.commit()
    message = "Libro registrado :D"
    return redirect("/leerlibros")
#Mostar libros
@app.route("/leerlibros")
def leerlibros():
    consulta_libro = Libro.query.join(Editorial, Libro.id_editorial == Editorial.id_editorial).join(Autor, Libro.id_autor == Autor.id_autor).join(Genero, Libro.id_genero == Genero.id_genero).add_columns(Libro.titulo_libro, Libro.fecha_publicacion, Libro.numero_paginas, Libro.formato, Libro.volumen, Editorial.nombre_editorial, Autor.nombre_autor, Genero.tipo_genero, Libro.id_libro)
    return render_template("mostrar_libro.html", consulta = consulta_libro)
#Eliminar Libros
@app.route("/eliminarlibro/<id>")
def eliminar(id):
    #para identificar la linea en la base de datos 
    libro = Libro.query.filter_by(id_libro = int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect("/leerlibros")
#Modificar libros
@app.route("/editarLibro/<id>")
def editarLibro(id):
    libro = Libro.query.filter_by(id_libro = int(id)).first() 
    consulta_autor = Autor.query.all()
    consulta_editorial = Editorial.query.all()
    consulta_genero = Genero.query.all()
    return render_template("modificarlibro.html", libro = libro, consulta_autor=consulta_autor, consulta_editorial = consulta_editorial, consulta_genero = consulta_genero)

@app.route("/modificarLibro", methods=['POST'])
def modificarLibro():
    id_libro = request.form["id_libro"]
    nuevo_titulo = request.form["titulo_libro"]
    nueva_fecha = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    editorial = request.form["editorial"]
    autor = request.form["autor"]
    genero = request.form["genero"]

    libro = Libro.query.filter_by(id_libro = int(id_libro)).first()
    libro.titulo_libro = nuevo_titulo
    libro.fecha_publicacion = nueva_fecha
    libro.numero_paginas = numero_paginas
    libro.formato = formato
    libro.volumen = volumen
    libro.id_editorial = editorial
    libro.id_autor = autor
    libro.id_genero = genero
    db.session.commit()
    return redirect("/leerlibros")


# Para registar Editoriales
@app.route("/editorial")
def editorial():
    return render_template("editorial.html")

@app.route("/registroEditorial", methods=["POST"])
def registroEditorial():
    nombre_editorial = request.form["nombre_editorial"]
    editorial_nueva =Editorial(nombre_editorial=nombre_editorial)
    db.session.add(editorial_nueva)
    print(editorial_nueva)
    db.session.commit()
    message = "Editorial registrada"
    return redirect("/leerEditoriales")
#Mostar editoriales
@app.route("/leerEditoriales")
def leerEditoriales():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    for editorial in consulta_editorial:
        nombre_editorial = editorial.nombre_editorial
    return render_template("mostrar_editorial.html", consulta = consulta_editorial )
#Eliminar editoriles
@app.route("/eliminareditorial/<id>")
def eliminareditorial(id):
    #para identificar la linea en la base de datos 
    editorial = Editorial.query.filter_by(id_editorial = int(id)).delete()
    db.session.commit()
    return redirect("/leerEditoriales")
#Modificar editoriales
@app.route("/editareditorial/<id>")
def editareditorial(id):
    editorial = Editorial.query.filter_by(id_editorial = int(id)).first()
    return render_template("modificareditorial.html", editorial = editorial)

@app.route("/modificareditorial", methods=['POST'])
def modificareditorial():
    id_editorial = request.form["id_editorial"]
    nombre_editorial = request.form["nombre_editorial"]
    editorial = Editorial.query.filter_by(id_editorial = int(id_editorial)).first()
    editorial.nombre_editorial = nombre_editorial
    db.session.commit()
    return redirect("/leerEditoriales")


# Para registar Generos
@app.route("/genero")
def genero():
    return render_template("genero.html")

@app.route("/registroGenero", methods=["POST"])
def registroGenero():
    tipo_genero = request.form["tipo_genero"]
    genero_nuevo = Genero(tipo_genero=tipo_genero)
    db.session.add(genero_nuevo)
    print(genero_nuevo)
    db.session.commit()
    message = "Genero registrado"
    return redirect("/leerGenero")

#Mostar genero
@app.route("/leerGenero")
def leerGenero():
    consulta_genero = Genero.query.all()
    for genero in consulta_genero:
        tipo_genero = genero.tipo_genero
    return render_template("mostrar_genero.html", consulta = consulta_genero)
#Eliminar genero
@app.route("/eliminargenero/<id>")
def eliminargenero(id):
    #para identificar la linea en la base de datos 
    genero = Genero.query.filter_by(id_genero = int(id)).delete()
    db.session.commit()
    return redirect("/leerGenero")
#Modificar genero
@app.route("/editargenero/<id>")
def editargenero(id):
    genero = Genero.query.filter_by(id_genero = int(id)).first()
    return render_template("modificargenero.html", genero = genero)

@app.route("/modificargenero", methods=['POST'])
def modificargenero():
    id_genero = request.form["id_genero"]
    tipo_genero = request.form["tipo_genero"]
    genero = Genero.query.filter_by(id_genero = int(id_genero)).first()
    genero.tipo_genero = tipo_genero
    db.session.commit()
    return redirect("/leerGenero")


# Para registar Autores
@app.route ("/autor")
def autor():
    return render_template("/autor.html")

@app.route("/registrarAutor",methods=["POST"])
def registrarAutor():
    nombre_autor = request.form["nombre_autor"] 
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]

    autor_nuevo = Autor(nombre_autor=nombre_autor,fecha_nac=fecha_nac,nacionalidad=nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    message = "Autor registrado :D"
    return redirect("leerAutores")
#Mostar Autores
@app.route("/leerAutores")
def leerAutores():
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    for autor in consulta_autor:
        nombre = autor.nombre_autor
        fecha_nac = autor.fecha_nac
        nacionalidad = autor.nacionalidad
    return render_template("mostrar_autor.html", consulta = consulta_autor)
#Eliminar Autores
@app.route("/eliminarAutor/<id>")
def eliminarAutor(id):
    #para identificar la linea en la base de datos 
    autor = Autor.query.filter_by(id_autor = int(id)).delete()
    print(autor)
    db.session.commit()
    return redirect("/leerAutores")
#Modificar Autores
@app.route("/editarAutor/<id>")
def editarAutor(id):
    autor = Autor.query.filter_by(id_autor = int(id)).first()
    return render_template("modificarautor.html", autor = autor)

@app.route("/modificarautor", methods=['POST'])
def modificarautor():
    id_autor = request.form["id_autor"]
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]
    autor = Autor.query.filter_by(id_autor = int(id_autor)).first()
    autor.nombre_autor = nombre_autor
    autor.fecha_nac = fecha_nac
    autor.nacionalidad = nacionalidad
    db.session.commit()
    return redirect("/leerAutores")


#Para registra en Mis Favoritos
@app.route ("/missFavoritos")
def missFavoritos():
    return redirect("/mostrar_Favorito")

@app.route("/misFavoritos/<id>")
def misFavoritos(id):
    libro = Libro.query.filter_by(id_libro = int(id)).first()
    usuario = Usuarios.query.filter_by(id_usuario = int(1)).first()
    return render_template("misfavoritos.html",libro = libro,usuario = usuario)

@app.route("/registroFavorito", methods=["POST"])
def registroFavorito():
    id_usuario = request.form["id_usuario"]
    id_libro = request.form["id_libro"]
    favorito_nuevo = MisFavoritos(id_libro=id_libro,id_usuario=id_usuario)
    db.session.add(favorito_nuevo)
    db.session.commit()
    return redirect("/mostrar_Favorito")

@app.route("/mostrar_Favorito")
def mostra_Favorito():
    consulta = MisFavoritos.query.join(Libro, MisFavoritos.id_libro == Libro.id_libro).join(Usuarios, MisFavoritos.id_usuario==Usuarios.id_usuario).add_columns(Libro.titulo_libro,Libro.id_libro)
    return render_template("mostrarFavoritos.html", consulta = consulta)

@app.route("/eliminarFavorito/<id>")
def eliminarFavorito(id):
    #para identificar la linea en la base de datos 
    misfavoritos = MisFavoritos.query.filter_by(id_libro = int(id)).delete()
    print(misfavoritos)
    db.session.commit()
    return redirect("/mostrar_Favorito")

if __name__== "__main__":
    db.create_all()
    app.run(debug=True)