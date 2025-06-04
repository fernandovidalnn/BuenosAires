using System;
using System.Windows.Forms;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaGuiasDespacho : Form
    {
        private string cuenta;

        public VentanaGuiasDespacho(string cuenta)
        {
            InitializeComponent();
            this.cuenta = cuenta;
            this.Text = $"Guías de Despacho - Usuario: {cuenta}";

            // Configurar columnas base
            grid.ConfigurarDataGridView(
                  "NroGD:N° Guía, "
                + "Producto:Producto, "
                + "EstadoGD:Estado, "
                + "NroFac:N° Factura, "
                + "Cliente:Cliente"
            );

            // Eventos
            btnVolver.Click += (sender, e) => Volver();
            grid.SelectionChanged += (sender, e) => Seleccionar();
            grid.CellClick += Grid_CellClick;

            // Cargar datos
            CargarGuias();
            this.CentrarVentana();
        }

        private void CargarGuias()
        {
            var bc = new ScGuiaDespacho();
            bc.ObtenerGuias();
            grid.DataSource = bc.ListaGuias;
            grid.RefrescarYajustar();

            // Agregar botones si aún no existen
            if (!grid.Columns.Contains("btnDespachado"))
            {
                var btnDespachado = new DataGridViewButtonColumn
                {
                    HeaderText = "Opciones",
                    Name = "btnDespachado",
                    Text = "Despachado",
                    UseColumnTextForButtonValue = true
                };
                grid.Columns.Add(btnDespachado);

                var btnImprimir = new DataGridViewButtonColumn
                {
                    HeaderText = "",
                    Name = "btnImprimir",
                    Text = "Imprimir",
                    UseColumnTextForButtonValue = true
                };
                grid.Columns.Add(btnImprimir);

                var btnEntregado = new DataGridViewButtonColumn
                {
                    HeaderText = "",
                    Name = "btnEntregado",
                    Text = "Entregado",
                    UseColumnTextForButtonValue = true
                };
                grid.Columns.Add(btnEntregado);
            }

            if (bc.ListaGuias.Count == 0)
            {
                this.MensajeInfo("No se encontraron guías de despacho.");
            }

            if (bc.JsonGuiaDespacho == "" || bc.ListaGuias == null)
            {
                this.MensajeInfo("Error al cargar las guías de despacho.");
            }
        }

        private void Grid_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0 || e.ColumnIndex < 0) return;

            string columna = grid.Columns[e.ColumnIndex].Name;
            int nroGD = Convert.ToInt32(grid.Rows[e.RowIndex].Cells["NroGD"].Value);
            var sc = new ScGuiaDespacho(); // clase lógica ya con ActualizarEstadoGuiaDespacho

            if (columna == "btnDespachado")
            {
                sc.ActualizarEstadoGuiaDespacho(nroGD, "Despachado");
                CargarGuias(); // Refresca la tabla
            }
            else if (columna == "btnEntregado")
            {
                sc.ActualizarEstadoGuiaDespacho(nroGD, "Entregado");
                CargarGuias(); // Refresca la tabla
            }
            else if (columna == "btnImprimir")
            {
                MessageBox.Show($"Función de imprimir para Guía {nroGD} aún no implementada", "Imprimir", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            // Puedes mostrar mensaje de confirmación
            if (!string.IsNullOrEmpty(sc.Mensaje))
                this.MensajeInfo(sc.Mensaje);
        }


        private void Seleccionar()
        {
            if (grid.SelectedRows.Count <= 0) return;

            var row = grid.SelectedRows[0];
            int nroGD = Convert.ToInt32(row.Cells["NroGD"].Value);
            string estado = row.Cells["EstadoGD"].Value.ToString();
            string mensaje = $"Guía seleccionada: {nroGD} – Estado: {estado}";
            // this.MensajeInfo(mensaje);
        }

        private void Volver()
        {
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        private void label1_Click(object sender, EventArgs e) { }
        private void lbBuenosAires_Click(object sender, EventArgs e) { }
        private void panSuperior_Paint(object sender, PaintEventArgs e) { }
    }
}
