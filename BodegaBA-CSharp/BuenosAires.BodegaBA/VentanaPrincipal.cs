using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaPrincipal : Form
    {
        public VentanaPrincipal(string cuenta)
        {
            InitializeComponent();
            this.Text = $"Ventana¨Principal - Usuario: {cuenta}";
            this.StartPosition = FormStartPosition.CenterScreen;

            btnConsultar.Click += (sender, e) => EnviarProducto(cuenta);
            btnAdministrar.Click += (sender, e) => EnviarAdministrar(cuenta);


        }

        private void EnviarProducto(string cuenta)
        {
            VentanaProducto ventana = new VentanaProducto(cuenta);
            ventana.ShowDialog();
            this.Hide();
        }

        private void EnviarAdministrar(string cuenta)
        {
            VentanaConsultar ventana = new VentanaConsultar(cuenta);
            ventana.ShowDialog();
            this.Hide();
        }

        private void VentanaPrincipal_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void btnConsultar_Click(object sender, EventArgs e)
        {

        }

        private void btnSalir_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
