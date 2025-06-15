# 🧊 Detector de Carteras Inactivas en Bitcoin

## Descripción  
Este proyecto ofrece una herramienta completa para identificar carteras de Bitcoin que llevan tiempo sin gastar sus fondos. Consta de dos componentes principales:

1. **Backend en Python**  
   - Interroga la API pública de Blockchain.com para obtener el historial de transacciones de cada dirección.  
   - Calcula la fecha del último gasto y compara con un umbral configurable (X años) para marcar direcciones como “inactivas”.  
   - Permite procesar listados extensos en modo batch sin depender de servicios de pago ni de APIs con límites estrictos.  

2. **Interfaz Web con Streamlit**  
   - Panel lateral para cargar un archivo `.txt` o introducir manualmente direcciones Bitcoin.  
   - Control deslizante para ajustar el umbral de inactividad (en años).  
   - Resumen de métricas clave (total de carteras, inactivas, nunca usadas).  
   - Tabla interactiva y filtrable con estado, balance, fechas y colores que distinguen carteras activas, inactivas y nunca usadas.  
   - Exportación a CSV y sección especial que resalta carteras inactivas con saldo positivo.  

Gracias a su dependencia exclusiva de datos públicos y de tecnologías de código abierto, la herramienta es completamente reproducible y transparente. Su diseño moderno (tipografía futurista, efectos de cristal esmerilado y paleta de colores diferenciadora) asegura una experiencia de usuario intuitiva y profesional.

---

## Características  
- Detección automatizada de carteras inactivas  
- Análisis masivo en modo batch  
- Umbral de inactividad configurable  
- Interfaz gráfica sin necesidad de conocimientos de programación  
- Tabla interactiva y filtrable con código de colores  
- Descarga de resultados en CSV  
- Diseño responsive y estilizado

---

## Requisitos  
- Python 3.8+  
- [Streamlit](https://streamlit.io/)  
- `requests`  
- `pandas`  

---

## Instalación  

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/tu-usuario/detector-wallets-inactivas.git
   cd detector-wallets-inactivas
   ```

2. Crea y activa un entorno virtual:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

3. Instala las dependencias:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso  

1. Inicia la aplicación Streamlit:  
   ```bash
   streamlit run app.py
   ```

2. En tu navegador, abre `http://localhost:8501`.  
3. En el panel lateral:
   - Carga un archivo `.txt` con una dirección Bitcoin por línea, o pégalas en el área de texto.
   - Ajusta el control deslizante para seleccionar los años mínimos de inactividad.
4. Haz clic en **🔍 Analizar direcciones**.  
5. Consulta el resumen de métricas, explora la tabla interactiva y descarga los resultados en CSV.

---

## Configuración  

- **Umbral de inactividad**: ajustable entre 1 y 15 años desde el control deslizante.  
- **Rate limits**: si la API de Blockchain.com devuelve HTTP 429, la app mostrará un mensaje de espera y pausará nuevas solicitudes hasta que expire el período indicado en el header `Retry-After`.

---

## Ejemplo de archivo `.txt`  
```
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
1BoatSLRHtKNngkdXEeobR76b53LETtpyT
bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq
```

---

## Contribuir  
1. Haz “fork” del repositorio.  
2. Crea una rama de feature: `git checkout -b feature/nueva-funcionalidad`.  
3. Realiza tus cambios y haz commit: `git commit -m "Agrega nueva funcionalidad"`.  
4. Envía un pull request describiendo tu aporte.

---

## Licencia  
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## Agradecimientos  
- [Blockchain.com](https://blockchain.com/) por proporcionar la API pública.  
- [Streamlit](https://streamlit.io/) por su framework de desarrollo rápido de aplicaciones web.  
- Iconografía y tipografía inspiradas en diseños futuristas para mejorar la UX.
