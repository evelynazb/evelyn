import tkinter as tk
from tkinter import ttk, Frame, Label, Button, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tkcalendar import DateEntry  # Necesitarás instalar esta biblioteca: pip install tkcalendar


# Crear datos simulados para el negocio de waffles
def generar_datos_simulados(dias=90):
    fechas = [datetime.now() - timedelta(days=i) for i in range(dias)]
    fechas.reverse()

    # Tipos de waffles
    tipos_waffles = ['Clásico', 'Chocolate', 'Fresa', 'Nutella', 'Especial']

    # Datos base de ventas
    ventas_base = [35, 28, 25, 40, 20]

    # Datos diarios con variación aleatoria
    datos = []
    for fecha in fechas:
        # Simular tendencia semanal (más ventas en fines de semana)
        factor_dia = 1.5 if fecha.weekday() >= 5 else 1.0

        # Simular variación por mes
        factor_mes = 1.0 + (fecha.month % 3) * 0.1

        for i, tipo in enumerate(tipos_waffles):
            # Ventas base * factores * variación aleatoria
            ventas = int(ventas_base[i] * factor_dia * factor_mes * np.random.uniform(0.8, 1.2))
            precio = 5 + (i * 1.5)  # Precio base + incremento según tipo
            ingresos = ventas * precio
            costo = ventas * (precio * 0.4)  # Costo estimado (40% del precio)

            datos.append({
                'fecha': fecha,
                'fecha_str': fecha.strftime('%Y-%m-%d'),
                'dia_semana': fecha.strftime('%A'),
                'tipo_waffle': tipo,
                'ventas': ventas,
                'precio': precio,
                'ingresos': ingresos,
                'costos': costo,
                'beneficio': ingresos - costo
            })

    return pd.DataFrame(datos)


class WaffleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Negocio de Waffles")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')

        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background='white', font=('Arial', 10))
        self.style.configure('TFrame', background='white')
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Metric.TLabel', font=('Arial', 14, 'bold'))

        # Generar datos
        self.df = generar_datos_simulados()
        self.tipos_waffles = self.df['tipo_waffle'].unique()

        # Variables para filtros
        self.fecha_inicio = self.df['fecha'].min()
        self.fecha_fin = self.df['fecha'].max()
        self.tipos_seleccionados = list(self.tipos_waffles)

        # Crear widgets
        self.crear_layout()
        self.actualizar_dashboard()

    def crear_layout(self):
        # Panel principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.pack(fill=tk.X, pady=5)
        ttk.Label(titulo_frame, text="Dashboard - Negocio de Waffles", style='Header.TLabel').pack()

        # Panel de filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtros")
        filtros_frame.pack(fill=tk.X, pady=5)

        # Filtro de fechas
        fechas_frame = ttk.Frame(filtros_frame)
        fechas_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(fechas_frame, text="Fecha inicio:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_inicio_widget = DateEntry(fechas_frame, width=12, date_pattern='yyyy-mm-dd',
                                             firstweekday='sunday')
        self.fecha_inicio_widget.grid(row=0, column=1, padx=5, pady=5)
        self.fecha_inicio_widget.set_date(self.fecha_inicio)

        ttk.Label(fechas_frame, text="Fecha fin:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_fin_widget = DateEntry(fechas_frame, width=12, date_pattern='yyyy-mm-dd',
                                          firstweekday='sunday')
        self.fecha_fin_widget.grid(row=0, column=3, padx=5, pady=5)
        self.fecha_fin_widget.set_date(self.fecha_fin)

        # Filtro de tipos de waffles
        waffle_frame = ttk.Frame(filtros_frame)
        waffle_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(waffle_frame, text="Tipos de waffles:").grid(row=0, column=0, padx=5, pady=5)

        # Variables para checkboxes
        self.checkvar = {}
        for i, tipo in enumerate(self.tipos_waffles):
            self.checkvar[tipo] = tk.BooleanVar(value=True)
            ttk.Checkbutton(waffle_frame, text=tipo, variable=self.checkvar[tipo]).grid(
                row=0, column=i + 1, padx=5, pady=5)

        # Botón para aplicar filtros
        ttk.Button(filtros_frame, text="Aplicar Filtros",
                   command=self.actualizar_filtros).pack(pady=5)

        # Panel de métricas
        metricas_frame = ttk.LabelFrame(main_frame, text="Métricas Clave")
        metricas_frame.pack(fill=tk.X, pady=5)

        # Variables para métricas
        self.var_ventas = StringVar()
        self.var_ingresos = StringVar()
        self.var_beneficio = StringVar()
        self.var_margen = StringVar()

        # Layout de métricas en grid
        ttk.Label(metricas_frame, text="Ventas Totales:", style='Metric.TLabel').grid(
            row=0, column=0, padx=10, pady=5)
        ttk.Label(metricas_frame, textvariable=self.var_ventas).grid(
            row=1, column=0, padx=10, pady=5)

        ttk.Label(metricas_frame, text="Ingresos Totales:", style='Metric.TLabel').grid(
            row=0, column=1, padx=10, pady=5)
        ttk.Label(metricas_frame, textvariable=self.var_ingresos).grid(
            row=1, column=1, padx=10, pady=5)

        ttk.Label(metricas_frame, text="Beneficio Total:", style='Metric.TLabel').grid(
            row=0, column=2, padx=10, pady=5)
        ttk.Label(metricas_frame, textvariable=self.var_beneficio).grid(
            row=1, column=2, padx=10, pady=5)

        ttk.Label(metricas_frame, text="Margen Promedio:", style='Metric.TLabel').grid(
            row=0, column=3, padx=10, pady=5)
        ttk.Label(metricas_frame, textvariable=self.var_margen).grid(
            row=1, column=3, padx=10, pady=5)

        # Panel de gráficos
        graficos_frame = ttk.Frame(main_frame)
        graficos_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Dividir en dos columnas
        left_frame = ttk.Frame(graficos_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(graficos_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear contenedores para los gráficos
        self.tendencia_frame = ttk.LabelFrame(left_frame, text="Tendencia de Ventas")
        self.tendencia_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tipos_frame = ttk.LabelFrame(right_frame, text="Ventas por Tipo de Waffle")
        self.tipos_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.dias_frame = ttk.LabelFrame(left_frame, text="Ventas por Día de la Semana")
        self.dias_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tabla de datos
        self.tabla_frame = ttk.LabelFrame(main_frame, text="Datos Recientes")
        self.tabla_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Crear Treeview para la tabla
        self.tree = ttk.Treeview(self.tabla_frame,
                                 columns=('fecha', 'tipo', 'ventas', 'ingresos', 'costos', 'beneficio'),
                                 show='headings')

        self.tree.heading('fecha', text='Fecha')
        self.tree.heading('tipo', text='Tipo de Waffle')
        self.tree.heading('ventas', text='Ventas')
        self.tree.heading('ingresos', text='Ingresos')
        self.tree.heading('costos', text='Costos')
        self.tree.heading('beneficio', text='Beneficio')

        self.tree.column('fecha', width=100)
        self.tree.column('tipo', width=120)
        self.tree.column('ventas', width=80, anchor='e')
        self.tree.column('ingresos', width=100, anchor='e')
        self.tree.column('costos', width=100, anchor='e')
        self.tree.column('beneficio', width=100, anchor='e')

        scrollbar = ttk.Scrollbar(self.tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def actualizar_filtros(self):
        # Actualizar filtros según selección del usuario
        self.fecha_inicio = self.fecha_inicio_widget.get_date()
        self.fecha_fin = self.fecha_fin_widget.get_date()

        self.tipos_seleccionados = [tipo for tipo, var in self.checkvar.items() if var.get()]

        # Actualizar el dashboard
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        # Filtrar datos según selección
        df_filtrado = self.df[
            (self.df['fecha'] >= pd.Timestamp(self.fecha_inicio)) &
            (self.df['fecha'] <= pd.Timestamp(self.fecha_fin))
            ]

        if self.tipos_seleccionados:
            df_filtrado = df_filtrado[df_filtrado['tipo_waffle'].isin(self.tipos_seleccionados)]

        # Actualizar métricas
        ventas_totales = df_filtrado['ventas'].sum()
        ingresos_totales = df_filtrado['ingresos'].sum()
        beneficio_total = df_filtrado['beneficio'].sum()
        margen_promedio = (beneficio_total / ingresos_totales * 100) if ingresos_totales > 0 else 0

        self.var_ventas.set(f"{ventas_totales:.0f} unidades")
        self.var_ingresos.set(f"${ingresos_totales:.2f}")
        self.var_beneficio.set(f"${beneficio_total:.2f}")
        self.var_margen.set(f"{margen_promedio:.1f}%")

        # Actualizar gráficos
        self.actualizar_grafico_tendencia(df_filtrado)
        self.actualizar_grafico_tipos(df_filtrado)
        self.actualizar_grafico_dias(df_filtrado)
        self.actualizar_tabla(df_filtrado)

    def actualizar_grafico_tendencia(self, df):
        # Limpiar frame
        for widget in self.tendencia_frame.winfo_children():
            widget.destroy()

        # Agrupar datos por fecha
        df_tendencia = df.groupby('fecha_str')[['ventas', 'ingresos', 'beneficio']].sum().reset_index()

        # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(df_tendencia['fecha_str'], df_tendencia['ventas'], 'b-', label='Ventas')
        ax.plot(df_tendencia['fecha_str'], df_tendencia['ingresos'], 'g-', label='Ingresos')
        ax.plot(df_tendencia['fecha_str'], df_tendencia['beneficio'], 'r-', label='Beneficio')

        ax.set_title('Tendencia a lo largo del tiempo')
        ax.legend()

        # Ajustar etiquetas del eje x para mostrar menos fechas
        if len(df_tendencia) > 10:
            mostrar_indices = np.linspace(0, len(df_tendencia) - 1, 10, dtype=int)
            ax.set_xticks([df_tendencia['fecha_str'].iloc[i] for i in mostrar_indices])

        fig.tight_layout()

        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.tendencia_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def actualizar_grafico_tipos(self, df):
        # Limpiar frame
        for widget in self.tipos_frame.winfo_children():
            widget.destroy()

        # Agrupar datos por tipo
        df_tipos = df.groupby('tipo_waffle')[['ventas']].sum().reset_index()

        # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        bars = ax.bar(df_tipos['tipo_waffle'], df_tipos['ventas'])

        # Añadir color a las barras
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        for i, bar in enumerate(bars):
            bar.set_color(colors[i % len(colors)])

        ax.set_title('Ventas por Tipo de Waffle')
        ax.set_ylabel('Unidades vendidas')

        # Ajustar etiquetas del eje x
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

        fig.tight_layout()

        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.tipos_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def actualizar_grafico_dias(self, df):
        # Limpiar frame
        for widget in self.dias_frame.winfo_children():
            widget.destroy()

        # Agrupar datos por día
        df_dias = df.groupby('dia_semana')[['ventas']].sum().reset_index()

        # Ordenar días de la semana correctamente
        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_dias['dia_semana'] = pd.Categorical(df_dias['dia_semana'], categories=orden_dias, ordered=True)
        df_dias = df_dias.sort_values('dia_semana')

        # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        bars = ax.bar(df_dias['dia_semana'], df_dias['ventas'])

        # Añadir color a las barras
        for i, bar in enumerate(bars):
            # Color más intenso para el fin de semana
            if i >= 5:  # Sábado y domingo
                bar.set_color('#ff7f0e')
            else:
                bar.set_color('#1f77b4')

        ax.set_title('Ventas por Día de la Semana')
        ax.set_ylabel('Unidades vendidas')

        # Ajustar etiquetas del eje x
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

        fig.tight_layout()

        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.dias_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def actualizar_tabla(self, df):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agrupar datos
        df_tabla = df.groupby(['fecha_str', 'tipo_waffle'])[
            ['ventas', 'ingresos', 'costos', 'beneficio']].sum().reset_index()
        df_tabla = df_tabla.sort_values(['fecha_str', 'tipo_waffle'], ascending=[False, True])

        # Insertar datos en la tabla
        for i, row in df_tabla.head(20).iterrows():
            self.tree.insert("", tk.END, values=(
                row['fecha_str'],
                row['tipo_waffle'],
                f"{row['ventas']:.0f}",
                f"${row['ingresos']:.2f}",
                f"${row['costos']:.2f}",
                f"${row['beneficio']:.2f}"
            ))


# Función principal
def main():
    root = tk.Tk()
    app = WaffleDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()