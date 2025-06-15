import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import time

# Configuración de la página
st.set_page_config(
    page_title="Detector de Wallets Inactivas en Bitcoin",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600&display=swap');
            
.header {
    font-family: 'Orbitron', sans-serif;
    color: #4FC3F7;
    text-shadow: 0 0 10px rgba(79, 195, 247, 0.7);
    font-size: 46px !important;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background-color: rgba(10, 23, 55, 0.7) !important;
    border-radius: 15px !important;
    padding: 25px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.4);
    backdrop-filter: blur(5px);
    border: 1px solid #2d4d7d;
    margin-bottom: 25px;
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #0a1737 !important;
    color: white !important;
    border: 1px solid #2d4d7d !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

.stButton>button {
    background: linear-gradient(45deg, #29B6F6, #4FC3F7) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: bold !important;
    font-size: 18px !important;
    transition: all 0.4s ease !important;
    width: 100%;
    margin-top: 15px;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(79, 195, 247, 0.6);
}

.frosted {
    background-color: rgba(10, 23, 55, 0.7) !important;
    backdrop-filter: blur(5px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.dataframe {
    background-color: rgba(10, 23, 55, 0.7) !important;
    color: white !important;
    border: 1px solid #2d4d7d !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #29B6F6, #4FC3F7);
}

.inactive {
    background-color: rgba(255, 110, 110, 0.2) !important;
}

.active {
    background-color: rgba(165, 214, 167, 0.2) !important;
}

.never-used {
    background-color: rgba(179, 157, 219, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# Cabecera con efecto especial
st.markdown('<p class="header">🧊 Detector de Carteras Inactivas en Bitcoin</p>', unsafe_allow_html=True)
st.caption("#### Analiza direcciones de Bitcoin para comprobar si han estado inactivas durante un número de años especificado")

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png", width=100)
    st.title("Configuración")
    st.info("Esta aplicación utiliza la API pública de Blockchain.com para obtener datos de transacciones en tiempo real.")
    st.divider()
    
    # Ejemplos de wallets
    st.caption("💡 Ejemplos de wallets para probar:")
    st.code("1HQ3Go3ggs8pFnXuHVHRytPCq5fGG8Hbhx")  
    st.code("1BoatSLRHtKNngkdXEeobR76b53LETtpyT")    
    st.code("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")  
    
    st.divider()
    st.caption("ℹ️ Una wallet se considera inactiva si no ha enviado BTC en el período seleccionado")
    st.caption("⚠️ Las transacciones de recepción no afectan la inactividad")

# Funciones principales
import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import time

# ... (el resto del código CSS y configuración permanece igual)

# Funciones principales
def obtener_datos_wallet(direccion):
    """Obtiene todos los datos de la wallet de Blockchain.com con manejo de rate limits"""
    url = f"https://blockchain.info/rawaddr/{direccion}?limit=200"
    
    # Verificar si estamos en período de espera
    if 'rate_limit_reset' in st.session_state and st.session_state.rate_limit_reset > time.time():
        reset_time = st.session_state.rate_limit_reset
        wait_seconds = int(reset_time - time.time())
        wait_time = str(timedelta(seconds=wait_seconds))
        st.error(f"⏱️ Demasiadas solicitudes. Por favor, espera {wait_time} antes de intentar de nuevo.")
        return None

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 429:
            # Calcular tiempo de espera (1 minuto por defecto)
            wait_seconds = 60
            reset_time = time.time() + wait_seconds
            
            # Intentar obtener Retry-After del header si existe
            if 'Retry-After' in response.headers:
                try:
                    wait_seconds = int(response.headers['Retry-After'])
                    reset_time = time.time() + wait_seconds
                except ValueError:
                    pass
            
            # Guardar en sesión el tiempo de reset
            st.session_state.rate_limit_reset = reset_time
            wait_time = str(timedelta(seconds=wait_seconds))
            
            st.error(f"⏱️ Demasiadas solicitudes. Por favor, inténtalo de nuevo en {wait_time}.")
            return None
        
        else:
            st.warning(f"⚠️ Error al obtener datos para {direccion}: Código {response.status_code}")
            return None
            
    except Exception as e:
        st.warning(f"⚠️ Error de conexión para {direccion}: {str(e)}")
        return None



def obtener_fecha_ultimo_gasto(wallet_data, direccion):
    """Obtiene la fecha de la última transacción de salida (cuando la wallet gastó BTC)"""
    if not wallet_data or 'txs' not in wallet_data:
        return None
    
    # Buscar la última transacción donde esta dirección fue INPUT (gastó fondos)
    for tx in wallet_data['txs']:
        for inp in tx.get('inputs', []):
            if 'prev_out' in inp and inp['prev_out'].get('addr') == direccion:
                return datetime.fromtimestamp(tx['time'])
    
    # Si no se encontró ninguna transacción de salida
    return None

def analizar_wallets(wallets, años):
    """Analiza una lista de wallets y devuelve un DataFrame con los resultados"""
    cutoff = datetime.utcnow() - timedelta(days=años * 365)
    datos = []
    
    # Barra de progreso
    progress_bar = st.progress(0)
    total_wallets = len(wallets)
    
    for i, w in enumerate(wallets):
        # Actualizar barra de progreso
        progress = (i + 1) / total_wallets
        progress_bar.progress(progress)
        
        # Obtener información de la wallet
        wallet_data = obtener_datos_wallet(w)
        
        # Obtener fechas importantes
        fecha_creacion = None
        fecha_ultimo_gasto = None
        
        if wallet_data:
            # Obtener fecha de creación (primera transacción)
            if wallet_data.get('txs'):
                fecha_creacion = datetime.fromtimestamp(wallet_data['txs'][-1]['time'])
            
            # Obtener fecha del último gasto
            fecha_ultimo_gasto = obtener_fecha_ultimo_gasto(wallet_data, w)
        
        # Determinar estado
        if not wallet_data or not wallet_data.get('txs'):
            estado = "🔵 SIN ACTIVIDAD"
            inactivo_desde = "N/A"
            años_inactividad = "N/A"
            es_inactiva = False
            nunca_usada = True
        elif fecha_ultimo_gasto is None:
            # Wallet que nunca ha gastado
            años_inactividad = (datetime.utcnow() - fecha_creacion).days // 365
            estado = f"🟣 NUNCA USADA (creada hace {años_inactividad} años)"
            inactivo_desde = "Nunca"
            es_inactiva = fecha_creacion < cutoff if fecha_creacion else False
            nunca_usada = True
        elif fecha_ultimo_gasto < cutoff:
            # Wallet inactiva
            años_inactividad = (datetime.utcnow() - fecha_ultimo_gasto).days // 365
            estado = f"🔴 INACTIVA (hace {años_inactividad} años)"
            inactivo_desde = fecha_ultimo_gasto.date()
            es_inactiva = True
            nunca_usada = False
        else:
            # Wallet activa
            años_inactividad = (datetime.utcnow() - fecha_ultimo_gasto).days // 365
            estado = f"🟢 ACTIVA (hace {años_inactividad} años)"
            inactivo_desde = fecha_ultimo_gasto.date()
            es_inactiva = False
            nunca_usada = False
        
        # Obtener información adicional
        balance = wallet_data.get('final_balance', 0) / 100000000 if wallet_data else 0
        total_recibido = wallet_data.get('total_received', 0) / 100000000 if wallet_data else 0
        total_transacciones = wallet_data.get('n_tx', 0) if wallet_data else 0
        
        datos.append({
            "Dirección": w, 
            "Balance (BTC)": f"{balance:.8f}",
            "Total Recibido (BTC)": f"{total_recibido:.8f}",
            "Transacciones": total_transacciones,
            "Creación": fecha_creacion.date() if fecha_creacion else "N/A",
            "Último gasto": inactivo_desde,
            "Años inactividad": años_inactividad,
            "Estado": estado,
            "Es Inactiva": es_inactiva,
            "Nunca Usada": nunca_usada
        })
    
    return pd.DataFrame(datos)

# Contenedor principal
with st.container():
    # Sección de configuración
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            años_inactivos = st.slider(
                "**Selecciona años mínimos de inactividad**", 
                min_value=1, 
                max_value=15, 
                value=5,
                help="Una wallet se considera inactiva si no ha enviado BTC en este período"
            )
            
            archivo = st.file_uploader(
                "**O sube un archivo .txt**", 
                type=["txt"],
                help="Archivo con una dirección Bitcoin por línea"
            )
        
        with col2:
            direcciones_input = st.text_area(
                "**Introduce direcciones de Bitcoin (una por línea)**",
                placeholder="Ejemplo:\n1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
                height=150
            )
    
    # Procesar direcciones
    direcciones = []
    if archivo:
        direcciones = archivo.read().decode("utf-8").splitlines()
    elif direcciones_input:
        direcciones = direcciones_input.strip().splitlines()
    
    # Eliminar direcciones vacías
    direcciones = [d.strip() for d in direcciones if d.strip()]
    
    # Botón de análisis
    if st.button("🔍 Analizar direcciones", use_container_width=True):
        if not direcciones:
            st.warning("⚠️ Debes ingresar al menos una dirección o subir un archivo.")
        else:
            with st.spinner(f"Analizando {len(direcciones)} wallets en la blockchain. Esto puede tardar unos minutos..."):
                resultado = analizar_wallets(direcciones, años_inactivos)
                
                # Obtener estadísticas
                total_inactivas = resultado['Es Inactiva'].sum()
                total_nunca_usadas = resultado['Nunca Usada'].sum()
                
                # Mostrar resumen
                with st.container():
                    st.success(f"✅ Análisis completado: {total_inactivas} wallets inactivas y {total_nunca_usadas} nunca usadas")
                    
                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res1.metric("Total Wallets", len(direcciones))
                    col_res2.metric("Wallets Inactivas", total_inactivas)
                    col_res3.metric("Wallets Nunca Usadas", total_nunca_usadas)
                
                # Mostrar resultados en tabla
                st.subheader("Resultados Detallados")
                
                # Función para aplicar estilos según el estado
                def color_row(row):
                    if 'INACTIVA' in row['Estado']:
                        return ['background-color: rgba(255, 110, 110, 0.2)'] * len(row)
                    elif 'ACTIVA' in row['Estado']:
                        return ['background-color: rgba(165, 214, 167, 0.2)'] * len(row)
                    elif 'NUNCA USADA' in row['Estado']:
                        return ['background-color: rgba(179, 157, 219, 0.2)'] * len(row)
                    else:
                        return [''] * len(row)
                
                styled_df = resultado.drop(columns=['Es Inactiva', 'Nunca Usada']).style.apply(color_row, axis=1)
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=min(400, 45 * len(direcciones)))
                
                # Descargar resultados
                csv = resultado.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Descargar resultados en CSV", 
                    csv, 
                    f"wallets_inactivas_{años_inactivos}_años.csv", 
                    "text/csv",
                    use_container_width=True
                )
                
                # Mostrar detalles de wallets inactivas
                if total_inactivas > 0:
                    st.subheader("💎 Wallets Inactivas con Balance")
                    inactivas_con_balance = resultado[
                        (resultado['Es Inactiva']) & 
                        (pd.to_numeric(resultado['Balance (BTC)'].str.replace(' BTC', '')) > 0)
                    ]
                    
                    if not inactivas_con_balance.empty:
                        st.dataframe(
                            inactivas_con_balance.drop(columns=['Es Inactiva', 'Nunca Usada']),
                            use_container_width=True
                        )
                    else:
                        st.info("No se encontraron wallets inactivas con balance positivo")

# Pie de página
st.divider()
st.caption("Datos proporcionados por blockchain.com API")