# diagnostico/models.py
from django.db import models

class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    pregunta_padre = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subpreguntas'
    )
    is_root = models.BooleanField(default=False)  # 👈 Campo agregado

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    texto = models.CharField(max_length=100)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    siguiente_pregunta = models.ForeignKey(
        Pregunta, on_delete=models.SET_NULL, null=True, blank=True, related_name='respuestas_anteriores'
    )
    diagnostico_final = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.texto} → {self.siguiente_pregunta or self.diagnostico_final}"
