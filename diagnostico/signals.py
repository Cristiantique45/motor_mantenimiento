from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pregunta, Respuesta


@receiver(post_migrate)
def crear_datos_iniciales(sender, **kwargs):
    if sender.name == 'diagnostico':
        if not Pregunta.objects.exists():
            # Raíz del flujo de mantenimiento e inspección
            root = Pregunta.objects.create(texto="Mantenimiento e inspección", is_root=True)

            # Nodo: Mantenimiento de líquidos (categoriza por tipo de líquido)
            p_liquidos = Pregunta.objects.create(texto="Mantenimiento de líquidos", pregunta_padre=root)

            # Tipos de líquido como subpreguntas
            p_lubricante = Pregunta.objects.create(texto="Líquido lubricante", pregunta_padre=p_liquidos)
            p_refrigerante = Pregunta.objects.create(texto="Líquido refrigerante", pregunta_padre=p_liquidos)
            p_hidraulico = Pregunta.objects.create(texto="Líquido hidráulico de dirección asistida", pregunta_padre=p_liquidos)

            # --- LUBRICANTE ---
            # Niveles / síntomas
            p_lub_nivel = Pregunta.objects.create(texto="¿Líquido lubricante bajo?", pregunta_padre=p_lubricante)
            p_lub_alto = Pregunta.objects.create(texto="¿Líquido lubricante alto?", pregunta_padre=p_lubricante)

            # Calidad del lubricante
            p_lub_calidad = Pregunta.objects.create(texto="¿Revisar la calidad del lubricante (turbio/ok)?", pregunta_padre=p_lub_nivel)
            p_lub_comprobar_nivel = Pregunta.objects.create(texto="Comprobar nivel del líquido lubricante", pregunta_padre=p_lub_calidad)

            # --- REFRIGERANTE ---
            p_ref_nivel = Pregunta.objects.create(texto="Nivel del líquido refrigerante (Bajo/Medio/Alto)", pregunta_padre=p_refrigerante)
            p_ref_inspeccion = Pregunta.objects.create(texto="Inspecciona el líquido refrigerante (color/partículas)", pregunta_padre=p_ref_nivel)
            p_ref_cierra_compuerta = Pregunta.objects.create(texto="Cerrar compuerta del líquido refrigerante", pregunta_padre=p_ref_inspeccion)

            # --- HIDRÁULICO (dirección asistida) ---
            p_hid_nivel = Pregunta.objects.create(texto="Nivel del líquido hidráulico (Bajo/Medio/Alto)", pregunta_padre=p_hidraulico)
            p_hid_revisa_fuga = Pregunta.objects.create(texto="Revisa posible fuga", pregunta_padre=p_hid_nivel)
            p_hid_inspeccion_color = Pregunta.objects.create(texto="Inspecciona el color/estado del líquido hidráulico", pregunta_padre=p_hid_nivel)

            # Respuestas raíz -> categorías
            Respuesta.objects.create(texto="Mantenimiento de líquidos", pregunta=root, siguiente_pregunta=p_liquidos)

            # Respuestas para tipos de líquido
            Respuesta.objects.create(texto="Líquido lubricante", pregunta=p_liquidos, siguiente_pregunta=p_lubricante)
            Respuesta.objects.create(texto="Líquido refrigerante", pregunta=p_liquidos, siguiente_pregunta=p_refrigerante)
            Respuesta.objects.create(texto="Líquido hidráulico de dirección asistida", pregunta=p_liquidos, siguiente_pregunta=p_hidraulico)

            # --- Respuestas para lubricante ---
            Respuesta.objects.create(texto="Bajo", pregunta=p_lubricante, siguiente_pregunta=p_lub_nivel)
            Respuesta.objects.create(texto="Alto", pregunta=p_lubricante, siguiente_pregunta=p_lub_alto)

            # Si está bajo -> preguntar si drena / revisar calidad
            Respuesta.objects.create(texto="Drena el aceite", pregunta=p_lub_nivel, diagnostico_final="Realizar cambio de aceite.")
            Respuesta.objects.create(texto="No drena", pregunta=p_lub_nivel, siguiente_pregunta=p_lub_calidad)

            # Calidad
            Respuesta.objects.create(texto="Está turbio", pregunta=p_lub_calidad, siguiente_pregunta=p_lub_comprobar_nivel)
            Respuesta.objects.create(texto="Está bien", pregunta=p_lub_calidad, diagnostico_final="Cerrar tapa de aceite y finalizar; programar revisión si persiste.")

            # Comprobar nivel (resultado)
            Respuesta.objects.create(texto="Mal (nivel)", pregunta=p_lub_comprobar_nivel, diagnostico_final="Nivel incorrecto: rellenar o llevar a taller.")
            Respuesta.objects.create(texto="Bien (nivel)", pregunta=p_lub_comprobar_nivel, diagnostico_final="Nivel correcto: cerrar tapa y finalizar.")

            # Si está alto -> inspeccionar color/contaminación
            Respuesta.objects.create(texto="Inspeccionar color/contaminación", pregunta=p_lub_alto, diagnostico_final="Revisar calidad y posibles fugas o sobrellenado; corregir según tipo.")

            # --- Respuestas para refrigerante ---
            Respuesta.objects.create(texto="Bajo", pregunta=p_refrigerante, siguiente_pregunta=p_ref_nivel)
            Respuesta.objects.create(texto="Medio", pregunta=p_refrigerante, siguiente_pregunta=p_ref_nivel)
            Respuesta.objects.create(texto="Alto", pregunta=p_refrigerante, siguiente_pregunta=p_ref_nivel)

            # Acciones según nivel
            Respuesta.objects.create(texto="Drenar el líquido actual", pregunta=p_ref_nivel, diagnostico_final="Drenar y reemplazar el líquido refrigerante según especificación.")
            Respuesta.objects.create(texto="Inspeccionar líquido", pregunta=p_ref_nivel, siguiente_pregunta=p_ref_inspeccion)

            # Inspección: partículas/color
            Respuesta.objects.create(texto="Tiene partículas externas", pregunta=p_ref_inspeccion, diagnostico_final="Partículas en refrigerante: limpiar sistema y reemplazar líquido.")
            Respuesta.objects.create(texto="Está bien", pregunta=p_ref_inspeccion, siguiente_pregunta=p_ref_cierra_compuerta)
            Respuesta.objects.create(texto="Tiene manchas/olor", pregunta=p_ref_inspeccion, diagnostico_final="Contaminación del refrigerante: solicitar técnica y reemplazo.")

            Respuesta.objects.create(texto="Cerrar compuerta", pregunta=p_ref_cierra_compuerta, diagnostico_final="Cerrar compuerta del sistema de refrigeración y monitorizar nivel.")

            # --- Respuestas para hidráulico ---
            Respuesta.objects.create(texto="Bajo", pregunta=p_hidraulico, siguiente_pregunta=p_hid_nivel)
            Respuesta.objects.create(texto="Medio", pregunta=p_hidraulico, siguiente_pregunta=p_hid_nivel)
            Respuesta.objects.create(texto="Alto", pregunta=p_hidraulico, siguiente_pregunta=p_hid_nivel)

            # Nivel -> revisar fuga o inspeccionar color
            Respuesta.objects.create(texto="Revisar fuga", pregunta=p_hid_nivel, siguiente_pregunta=p_hid_revisa_fuga)
            Respuesta.objects.create(texto="Inspeccionar color/estado", pregunta=p_hid_nivel, siguiente_pregunta=p_hid_inspeccion_color)

            # Fuga -> manchas rojas? limpiar/añadir
            Respuesta.objects.create(texto="Tiene manchas rojas", pregunta=p_hid_revisa_fuga, diagnostico_final="Limpia el área circundante y agrega líquido correcto hasta la marca.")
            Respuesta.objects.create(texto="No tiene manchas", pregunta=p_hid_revisa_fuga, diagnostico_final="Agregar líquido nuevo y cerrar la compuerta; programar revisión si persiste la pérdida.")

            # Inspección color/estado
            Respuesta.objects.create(texto="Está bien", pregunta=p_hid_inspeccion_color, diagnostico_final="Cerrar compuerta del líquido hidráulico y programar próxima revisión.")
            Respuesta.objects.create(texto="Tiene burbujas", pregunta=p_hid_inspeccion_color, diagnostico_final="Cambiar líquido hidráulico y purgar el sistema.")
            Respuesta.objects.create(texto="Tiene suciedad/contaminación", pregunta=p_hid_inspeccion_color, diagnostico_final="Programar cambio y limpieza del sistema hidráulico.")

            print("✅ Datos iniciales de diagnóstico ampliados creados correctamente.")
