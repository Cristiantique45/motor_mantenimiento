from django.core.management.base import BaseCommand
from diagnostico.models import Pregunta, Respuesta


class Command(BaseCommand):
    help = 'Fill missing Respuesta entries that link parent questions to their child questions.'

    def handle(self, *args, **options):
        pairs = [
            # root -> categories (should already exist)
            ("Mantenimiento de líquidos", "Aceite del motor"),
            ("Mantenimiento de líquidos", "Aceite de la caja"),
            ("Mantenimiento de líquidos", "Líquido de frenos"),
            ("Mantenimiento de líquidos", "Líquido hidráulico de dirección"),

            ("Mantenimiento de componentes", "Rodamientos"),
            ("Mantenimiento de componentes", "Filtro de aire"),
            ("Mantenimiento de componentes", "Bujías"),
            ("Mantenimiento de componentes", "Llantas"),

            ("Inspección visual", "Revisión de mangueras"),
            ("Inspección visual", "Revisión de correas"),

            # líquidos intermedios -> sus opciones
            ("Aceite del motor", "¿Ha excedido el kilometraje recomendado para cambio de aceite?"),
            ("Aceite del motor", "¿Color del aceite en la varilla?"),
            ("Aceite de la caja", "¿Estado del aceite de la caja?"),
            ("Líquido de frenos", "¿Estado del líquido de frenos?"),
            ("Líquido de frenos", "¿Hace más de 5 años del último cambio?"),
            ("Líquido hidráulico de dirección", "¿Nivel del líquido hidráulico?"),

            # componentes intermedios -> sus opciones
            ("Rodamientos", "¿Kilometraje desde último cambio de rodamientos?"),
            ("Filtro de aire", "¿Kilometraje desde último cambio de filtro?"),
            ("Filtro de aire", "¿Estado del filtro de aire?"),
            ("Bujías", "¿Hace cuántos años se cambiaron las bujías?"),
            ("Bujías", "¿Kilometraje desde último cambio de bujías?"),
            ("Llantas", "¿Profundidad del grabado de las llantas?"),

            # inspección visual internals
            ("Revisión de mangueras", "¿Estado de las mangueras?"),
            ("Revisión de correas", "¿Estado de las correas?"),
        ]

        created = 0
        for parent_text, child_text in pairs:
            parent = Pregunta.objects.filter(texto=parent_text).first()
            child = Pregunta.objects.filter(texto=child_text).first()
            if not parent:
                self.stdout.write(self.style.WARNING(f"Parent not found: {parent_text}"))
                continue
            if not child:
                self.stdout.write(self.style.WARNING(f"Child not found: {child_text}"))
                continue

            exists = Respuesta.objects.filter(pregunta=parent, siguiente_pregunta=child).exists()
            if exists:
                self.stdout.write(f"Exists: {parent_text} -> {child_text}")
                continue

            Respuesta.objects.create(texto=child.texto, pregunta=parent, siguiente_pregunta=child)
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Created: {parent_text} -> {child_text}"))

        self.stdout.write(self.style.SUCCESS(f"Done. {created} respuestas created."))
