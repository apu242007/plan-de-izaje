import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class PlanDeIzajeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plan de Izaje")
        self.geometry("1200x900")
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Cargar la imagen del manipulador
        self.image_grua = Image.open("grua.png")
        self.image_grua = self.image_grua.resize((300, 200), Image.LANCZOS)  # Redimensionar si es necesario
        self.photo_grua = ImageTk.PhotoImage(self.image_grua)

        # Mostrar la imagen del manipulador en un Label
        image_label_grua = tk.Label(frame, image=self.photo_grua)
        image_label_grua.grid(row=0, column=0, columnspan=2, pady=10)

        # Sección de entrada de datos
        tk.Label(frame, text="Radio inicial (m):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.radio_inicial = tk.Entry(frame)
        self.radio_inicial.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Peso del gancho (kg):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.peso_gancho = tk.Entry(frame)
        self.peso_gancho.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Peso de la herramienta (kg):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.peso_herramienta = tk.Entry(frame)
        self.peso_herramienta.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Peso de la carga (kg):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.peso_carga = tk.Entry(frame)
        self.peso_carga.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Otros pesos (kg):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.otros_pesos = tk.Entry(frame)
        self.otros_pesos.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame, text="Velocidad del viento (km/h):").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.velocidad_viento = tk.Entry(frame)
        self.velocidad_viento.grid(row=6, column=1, padx=5, pady=5)

        # Botón para calcular
        self.calculate_button = tk.Button(frame, text="Calcular", command=self.calculate)
        self.calculate_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

        # Cargar la imagen de la tabla
        self.image_tabla = Image.open("tabla manipulador.png")
        self.image_tabla = self.image_tabla.resize((700, 300), Image.LANCZOS)  # Redimensionar si es necesario
        self.photo_tabla = ImageTk.PhotoImage(self.image_tabla)

        # Mostrar la imagen de la tabla en un Label
        image_label_tabla = tk.Label(frame, image=self.photo_tabla)
        image_label_tabla.grid(row=8, column=0, columnspan=2, pady=10)

        # Botones para enviar por email y descargar PDF
        self.email_button = tk.Button(frame, text="Enviar por Email", command=self.send_email)
        self.email_button.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)

        self.pdf_button = tk.Button(frame, text="Descargar PDF", command=self.download_pdf)
        self.pdf_button.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

    def calculate(self):
        try:
            radio_inicial = float(self.radio_inicial.get())
            velocidad_viento = float(self.velocidad_viento.get())

            if velocidad_viento > 50:
                messagebox.showwarning("Advertencia", "La velocidad del viento es demasiado alta para realizar el izaje.")
                return

            peso_gancho = float(self.peso_gancho.get())
            peso_herramienta = float(self.peso_herramienta.get())
            peso_carga = float(self.peso_carga.get())
            otros_pesos = float(self.otros_pesos.get())

            carga_bruta = peso_gancho + peso_herramienta + peso_carga + otros_pesos
            capacidad_bruta_menor = self.obtener_capacidad_por_radio(radio_inicial)

            if carga_bruta > capacidad_bruta_menor:
                messagebox.showwarning("Advertencia", "La carga bruta excede la capacidad de la grúa. No se puede realizar el izaje.")
            else:
                messagebox.showinfo("Información", "El izaje es seguro.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def obtener_capacidad_por_radio(self, radio):
        # Aquí deberías implementar la lógica para obtener la capacidad según el radio y la tabla proporcionada
        # Este es un ejemplo simplificado:
        capacidad_por_radio = {
            3: 30000,
            3.5: 25650,
            4: 22775,
            4.5: 19850,
            5: 17875,
            6: 14250,
            7: 11500,
            8: 10300,
            9: 8750,
            10: 7530
        }
        return capacidad_por_radio.get(radio, 0)

    def send_email(self):
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

    def download_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Plan de Izaje", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Radio Inicial: {self.radio_inicial.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Peso del Gancho: {self.peso_gancho.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Peso de la Herramienta: {self.peso_herramienta.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Peso de la Carga: {self.peso_carga.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Otros Pesos: {self.otros_pesos.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Carga Bruta: {self.radio_inicial.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Capacidad Bruta Menor: {self.obtener_capacidad_por_radio(float(self.radio_inicial.get()))}", ln=True)
        pdf.cell(200, 10, txt=f"Velocidad del Viento: {self.velocidad_viento.get()} km/h", ln=True)
        pdf.output("plan_de_izaje.pdf")
        messagebox.showinfo("Información", "Archivo PDF generado exitosamente.")

if __name__ == "__main__":
    app = PlanDeIzajeApp()
    app.mainloop()

