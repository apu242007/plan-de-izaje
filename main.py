import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class PlanDeIzajeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plan de Izaje")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Sección de entrada de datos
        tk.Label(self, text="Radio inicial (m):").grid(row=0, column=0)
        self.radio_inicial = tk.Entry(self)
        self.radio_inicial.grid(row=0, column=1)

        tk.Label(self, text="Longitud inicial (m):").grid(row=1, column=0)
        self.longitud_inicial = tk.Entry(self)
        self.longitud_inicial.grid(row=1, column=1)

        tk.Label(self, text="Capacidad inicial (kg):").grid(row=2, column=0)
        self.capacidad_inicial = tk.Entry(self)
        self.capacidad_inicial.grid(row=2, column=1)

        # Botón para calcular
        self.calculate_button = tk.Button(self, text="Calcular", command=self.calculate)
        self.calculate_button.grid(row=3, column=0, columnspan=2)

        # Sección para mostrar resultados
        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2)

        # Botones para enviar por email y descargar PDF
        self.email_button = tk.Button(self, text="Enviar por Email", command=self.send_email)
        self.email_button.grid(row=5, column=0)

        self.pdf_button = tk.Button(self, text="Descargar PDF", command=self.download_pdf)
        self.pdf_button.grid(row=5, column=1)

def calculate(self):
    try:
        radio_inicial = float(self.radio_inicial.get())
        longitud_inicial = float(self.longitud_inicial.get())
        capacidad_inicial = float(self.capacidad_inicial.get())

        peso_gancho = float(self.peso_gancho.get())
        peso_herramienta = float(self.peso_herramienta.get())
        peso_carga = float(self.peso_carga.get())
        otros_pesos = float(self.otros_pesos.get())

        carga_bruta = peso_gancho + peso_herramienta + peso_carga + otros_pesos
        capacidad_bruta_menor = min(self.obtener_capacidad_por_radio(radio_inicial))

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Carga Bruta: {carga_bruta} kg\n")
        self.result_text.insert(tk.END, f"Capacidad Bruta Menor: {capacidad_bruta_menor} kg\n")

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
        # Lógica para enviar email
        pass

    def download_pdf(self):
        # Lógica para descargar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Plan de Izaje", ln=True, align='C')
        pdf.output("plan_de_izaje.pdf")
        messagebox.showinfo("Información", "Archivo PDF generado exitosamente.")

if __name__ == "__main__":
    app = PlanDeIzajeApp()
    app.mainloop()

