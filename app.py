import streamlit as st

# ==============================================================================
# CONCESIONARIA ALFONSO - SISTEMA DE PRE-SELECCIÓN ONLINE (STREAMLIT)
# ==============================================================================

# 1. INICIALIZACIÓN DE LA ESTRUCTURA DE DATOS EN SESSION_STATE
if "catalogo_vehiculos" not in st.session_state:
    st.session_state.catalogo_vehiculos = [
        {
            "id": 1,
            "marca": "Toyota",
            "modelo": "Corolla",
            "anio": 2023,
            "precio": 24500,
            "tipo": "Sedan",
            "disponible": True,
            "imagen": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=600"
        },
        {
            "id": 2,
            "marca": "Ford",
            "modelo": "Mustang",
            "anio": 2024,
            "precio": 55000,
            "tipo": "Deportivo",
            "disponible": True,
            "imagen": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=600"
        },
        {
            "id": 3,
            "marca": "Chevrolet",
            "modelo": "Tracker",
            "anio": 2023,
            "precio": 22000,
            "tipo": "SUV",
            "disponible": True,
            "imagen": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"
        },
        {
            "id": 4,
            "marca": "Volkswagen",
            "modelo": "Golf",
            "anio": 2022,
            "precio": 28000,
            "tipo": "Hatchback",
            "disponible": False,  # Simulación de auto reservado
            "imagen": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600"
        },
    ]

if "reservas_realizadas" not in st.session_state:
    st.session_state.reservas_realizadas = []


# 2. FUNCIONES (def) PARA LA LÓGICA DEL NEGOCIO
def mostrar_catalogo(lista_autos):
    """Recorre la lista de diccionarios y muestra los vehículos usando componentes de Streamlit."""
    if not lista_autos:
        st.warning("⚠️ No hay vehículos para mostrar en este momento.")
        return

    # Usamos columnas para que no se vea una lista infinita hacia abajo si hay muchos
    cols = st.columns(2) 
    
    for i, auto in enumerate(lista_autos):
        col = cols[i % 2]
        with col:
            # Requisito: Foto arriba de cada modelo
            st.image(auto["imagen"], use_container_width=True)
            
            estado = "✅ Disponible" if auto["disponible"] else "❌ RESERVADO"
            st.write(f"### {auto['marca']} {auto['modelo']}")
            st.write(f"**ID:** {auto['id']} | **Año:** {auto['anio']} | **Tipo:** {auto['tipo']}")
            st.write(f"**Precio:** US${auto['precio']}")
            st.write(f"**Estado:** {estado}")
            st.divider()


def filtrar_por_precio_maximo(lista_autos, precio_limite):
    """Filtra y retorna los autos con un precio menor o igual al ingresado."""
    resultados = []
    for auto in lista_autos:
        if auto["precio"] <= precio_limite and auto["disponible"]:
            resultados.append(auto)
    return resultados


def buscar_auto_por_id(lista_autos, auto_id):
    """Busca un diccionario en la lista según su ID único."""
    for auto in lista_autos:
        if auto["id"] == auto_id:
            return auto
    return None


def crear_reserva(auto, nombre_cliente, telefono):
    """Genera la confirmación de selección para ahorrar tiempo en el salón."""
    if not auto["disponible"]:
        return None

    # Cambiamos el estado dentro de la estructura de datos
    auto["disponible"] = False

    # Creamos un nuevo diccionario de reserva
    ticket = {
        "codigo_ticket": f"ALF-{auto['id']}0099",
        "cliente": nombre_cliente,
        "telefono": telefono,
        "vehiculo": f"{auto['marca']} {auto['modelo']} ({auto['anio']})",
        "precio_total": auto["precio"],
    }
    st.session_state.reservas_realizadas.append(ticket)
    return ticket


# 3. INTERFAZ PRINCIPAL DE STREAMLIT (Sustituye al bucle while)
def ejecutar_app():
    st.title("🚗 Concesionaria Alfonso")
    st.write("Ahorra tiempo seleccionando tu auto online antes de acudir al salón.")

    # Navegación en la barra lateral
    st.sidebar.title("--- MENÚ PRINCIPAL ---")
    opcion = st.sidebar.radio(
        "Navegación:",
        ["Ver catálogo completo", "Filtrar por presupuesto máximo", "Pre-seleccionar / Reservar auto", "Mis Reservas"]
    )

    # ---------------------------------------------------------
    # OPCIÓN 1: Ver catálogo completo
    # ---------------------------------------------------------
    if opcion == "Ver catálogo completo":
        st.header("Catálogo Disponible")
        mostrar_catalogo(st.session_state.catalogo_vehiculos)

    # ---------------------------------------------------------
    # OPCIÓN 2: Filtrar por presupuesto máximo
    # ---------------------------------------------------------
    elif opcion == "Filtrar por presupuesto máximo":
        st.header("Filtrar por Presupuesto")
        presupuesto = st.number_input("Ingrese su presupuesto máximo en USD:", min_value=0, step=1000)
        
        if st.button("Buscar"):
            filtrados = filtrar_por_precio_maximo(st.session_state.catalogo_vehiculos, presupuesto)
            if filtrados:
                st.success(f"Autos encontrados hasta US${presupuesto}:")
                mostrar_catalogo(filtrados)
            else:
                st.warning("⚠️ No se encontraron autos disponibles dentro de ese presupuesto.")

    # ---------------------------------------------------------
    # OPCIÓN 3: Pre-seleccionar / Reservar auto
    # ---------------------------------------------------------
    elif opcion == "Pre-seleccionar / Reservar auto":
        st.header("Pre-seleccionar / Reservar auto")
        
        # Mostramos el catálogo para que el usuario sepa qué ID elegir
        with st.expander("Ver Catálogo de Referencia", expanded=False):
            mostrar_catalogo(st.session_state.catalogo_vehiculos)

        st.subheader("Complete sus datos")
        # Usamos st.form para agrupar los inputs tal como se hacían secuencialmente en consola
        with st.form("reserva_form"):
            auto_id = st.number_input("Ingrese el ID del vehículo que desea elegir:", min_value=1, step=1)
            nombre = st.text_input("Ingrese su nombre y apellido:")
            telefono = st.text_input("Ingrese su número de teléfono:")
            
            submit = st.form_submit_button("Confirmar Pre-selección")

            if submit:
                auto_elegido = buscar_auto_por_id(st.session_state.catalogo_vehiculos, auto_id)

                if auto_elegido is None:
                    st.error("❌ El ID ingresado no existe.")
                elif not auto_elegido["disponible"]:
                    st.warning("⚠️ Este vehículo ya no se encuentra disponible para reserva.")
                elif not nombre or not telefono:
                    st.error("❌ Por favor, complete todos los campos de contacto.")
                else:
                    st.success(f"Ha elegido: {auto_elegido['marca']} {auto_elegido['modelo']} - US${auto_elegido['precio']}")
                    ticket = crear_reserva(auto_elegido, nombre, telefono)

                    if ticket:
                        st.success("¡PRE-SELECCIÓN CONFIRMADA!")
                        st.info(f"""
                        **Código de atención:** {ticket['codigo_ticket']}  
                        **Cliente:** {ticket['cliente']}  
                        **Auto asignado:** {ticket['vehiculo']}  
                        
                        *Presente este código en Concesionaria Alfonso para ser atendido de inmediato.*
                        """)
                        # Forzamos la recarga para que el catálogo global se actualice mostrando el auto como RESERVADO
                        st.rerun()

    # ---------------------------------------------------------
    # OPCIÓN 4: Mis Reservas (Extra para validar el session_state)
    # ---------------------------------------------------------
    elif opcion == "Mis Reservas":
        st.header("Reservas Realizadas en esta Sesión")
        if st.session_state.reservas_realizadas:
            # Como no podemos usar Pandas, mostramos la lista de diccionarios con st.table() nativo
            st.table(st.session_state.reservas_realizadas)
        else:
            st.info("Aún no has realizado ninguna reserva.")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    ejecutar_app()
