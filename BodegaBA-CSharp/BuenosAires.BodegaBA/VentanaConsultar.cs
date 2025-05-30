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
            this.Text = $"Administrar productos - Usuario: {cuenta}";
            btnVolver.Click += (sender, e) => Volver(cuenta);
            this.CentrarVentana();
            grid.ConfigurarDataGridView(
                 "idprod:ID, "
               + "nomprod:Nombre, "
               + "descprod:Descripción, "
               + "precio:Precio, "
               + "imagen:Imagen"
           );
        }

        private void Volver(string cuenta)
        {
            var ventana = new VentanaPrincipal(cuenta);
            this.Hide();
            ventana.ShowDialog();
        }
    }
}
