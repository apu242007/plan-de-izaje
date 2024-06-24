import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import math
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sqlite3  # Para almacenamiento de datos
import pandas as pd  # Para exportar a Excel
import threading  # Para multithreading
import logging  # Para logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlanDeIzajeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plan de Izaje")
        self.geometry("1200x1000")
        self.advertencia_resultado = ""
        self.create_widgets()

        # Conexión a la base de datos
        self.conn = sqlite3.connect('izaje.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Izaje (
                id INTEGER PRIMARY KEY,
                capacidad_nominal REAL,
                longitud_brazo REAL,
                altura_max_izaje REAL,
                peso_manipulador REAL,
                peso_contrapeso REAL,
                peso_carga REAL,
                longitud_carga REAL,
                anchura_carga REAL,
                altura_carga REAL,
                centro_gravedad REAL,
                terreno TEXT,
                distancia_obstaculo REAL,
                altura_obstaculo REAL,
                velocidad_viento REAL,
                direccion_viento REAL,
                temperatura_ambiente REAL,
                experiencia_operador REAL,
                estado_equipo TEXT,
                resultado TEXT
            )
        ''')
        self.conn.commit()

    def save_to_db(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Izaje (
                capacidad_nominal, longitud_brazo, altura_max_izaje, peso_manipulador, peso_contrapeso, 
                peso_carga, longitud_carga, anchura_carga, altura_carga, centro_gravedad, terreno, 
                distancia_obstaculo, altura_obstaculo, velocidad_viento, direccion_viento, 
                temperatura_ambiente, experiencia_operador, estado_equipo, resultado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.02, anchor=tk.N)

        # Sección 1: Características del manipulador telescópico
        tk.Label(frame, text="Capacidad de carga nominal (toneladas):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.capacidad_nominal = ttk.Combobox(frame, values=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300], width=8)
        self.capacidad_nominal.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Longitud del brazo telescópico (metros):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.longitud_brazo = ttk.Combobox(frame, values=[10, 20, 30, 40, 50, 60], width=8)
        self.longitud_brazo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Altura máxima de izaje (metros):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)
        self.altura_max_izaje = ttk.Combobox(frame, values=[10, 20, 30, 40, 50, 60], width=8)
        self.altura_max_izaje.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame, text="Peso del manipulador telescópico (toneladas):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.peso_manipulador = ttk.Combobox(frame, values=[10, 20, 30, 40, 50, 60], width=8)
        self.peso_manipulador.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Peso del contrapeso (toneladas):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.peso_contrapeso = ttk.Combobox(frame, values=[1, 2, 3, 4, 5], width=8)
        self.peso_contrapeso.grid(row=1, column=3, padx=5, pady=5)

        # Sección 2: Características de la carga
        tk.Label(frame, text="Peso de la carga (toneladas):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.peso_carga = tk.Entry(frame, width=10)
        self.peso_carga.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Longitud de la carga (metros):").grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        self.longitud_carga = tk.Entry(frame, width=10)
        self.longitud_carga.grid(row=2, column=3, padx=5, pady=5)

        tk.Label(frame, text="Anchura de la carga (metros):").grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)
        self.anchura_carga = tk.Entry(frame, width=10)
        self.anchura_carga.grid(row=2, column=5, padx=5, pady=5)

        tk.Label(frame, text="Altura de la carga (metros):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.altura_carga = tk.Entry(frame, width=10)
        self.altura_carga.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Centro de gravedad de la carga (metros):").grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)
        self.centro_gravedad = tk.Entry(frame, width=10)
        self.centro_gravedad.grid(row=3, column=3, padx=5, pady=5)

        # Sección 3: Condiciones del sitio de izaje
        tk.Label(frame, text="Terreno:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.terreno = ttk.Combobox(frame, values=["nivelado", "desnivelado"], width=10)
        self.terreno.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Distancia al obstáculo más cercano (metros):").grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)
        self.distancia_obstaculo = tk.Entry(frame, width=10)
        self.distancia_obstaculo.grid(row=4, column=3, padx=5, pady=5)

        tk.Label(frame, text="Altura del obstáculo más cercano (metros):").grid(row=4, column=4, padx=5, pady=5, sticky=tk.E)
        self.altura_obstaculo = tk.Entry(frame, width=10)
        self.altura_obstaculo.grid(row=4, column=5, padx=5, pady=5)

        # Sección 4: Condiciones climáticas
        tk.Label(frame, text="Velocidad del viento (m/s):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.velocidad_viento = tk.Entry(frame, width=10)
        self.velocidad_viento.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame, text="Dirección del viento (grados):").grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)
        self.direccion_viento = tk.Entry(frame, width=10)
        self.direccion_viento.grid(row=5, column=3, padx=5, pady=5)

        tk.Label(frame, text="Temperatura ambiente (°C):").grid(row=5, column=4, padx=5, pady=5, sticky=tk.E)
        self.temperatura_ambiente = tk.Entry(frame, width=10)
        self.temperatura_ambiente.grid(row=5, column=5, padx=5, pady=5)

        # Sección 5: Operador y equipo
        tk.Label(frame, text="Experiencia del operador (años):").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.experiencia_operador = tk.Entry(frame, width=10)
        self.experiencia_operador.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(frame, text="Estado del equipo:").grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)
        self.estado_equipo = ttk.Combobox(frame, values=["ok", "mantenimiento"], width=10)
        self.estado_equipo.grid(row=6, column=3, padx=5, pady=5)

        # Botón para calcular
        self.calculate_button = tk.Button(frame, text="Calcular", command=self.calculate)
        self.calculate_button.grid(row=7, column=0, columnspan=6, padx=5, pady=10)

        # Área para los gráficos
        graph_frame = tk.Frame(self)
        graph_frame.place(relx=0.5, rely=0.35, anchor=tk.N)

        # Gráfico interactivo de Plotly
        self.plotly_widget = tk.Label(graph_frame, text="El gráfico se generará después de calcular")
        self.plotly_widget.pack()

        # Imagen estática
        self.figure_image = Image.open("grua_grafico.png")
        self.photo = ImageTk.PhotoImage(self.figure_image.resize((450, 250), Image.LANCZOS))
        self.image_label = tk.Label(graph_frame, image=self.photo)
        self.image_label.pack()

        # Botones para enviar por email y descargar PDF
        button_frame = tk.Frame(self)
        button_frame.place(relx=0.5, rely=0.8, anchor=tk.N)

        self.email_button = tk.Button(button_frame, text="Enviar por Email", command=self.send_email)
        self.email_button.grid(row=0, column=0, padx=5, pady=5)

        self.pdf_button = tk.Button(button_frame, text="Descargar PDF", command=self.download_pdf)
        self.pdf_button.grid(row=0, column=1, padx=5, pady=5)

        # Botón para exportar a Excel
        self.excel_button = tk.Button(button_frame, text="Exportar a Excel", command=self.export_to_excel)
        self.excel_button.grid(row=0, column=2, padx=5, pady=5)

    def calculate(self):
        try:
            # Verificar que todos los campos tengan valores
            if not all([self.capacidad_nominal.get(), self.longitud_brazo.get(), self.altura_max_izaje.get(), self.peso_manipulador.get(),
                        self.peso_contrapeso.get(), self.peso_carga.get(), self.longitud_carga.get(), self.anchura_carga.get(),
                        self.altura_carga.get(), self.centro_gravedad.get(), self.terreno.get(), self.distancia_obstaculo.get(),
                        self.altura_obstaculo.get(), self.velocidad_viento.get(), self.direccion_viento.get(),
                        self.temperatura_ambiente.get(), self.experiencia_operador.get(), self.estado_equipo.get()]):
                messagebox.showerror("Error", "Todos los campos deben tener valores.")
                return

            capacidad_nominal = float(self.capacidad_nominal.get())
            longitud_brazo = float(self.longitud_brazo.get())
            altura_max_izaje = float(self.altura_max_izaje.get())
            peso_manipulador = float(self.peso_manipulador.get())
            peso_contrapeso = float(self.peso_contrapeso.get())

            peso_carga = float(self.peso_carga.get())
            longitud_carga = float(self.longitud_carga.get())
            anchura_carga = float(self.anchura_carga.get())
            altura_carga = float(self.altura_carga.get())
            centro_gravedad = float(self.centro_gravedad.get())

            distancia_obstaculo = float(self.distancia_obstaculo.get())
            altura_obstaculo = float(self.altura_obstaculo.get())

            velocidad_viento = float(self.velocidad_viento.get())

            # Fórmulas de cálculo de la capacidad de izaje
            M = peso_carga * centro_gravedad
            M_permisible = capacidad_nominal * longitud_brazo
            alpha = math.asin(M / M_permisible)
            h = altura_max_izaje - (longitud_brazo * math.sin(alpha))
            d = distancia_obstaculo - (longitud_brazo * math.cos(alpha))

            # Fórmulas de cálculo de la estabilidad
            W_total = peso_carga + peso_manipulador + peso_contrapeso
            M_estabilidad = W_total * centro_gravedad
            FS_estabilidad = M_estabilidad / (W_total * altura_carga)  # Usamos altura_carga como altura del centro de gravedad

            # Fórmulas de cálculo de la capacidad de carga reducida
            V_permisible = 20  # Velocidad del viento permisible para grúas hasta 300 toneladas
            FRV = 1 - (velocidad_viento / V_permisible)
            CCR = capacidad_nominal * FRV

            # Generar gráfico interactivo con Plotly
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Gráfico de Izaje", "Esquema de Grúa"))

            # Gráfico de Izaje
            x = np.linspace(0, max(d, 5) + 5, 100)
            y = np.linspace(0, max(h, 5) + 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = np.sqrt(X**2 + Y**2)

            contour = go.Contour(
                z=Z,
                x=x,
                y=y,
                colorscale=['green', 'yellow', 'red'],
                contours=dict(
                    start=0,
                    end=max(d, 5) + 5,
                    size=(max(d, 5) + 5) / 3
                )
            )

            line = go.Scatter(
                x=[0, d],
                y=[0, h],
                mode='lines+markers',
                line=dict(color='black', width=2),
                marker=dict(size=10)
            )

            fig.add_trace(contour, row=1, col=1)
            fig.add_trace(line, row=1, col=1)

            fig.update_xaxes(title_text="Distancia al obstáculo (m)", row=1, col=1)
            fig.update_yaxes(title_text="Altura de izaje (m)", row=1, col=1)

            # Esquema de Grúa (usando un gráfico de dispersión simple como placeholder)
            fig.add_trace(go.Scatter(
                x=[0, d],
                y=[0, h],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Brazo de la grúa'
                ), row=1, col=2)

            fig.add_trace(go.Scatter(
                x=[d],
                y=[h],
                mode='markers',
                marker=dict(size=15, color='red'),
                name='Carga'
            ), row=1, col=2)

            fig.update_xaxes(title_text="Distancia (m)", row=1, col=2)
            fig.update_yaxes(title_text="Altura (m)", row=1, col=2)

            fig.update_layout(height=600, width=1000, title_text="Análisis de Izaje")

            # Guardar el gráfico como imagen PNG
            fig.write_image("izaje_plot.png")

            # Actualizar el widget con el nuevo gráfico
            self.plotly_widget.destroy()
            self.plotly_widget = tk.Label(self, text="Gráfico generado. Abra 'izaje_plot.png' para ver el gráfico.")
            self.plotly_widget.place(relx=0.5, rely=0.35, anchor=tk.N)

            if peso_carga > CCR:
                self.advertencia_resultado = (
                    f"La carga bruta excede la capacidad de la grúa. No se puede realizar el izaje.\n"
                    f"Fórmula: Capacidad de Carga Reducida (CCR) = Capacidad Nominal x (1 - (Velocidad del Viento / Velocidad del Viento Permisible))\n"
                    f"Resultado: {peso_carga} toneladas > {CCR:.2f} toneladas"
                )
                messagebox.showwarning("Advertencia", self.advertencia_resultado)
            else:
                self.advertencia_resultado = (
                    f"El izaje es seguro.\n"
                    f"Fórmula: Capacidad de Carga Reducida (CCR) = Capacidad Nominal x (1 - (Velocidad del Viento / Velocidad del Viento Permisible))\n"
                    f"Resultado: {peso_carga} toneladas <= {CCR:.2f} toneladas"
                )
                messagebox.showinfo("Información", self.advertencia_resultado)

            # Guardar datos en la base de datos
            self.save_to_db((
                capacidad_nominal, longitud_brazo, altura_max_izaje, peso_manipulador, peso_contrapeso,
                peso_carga, longitud_carga, anchura_carga, altura_carga, centro_gravedad, self.terreno.get(),
                distancia_obstaculo, altura_obstaculo, velocidad_viento, float(self.direccion_viento.get()),
                float(self.temperatura_ambiente.get()), float(self.experiencia_operador.get()), self.estado_equipo.get(),
                self.advertencia_resultado
            ))

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def send_email(self):
        def send_email_thread():
            sender_email = "tu_email@gmail.com"
            receiver_email = "destinatario_email@gmail.com"
            password = "tu_contraseña"

            subject = "Plan de Izaje"
            body = "Adjunto encontrará el plan de izaje en formato PDF."

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            pdfname = "plan_de_izaje.pdf"
            with open(pdfname, "rb") as pdf:
                part = MIMEApplication(pdf.read(), Name=pdfname)
            part['Content-Disposition'] = f'attachment; filename="{pdfname}"'
            msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()
                messagebox.showinfo("Información", "Correo enviado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {str(e)}")

        threading.Thread(target=send_email_thread).start()

    def download_pdf(self):
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Agregar título y espaciado
            pdf.cell(0, 10, txt="Plan de Izaje", ln=True, align='C')
            pdf.ln(10)
            
            # Agregar datos de entrada
            pdf.cell(0, 10, txt=f"Capacidad de carga nominal: {self.capacidad_nominal.get()} toneladas", ln=True)
            pdf.cell(0, 10, txt=f"Longitud del brazo telescópico: {self.longitud_brazo.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Altura máxima de izaje: {self.altura_max_izaje.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Peso del manipulador telescópico: {self.peso_manipulador.get()} toneladas", ln=True)
            pdf.cell(0, 10, txt=f"Peso del contrapeso: {self.peso_contrapeso.get()} toneladas", ln=True)
            pdf.cell(0, 10, txt=f"Peso de la carga: {self.peso_carga.get()} toneladas", ln=True)
            pdf.cell(0, 10, txt=f"Longitud de la carga: {self.longitud_carga.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Anchura de la carga: {self.anchura_carga.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Altura de la carga: {self.altura_carga.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Centro de gravedad de la carga: {self.centro_gravedad.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Terreno: {self.terreno.get()}", ln=True)
            pdf.cell(0, 10, txt=f"Distancia al obstáculo más cercano: {self.distancia_obstaculo.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Altura del obstáculo más cercano: {self.altura_obstaculo.get()} metros", ln=True)
            pdf.cell(0, 10, txt=f"Velocidad del viento: {self.velocidad_viento.get()} m/s", ln=True)
            pdf.cell(0, 10, txt=f"Dirección del viento: {self.direccion_viento.get()} grados", ln=True)
            pdf.cell(0, 10, txt=f"Temperatura ambiente: {self.temperatura_ambiente.get()} °C", ln=True)
            pdf.cell(0, 10, txt=f"Experiencia del operador: {self.experiencia_operador.get()} años", ln=True)
            pdf.cell(0, 10, txt=f"Estado del equipo: {self.estado_equipo.get()}", ln=True)
            pdf.ln(10)
            
            # Agregar resultados
            carga_bruta = float(self.peso_carga.get())
            
            pdf.cell(0, 10, txt=f"Carga Bruta: {carga_bruta} toneladas", ln=True)
            pdf.ln(10)
            
            # Agregar el resultado del cartel de advertencia
            pdf.multi_cell(0, 10, txt=f"Resultado del Cálculo:\n{self.advertencia_resultado}")
            pdf.ln(10)
            
            # Agregar la imagen del gráfico de Plotly
            pdf.image("izaje_plot.png", x=10, y=140, w=190)
            
            pdf.output("plan_de_izaje.pdf")
            messagebox.showinfo("Información", "Archivo PDF generado exitosamente.")
        except PermissionError:
            messagebox.showerror("Error", "No se pudo crear el archivo PDF. Asegúrese de que el archivo no esté abierto en otro programa.")

    def export_to_excel(self):
        try:
            # Recopilar datos en un DataFrame
            data = {
                'Capacidad Nominal (toneladas)': [self.capacidad_nominal.get()],
                'Longitud del Brazo (metros)': [self.longitud_brazo.get()],
                'Altura Máxima de Izaje (metros)': [self.altura_max_izaje.get()],
                'Peso del Manipulador (toneladas)': [self.peso_manipulador.get()],
                'Peso del Contrapeso (toneladas)': [self.peso_contrapeso.get()],
                'Peso de la Carga (toneladas)': [self.peso_carga.get()],
                'Longitud de la Carga (metros)': [self.longitud_carga.get()],
                'Anchura de la Carga (metros)': [self.anchura_carga.get()],
                'Altura de la Carga (metros)': [self.altura_carga.get()],
                'Centro de Gravedad (metros)': [self.centro_gravedad.get()],
                'Terreno': [self.terreno.get()],
                'Distancia al Obstáculo (metros)': [self.distancia_obstaculo.get()],
                'Altura del Obstáculo (metros)': [self.altura_obstaculo.get()],
                'Velocidad del Viento (m/s)': [self.velocidad_viento.get()],
                'Dirección del Viento (grados)': [self.direccion_viento.get()],
                'Temperatura Ambiente (°C)': [self.temperatura_ambiente.get()],
                'Experiencia del Operador (años)': [self.experiencia_operador.get()],
                'Estado del Equipo': [self.estado_equipo.get()],
                'Resultado': [self.advertencia_resultado]
            }
            
            df = pd.DataFrame(data)
            
            # Guardar el DataFrame en un archivo Excel
            df.to_excel('plan_de_izaje.xlsx', index=False)
            messagebox.showinfo("Información", "Datos exportados a Excel exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel. Error: {str(e)}")

if __name__ == "__main__":
    app = PlanDeIzajeApp()
    app.mainloop()
