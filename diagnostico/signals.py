from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pregunta, Respuesta

@receiver(post_migrate)
def crear_datos_iniciales(sender, **kwargs):
    if sender.name == 'diagnostico':
        if not Pregunta.objects.exists():
            # Pregunta raíz
            p1 = Pregunta.objects.create(texto="¿El motor hace ruidos extraños al encender?", is_root=True)

            # Subpregunta
            p2 = Pregunta.objects.create(texto="¿El ruido proviene de la parte superior del motor?", pregunta_padre=p1)

            # Respuestas de la primera pregunta
            Respuesta.objects.create(texto="Sí", pregunta=p1, siguiente_pregunta=p2)
            Respuesta.objects.create(texto="No", pregunta=p1, diagnostico_final="El motor parece estar en buen estado.")

            # Respuestas de la segunda pregunta
            Respuesta.objects.create(texto="Sí", pregunta=p2, diagnostico_final="Posible causa: válvulas desajustadas.")
            Respuesta.objects.create(texto="No", pregunta=p2, diagnostico_final="Posible causa: bomba de aceite defectuosa.")

            print("✅ Datos iniciales de diagnóstico creados correctamente.")
