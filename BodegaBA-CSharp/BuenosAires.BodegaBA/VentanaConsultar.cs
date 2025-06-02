using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.ServiceProxy;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaConsultar : Form
    {
        public VentanaConsultar(string cuenta)
        {
            InitializeComponent();
            this.Text = $"Productos disponibles - Usuario: {cuenta}";
            btnVolver.Click += (sender, e) => Volver(cuenta);
            this.CentrarVentana();

            // Cargar productos desde el servicio
            var sc = new ScStockProducto();
            sc.StockProducto();
            grid.DataSource = sc.ListaProductos;

            grid.Columns["IdProd"].HeaderText = "ID Producto";
            grid.Columns["NomProd"].HeaderText = "Nombre";
            grid.Columns["Cantidad"].HeaderText = "Cantidad";  // ✅ NUEVA COLUMNA
            grid.Columns["Estado"].HeaderText = "Estado";
        }

        private void Volver(string cuenta)
        {
            var ventana = new VentanaPrincipal(cuenta);
            this.Hide();
            ventana.ShowDialog();
        }
    }
}
