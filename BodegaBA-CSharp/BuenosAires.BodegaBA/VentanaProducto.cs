using System.Windows.Forms;
using BuenosAires.ServiceProxy;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaProducto : Form
    {
        public VentanaProducto(string cuenta)
        {
            InitializeComponent();
            this.Text = $"Mantenedor de productos - Usuario: {cuenta}";
            btnBuscar.Click += (sender, e) => Buscar();
            btnNuevo.Click += (sender, e) => Nuevo();
            btnGuardar.Click += (sender, e) => Guardar();
            btnEliminar.Click += (sender, e) => Eliminar();
            btnCargarProductos.Click += (sender, e) => CargarProductos();
            btnVolver.Click += (sender, e) => Volver(cuenta);
            grid.SelectionChanged += (sender, e) => Seleccionar();
            grid.ConfigurarDataGridView(
                  "idprod:ID, "
                + "nomprod:Nombre, "
                + "descprod:Descripción, "
                + "precio:Precio, "
                + "imagen:Imagen"
            );
            CargarProductos();
            this.CentrarVentana();
        }

        private void Nuevo()
        {
            this.Limpiar(new TextBox[]
            {
                txtIdProd,
                txtNomProd,
                txtDescProd,
                txtPrecio,
                txtImagen
            });
        }

        public bool ValidarCamposNumericos()
        {
            if (txtIdProd.Text != "" && !txtIdProd.EsNumero())
            {
                return this.ErrEntero("ID");
            }
            if (!txtPrecio.EsNumero())
            {
                return this.ErrEntero("Precio");
            }
            return true;
        }

        private void Seleccionar()
        {
            if (grid.SelectedRows.Count <= 0) return;

            DataGridViewRow row = grid.SelectedRows[0];
            if (row.GetString("idprod") != "0")
            {
                this.AsignarValoresTextBox(row);
            }
            txtNomProd.FocusToEnd();
        }

        private bool Buscar()
        {
            int id = new VentanaBuscarID().MostrarVentanaModal();
            if (id == -1) return false;

            var bc = new ScProducto();
            bc.Leer(id);

            if (bc.Producto == null) return this.MensajeInfo(bc.Mensaje);

            CargarProductos();
            this.AsignarValoresTextBox(bc.Producto);

            grid.SeleccionarId("idprod", txtIdProd.ToInt());
            txtNomProd.FocusToEnd();
            return true;
        }

        private void Guardar()
        {
            if (!ValidarCamposNumericos()) return;

            var prod = new Producto();
            prod.idprod = txtIdProd.ToIntOrDefault();
            prod.nomprod = txtNomProd.Text;
            prod.descprod = txtDescProd.Text;
            prod.precio = txtPrecio.ToInt();
            prod.imagen = txtImagen.Text;

            var bc = new ScProducto();

            if (txtIdProd.Text.Trim() == "")
            {
                bc.Crear(prod);
            }
            else
            {
                bc.Actualizar(prod);
            }

            if (!bc.HayErrores)
            {
                txtIdProd.SetText(bc.Producto.idprod);
                CargarProductos();
                grid.SeleccionarId("idprod", bc.Producto.idprod);
                txtNomProd.FocusToEnd();
            }

            this.MensajeInfo(bc.Mensaje);
        }

        private bool Eliminar()
        {
            var bc = new ScProducto();
            if (txtIdProd.Text.Trim() == "")
            {
                return this.ErrAccionID("ID", "eliminar");
            }
            bc.Eliminar(txtIdProd.ToInt());
            CargarProductos();
            this.MensajeInfo(bc.Mensaje);
            return true;
        }

        private void Volver(string cuenta)
        {
            var ventana = new VentanaPrincipal(cuenta);
            this.Hide();
            ventana.ShowDialog();
        }

        public void CargarProductos()
        {
            var bc = new ScProducto();
            bc.LeerTodos();
            grid.DataSource = bc.Lista;
            grid.RefrescarYajustar();
            if (bc.HayErrores == true) this.MensajeInfo(bc.Mensaje);
        }

        private void panSuperior_Paint(object sender, PaintEventArgs e)
        {

        }

        private void txtNomProd_TextChanged(object sender, System.EventArgs e)
        {

        }

        private void lblIdProd_Click(object sender, System.EventArgs e)
        {

        }

        private void btnBuscar_Click(object sender, System.EventArgs e)
        {

        }

        private void btnCargarProductos_Click(object sender, System.EventArgs e)
        {

        }

        private void btnEliminar_Click(object sender, System.EventArgs e)
        {

        }

        private void lblNomProd_Click(object sender, System.EventArgs e)
        {

        }

        private void btnGuardar_Click(object sender, System.EventArgs e)
        {

        }

        private void lblDescProd_Click(object sender, System.EventArgs e)
        {

        }

        private void btnNuevo_Click(object sender, System.EventArgs e)
        {

        }

        private void lblPrecio_Click(object sender, System.EventArgs e)
        {

        }

        private void txtImagen_TextChanged(object sender, System.EventArgs e)
        {

        }

        private void lblImagen_Click(object sender, System.EventArgs e)
        {

        }

        private void txtPrecio_TextChanged(object sender, System.EventArgs e)
        {

        }

        private void txtIdProd_TextChanged(object sender, System.EventArgs e)
        {

        }

        private void txtDescProd_TextChanged(object sender, System.EventArgs e)
        {

        }

        private void lbBuenosAires_Click(object sender, System.EventArgs e)
        {

        }
    }
}
