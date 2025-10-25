from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pregunta, Respuesta


@receiver(post_migrate)
def crear_datos_iniciales(sender, **kwargs):
    if sender.name == 'diagnostico':
        if not Pregunta.objects.exists():
            # Raíz del flujo de mantenimiento e inspección
            root = Pregunta.objects.create(texto="Mantenimiento e inspección", is_root=True)

            # Preguntas iniciales sobre el vehículo
            p_edad = Pregunta.objects.create(texto="¿Cuántos años tiene el vehículo?", pregunta_padre=root)
            p_kilometraje = Pregunta.objects.create(texto="¿Cuál es el kilometraje actual del vehículo?", pregunta_padre=root)

            # Categorías principales de mantenimiento
            p_liquidos = Pregunta.objects.create(texto="Mantenimiento de líquidos", pregunta_padre=root)
            p_componentes = Pregunta.objects.create(texto="Mantenimiento de componentes", pregunta_padre=root)
            p_inspeccion = Pregunta.objects.create(texto="Inspección visual", pregunta_padre=root)

            # Componentes mecánicos
            p_rodamiento = Pregunta.objects.create(texto="Rodamientos", pregunta_padre=p_componentes)
            p_filtro_aire = Pregunta.objects.create(texto="Filtro de aire", pregunta_padre=p_componentes)
            p_bujias = Pregunta.objects.create(texto="Bujías", pregunta_padre=p_componentes)
            p_llantas = Pregunta.objects.create(texto="Llantas", pregunta_padre=p_componentes)

            # Inspección visual
            p_mangueras = Pregunta.objects.create(texto="Revisión de mangueras", pregunta_padre=p_inspeccion)
            p_correas = Pregunta.objects.create(texto="Revisión de correas", pregunta_padre=p_inspeccion)
            
            # Tipos de líquido como subpreguntas
            p_lubricante = Pregunta.objects.create(texto="Aceite del motor", pregunta_padre=p_liquidos)
            p_aceite_caja = Pregunta.objects.create(texto="Aceite de la caja", pregunta_padre=p_liquidos)
            p_frenos = Pregunta.objects.create(texto="Líquido de frenos", pregunta_padre=p_liquidos)
            p_hidraulico = Pregunta.objects.create(texto="Líquido hidráulico de dirección", pregunta_padre=p_liquidos)

            # --- ACEITE MOTOR ---
            p_lub_km = Pregunta.objects.create(texto="¿Ha excedido el kilometraje recomendado para cambio de aceite?", pregunta_padre=p_lubricante)
            p_lub_inspeccion = Pregunta.objects.create(texto="¿Color del aceite en la varilla?", pregunta_padre=p_lub_km)
            
            # --- ACEITE CAJA ---
            p_caja_inspeccion = Pregunta.objects.create(texto="¿Estado del aceite de la caja?", pregunta_padre=p_aceite_caja)
            
            # --- LÍQUIDO DE FRENOS ---
            p_frenos_inspeccion = Pregunta.objects.create(texto="¿Estado del líquido de frenos?", pregunta_padre=p_frenos)
            p_frenos_edad = Pregunta.objects.create(texto="¿Hace más de 5 años del último cambio?", pregunta_padre=p_frenos)
            
            # --- HIDRÁULICO DIRECCIÓN ---
            p_hid_nivel = Pregunta.objects.create(texto="¿Nivel del líquido hidráulico?", pregunta_padre=p_hidraulico)
            p_hid_inspeccion = Pregunta.objects.create(texto="¿Estado del líquido hidráulico?", pregunta_padre=p_hid_nivel)
            
            # --- RODAMIENTOS ---
            p_rod_km = Pregunta.objects.create(texto="¿Kilometraje desde último cambio de rodamientos?", pregunta_padre=p_rodamiento)
            
            # --- FILTRO DE AIRE ---
            p_filtro_km = Pregunta.objects.create(texto="¿Kilometraje desde último cambio de filtro?", pregunta_padre=p_filtro_aire)
            p_filtro_inspeccion = Pregunta.objects.create(texto="¿Estado del filtro de aire?", pregunta_padre=p_filtro_aire)
            
            # --- BUJÍAS ---
            p_bujias_edad = Pregunta.objects.create(texto="¿Hace cuántos años se cambiaron las bujías?", pregunta_padre=p_bujias)
            p_bujias_km = Pregunta.objects.create(texto="¿Kilometraje desde último cambio de bujías?", pregunta_padre=p_bujias)
            
            # --- LLANTAS ---
            p_llantas_profundidad = Pregunta.objects.create(texto="¿Profundidad del grabado de las llantas?", pregunta_padre=p_llantas)
            p_llantas_estado = Pregunta.objects.create(texto="¿Estado general de las llantas?", pregunta_padre=p_llantas)
            
            # --- MANGUERAS ---
            p_mangueras_estado = Pregunta.objects.create(texto="¿Estado de las mangueras?", pregunta_padre=p_mangueras)
            
            # --- CORREAS ---
            p_correas_estado = Pregunta.objects.create(texto="¿Estado de las correas?", pregunta_padre=p_correas)

            # Respuestas para edad del vehículo
            Respuesta.objects.create(texto="Menos de 5 años", pregunta=p_edad, siguiente_pregunta=p_kilometraje)
            Respuesta.objects.create(texto="Entre 5 y 10 años", pregunta=p_edad, siguiente_pregunta=p_kilometraje)
            Respuesta.objects.create(texto="Más de 10 años", pregunta=p_edad, siguiente_pregunta=p_kilometraje)

            # Respuestas para kilometraje
            Respuesta.objects.create(texto="Menos de 30,000 km", pregunta=p_kilometraje, diagnostico_final="Realizar mantenimiento básico según manual.")
            Respuesta.objects.create(texto="Entre 30,000 y 60,000 km", pregunta=p_kilometraje, diagnostico_final="Considerar revisión de rodamientos y componentes mayores.")
            Respuesta.objects.create(texto="Más de 60,000 km", pregunta=p_kilometraje, diagnostico_final="Programar revisión completa de componentes críticos.")

            # Respuestas raíz -> categorías
            Respuesta.objects.create(texto="Revisar líquidos", pregunta=root, siguiente_pregunta=p_liquidos)
            Respuesta.objects.create(texto="Revisar componentes", pregunta=root, siguiente_pregunta=p_componentes)
            Respuesta.objects.create(texto="Realizar inspección visual", pregunta=root, siguiente_pregunta=p_inspeccion)

            # Respuestas para las subcategorías de líquidos (para que al entrar en 'Mantenimiento de líquidos' haya opciones)
            Respuesta.objects.create(texto="Aceite del motor", pregunta=p_liquidos, siguiente_pregunta=p_lubricante)
            Respuesta.objects.create(texto="Aceite de la caja", pregunta=p_liquidos, siguiente_pregunta=p_aceite_caja)
            Respuesta.objects.create(texto="Líquido de frenos", pregunta=p_liquidos, siguiente_pregunta=p_frenos)
            Respuesta.objects.create(texto="Líquido hidráulico de dirección", pregunta=p_liquidos, siguiente_pregunta=p_hidraulico)

            # Respuestas para componentes (para que al entrar en 'Mantenimiento de componentes' haya opciones)
            Respuesta.objects.create(texto="Rodamientos", pregunta=p_componentes, siguiente_pregunta=p_rodamiento)
            Respuesta.objects.create(texto="Filtro de aire", pregunta=p_componentes, siguiente_pregunta=p_filtro_aire)
            Respuesta.objects.create(texto="Bujías", pregunta=p_componentes, siguiente_pregunta=p_bujias)
            Respuesta.objects.create(texto="Llantas", pregunta=p_componentes, siguiente_pregunta=p_llantas)

            # Respuestas para la inspección visual (para que al entrar en 'Inspección visual' haya opciones)
            Respuesta.objects.create(texto="Revisión de mangueras", pregunta=p_inspeccion, siguiente_pregunta=p_mangueras)
            Respuesta.objects.create(texto="Revisión de correas", pregunta=p_inspeccion, siguiente_pregunta=p_correas)

            # Enlazar cada subpregunta con sus propias opciones (para que las preguntas intermedias muestren respuestas)
            # Líquidos -> opciones internas
            Respuesta.objects.create(texto="Ver kilometraje/recomendación", pregunta=p_lubricante, siguiente_pregunta=p_lub_km)
            Respuesta.objects.create(texto="Inspeccionar aceite de caja", pregunta=p_aceite_caja, siguiente_pregunta=p_caja_inspeccion)
            Respuesta.objects.create(texto="Inspeccionar líquido de frenos", pregunta=p_frenos, siguiente_pregunta=p_frenos_inspeccion)
            Respuesta.objects.create(texto="Inspeccionar líquido hidráulico", pregunta=p_hidraulico, siguiente_pregunta=p_hid_nivel)

            # Componentes -> opciones internas
            Respuesta.objects.create(texto="Ver kilometraje rodamientos", pregunta=p_rodamiento, siguiente_pregunta=p_rod_km)
            Respuesta.objects.create(texto="Ver kilometraje filtro de aire", pregunta=p_filtro_aire, siguiente_pregunta=p_filtro_km)
            Respuesta.objects.create(texto="Ver estado de bujías", pregunta=p_bujias, siguiente_pregunta=p_bujias_edad)
            Respuesta.objects.create(texto="Ver profundidad de llantas", pregunta=p_llantas, siguiente_pregunta=p_llantas_profundidad)

            # Inspección visual -> opciones internas
            Respuesta.objects.create(texto="Inspección mangueras - estado", pregunta=p_mangueras, siguiente_pregunta=p_mangueras_estado)
            Respuesta.objects.create(texto="Inspección correas - estado", pregunta=p_correas, siguiente_pregunta=p_correas_estado)

            # --- Respuestas para aceite motor ---
            Respuesta.objects.create(texto="Sí, excedió kilometraje", pregunta=p_lub_km, diagnostico_final="Programar cambio de aceite inmediatamente.")
            Respuesta.objects.create(texto="No, dentro del rango", pregunta=p_lub_km, siguiente_pregunta=p_lub_inspeccion)

            Respuesta.objects.create(texto="Color turbio/oscuro", pregunta=p_lub_inspeccion, diagnostico_final="Cambiar aceite aunque no haya cumplido el kilometraje.")
            Respuesta.objects.create(texto="Color normal", pregunta=p_lub_inspeccion, diagnostico_final="Mantener monitoreo regular del nivel y color.")

            # --- Respuestas para aceite caja ---
            Respuesta.objects.create(texto="Turbio", pregunta=p_caja_inspeccion, diagnostico_final="Drenar y reemplazar el aceite de la caja.")
            Respuesta.objects.create(texto="Normal", pregunta=p_caja_inspeccion, diagnostico_final="Mantener nivel entre máximo y mínimo.")

            # --- Respuestas para líquido frenos ---
            Respuesta.objects.create(texto="Turbio", pregunta=p_frenos_inspeccion, diagnostico_final="Drenar y reemplazar el líquido de frenos.")
            Respuesta.objects.create(texto="Normal", pregunta=p_frenos_inspeccion, siguiente_pregunta=p_frenos_edad)

            Respuesta.objects.create(texto="Sí, más de 5 años", pregunta=p_frenos_edad, diagnostico_final="Reemplazar líquido de frenos por tiempo transcurrido.")
            Respuesta.objects.create(texto="No", pregunta=p_frenos_edad, diagnostico_final="Mantener nivel entre máximo y mínimo.")

            # --- Respuestas para hidráulico dirección ---
            Respuesta.objects.create(texto="Bajo", pregunta=p_hid_nivel, siguiente_pregunta=p_hid_inspeccion)
            Respuesta.objects.create(texto="Normal", pregunta=p_hid_nivel, diagnostico_final="Mantener nivel y monitorear regularmente.")

            Respuesta.objects.create(texto="Turbio", pregunta=p_hid_inspeccion, diagnostico_final="Drenar y reemplazar el líquido hidráulico.")
            Respuesta.objects.create(texto="Normal", pregunta=p_hid_inspeccion, diagnostico_final="Rellenar si es necesario y mantener monitoreo.")

            # --- Respuestas para rodamientos ---
            Respuesta.objects.create(texto="Más de 30,000 km", pregunta=p_rod_km, diagnostico_final="Programar revisión/cambio de rodamientos.")
            Respuesta.objects.create(texto="Menos de 30,000 km", pregunta=p_rod_km, diagnostico_final="Continuar monitoreo normal.")

            # --- Respuestas para filtro aire ---
            Respuesta.objects.create(texto="Kilometraje excedido", pregunta=p_filtro_km, diagnostico_final="Cambiar filtro de aire.")
            Respuesta.objects.create(texto="Dentro del rango", pregunta=p_filtro_km, siguiente_pregunta=p_filtro_inspeccion)

            Respuesta.objects.create(texto="Sucio", pregunta=p_filtro_inspeccion, diagnostico_final="Limpiar o reemplazar el filtro de aire.")
            Respuesta.objects.create(texto="Limpio", pregunta=p_filtro_inspeccion, diagnostico_final="Mantener monitoreo regular.")

            # --- Respuestas para bujías ---
            Respuesta.objects.create(texto="Más de 5 años", pregunta=p_bujias_edad, diagnostico_final="Programar cambio de bujías por tiempo.")
            Respuesta.objects.create(texto="Menos de 5 años", pregunta=p_bujias_edad, siguiente_pregunta=p_bujias_km)

            Respuesta.objects.create(texto="Kilometraje excedido", pregunta=p_bujias_km, diagnostico_final="Programar cambio de bujías por kilometraje.")
            Respuesta.objects.create(texto="Dentro del rango", pregunta=p_bujias_km, diagnostico_final="Continuar monitoreo normal.")

            # --- Respuestas para llantas ---
            Respuesta.objects.create(texto="Profundidad insuficiente", pregunta=p_llantas_profundidad, diagnostico_final="Programar cambio de llantas.")
            Respuesta.objects.create(texto="Profundidad adecuada", pregunta=p_llantas_profundidad, siguiente_pregunta=p_llantas_estado)

            Respuesta.objects.create(texto="Desgaste irregular/daños", pregunta=p_llantas_estado, diagnostico_final="Revisar alineación y cambiar llantas si es necesario.")
            Respuesta.objects.create(texto="Estado normal", pregunta=p_llantas_estado, diagnostico_final="Continuar monitoreo regular.")

            # --- Respuestas para mangueras ---
            Respuesta.objects.create(texto="Grietas o daños", pregunta=p_mangueras_estado, diagnostico_final="Reemplazar mangueras dañadas.")
            Respuesta.objects.create(texto="Estado normal", pregunta=p_mangueras_estado, diagnostico_final="Continuar inspección regular.")

            # --- Respuestas para correas ---
            Respuesta.objects.create(texto="Grietas o desgaste", pregunta=p_correas_estado, diagnostico_final="Programar cambio de correas.")
            Respuesta.objects.create(texto="Estado normal", pregunta=p_correas_estado, diagnostico_final="Continuar monitoreo regular.")

            print("✅ Datos iniciales de diagnóstico ampliados creados correctamente.")
