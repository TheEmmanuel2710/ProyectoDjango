from django.db import models

# Create your models here.
class Categoria(models.Model):
    catNombre=models.CharField(max_length=25,unique=True)
    
    def __str__(self) -> str:
        return self.catNombre

class Producto(models.Model):
    proCodigo=models.IntegerField(unique=True)
    proNombre=models.CharField(max_length=45)
    proPrecio=models.IntegerField()
    proCategoria=models.ForeignKey(Categoria,on_delete=models.PROTECT)
    proFoto=models.FileField(upload_to=f"fotos/",null=True,blank=True)
    
    def __str__(self) -> str:
        return self.proNombre