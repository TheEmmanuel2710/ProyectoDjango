from django.shortcuts import render,redirect
from appTienda.models import Categoria,Producto
from django.db import Error
from django.db import IntegrityError
from rest_framework import generics
from appTienda.serializers import CategoriaSerializer,ProductoSerializer
import os
# Create your views here.
# -----Inicio comandos
# py -m venv entorno,crea el entorno
# django-admin startproject GestionNegocio
# cd Gestion Negocio 
# python manage.py startapp appTienda,para crear la aplicacion
# python manage.py makemigrations, para crear las migraciones para poder después crear las tablas en la base de datos.
# python manage.py migrate,para terminar de crear las tablas en la base de datos 
# python manage.py runserver
# python manage.py createsuperuser
#emma
#1627manueltami
# pip freeze > requirements.txt
#pip install -r  requirements.txt
#py manage.py runserver 0.0.0.0:8000
# pip install djangorestframework
# pip install fpdf
# pip install django-cors-headers
# ----Fin comandos
def inicio(request):
    return render(request,"Inicio.html")

def vistaCategorias(request):
    return render(request,"frmAgregarCategoria.html")
    
def agregarCategoria(request):
    nombre=request.POST["txtNombre"]
    try:
        categoria=Categoria(catNombre=nombre)
        categoria.save()
        mensaje="-----Categoria agregada correctamente-----"
    except Error as error:
        mensaje=f"-----Problemas al agregar la categoria {error}-----"
    retorno={"mensaje":mensaje}
    return render(request,"frmAgregarCategoria.html",retorno)

def vistaProducto(request):
    try:
        categorias=Categoria.objects.all()
        mensaje=""
    except Error as error:
        mensaje=f"Problemas -->{error}"
    retorno={"mensaje":mensaje,"listaCategorias":categorias,"producto":None}
    return render(request,"frmAgregarProducto.html",retorno)

def listarProductos(request):
    try:
        productos=Producto.objects.all()
        mensaje=""
    except Error as error:
        mensaje=f"-----Problemas al listar {error}-----"
    retorno={"mensaje":mensaje,"listaProductos":productos}
    return render(request,"listarProductos.html",retorno)


def agregarProducto(request):
    nombre = request.POST["txtNombre"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES["fileFoto"]
    try:
        # obtener la categoria de acuerdo a su id
        categoria = Categoria.objects.get(id=idCategoria)
        producto = Producto(proNombre=nombre, proCodigo=codigo, proPrecio=precio, proCategoria=categoria, proFoto=archivo)
        # Verificacion de la existencia del producto con un codigo duplicado
        if Producto.objects.filter(proCodigo=codigo).exists():
            mensaje = f"El producto con código {codigo} ya existe"
        else:   
            # crear el producto
            producto = Producto(proNombre=nombre, proCodigo=codigo, proPrecio=precio, proCategoria=categoria, proFoto=archivo)
            # registrar el producto a la base de datos
            producto.save()           
            mensaje = "Producto Agregado de manera satisfactoria"
            return redirect("/listarProductos/")
        
    except IntegrityError as error:
        mensaje = f"Problemas al agregar->{error}"
    categorias = Categoria.objects.all()
    retorno = {"mensaje": mensaje, "listaCategorias": categorias, "producto": producto}
    return render(request, "frmAgregarProducto.html", retorno)

def consultarProducto(request,id):
    try:
        producto=Producto.objects.get(id=id)
        categorias=Categoria.objects.all()
        mensaje=""
    except Error as error:
        mensaje=f"Problemas -->{error}"
    retorno={
        "mensaje":mensaje,
        "producto":producto,
        "listaCategoria":categorias
    }
    return render(request,"frmEditar.html",retorno)

def actualizarProducto(request):
    idProducto=int(request.POST["idProducto"])
    nombre=request.POST["txtNombre"]
    codigo= int(request.POST["txtCodigo"])
    precio= int(request.POST["txtPrecio"])
    idCategoria= int(request.POST["cbCategoria"])
    archivo=request.FILES.get("fileFoto",False)
    try:
        categoria=Categoria.objects.get(id=idCategoria)
        producto=Producto.objects.get(id=idProducto)
        producto.proNombre=nombre
        producto.proPrecio=precio
        producto.proCategoria=categoria
        producto.proCodigo=codigo
        if(archivo!=''):
            producto.proFoto=archivo
        producto.save()
        mensaje="Producto actualizado de manera correcta"
        return redirect("/listarProductos/")
    except Error as error:
        mensaje=f"Problemas al actualizar ->{error}"
    categorias=Categoria.objects.all()
    retorno={"mensaje":mensaje,"listaCategoria":categorias,"producto":producto}
    return render(request,"frmEditar.html",retorno)    


def eliminarProducto(request, id):
    try:
        producto = Producto.objects.get(id=id)
        # Guardar el path de la imagen antes de borrar el producto
        imagen = producto.proFoto.path
        producto.delete()
        # Borrar la imagen del producto de la carpeta de fotos
        os.remove(imagen)
        mensaje = "Producto eliminado"
    except Error as error:
        mensaje = f"Problemas al eliminar el producto -->{error}"
    retorno = {
        "mensaje": mensaje
    }
    return redirect("/listarProductos/", retorno)

class CategoriaList(generics.ListCreateAPIView):
    queryset=Categoria.objects.all()
    serializer_class=CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Categoria.objects.all()
    serializer_class=CategoriaSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer
