using System;
using System.Windows.Forms;
using BuenosAires.Model.Utiles;
using BuenosAires.ServiceProxy;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaLogin : Form
    {
        public VentanaLogin()
        {
            InitializeComponent();
            this.AcceptButton = btnIngresar;
            this.StartPosition = FormStartPosition.CenterScreen;
        }

        private void btnIngresar_Click(object sender, EventArgs e)
        {
            if(txtCuenta.Text.Trim() == "")
            {
                this.MensajeInfo("Debe ingresar una cuenta");
                return;
            }
            if (txtPassword.Text.Trim() == "")
            {
                this.MensajeInfo("Debe ingresar una contraseña");
                return;
            }

            var ventana = new VentanaPrincipal(txtCuenta.Text);
            this.Hide();
            ventana.ShowDialog();

            var sc = new ScAutenticacion();
            sc.Autenticar("Bodeguero", txtCuenta.Text, txtPassword.Text);
            if (sc.Autenticado)
            {
                new VentanaProducto(sc.NombreUsuario + " (" + sc.TipoUsuario + ")").Show();
                Hide();
            }
            else
            {
                this.MensajeInfo(sc.Mensaje);
            }
        }

        private void txtPassword_TextChanged(object sender, EventArgs e)
        {

        }

        private void txtCuenta_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
