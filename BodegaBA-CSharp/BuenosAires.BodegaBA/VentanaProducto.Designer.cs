namespace BuenosAires.BodegaBA
{
    partial class VentanaProducto
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de Windows Forms

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnCargarProductos = new System.Windows.Forms.Button();
            this.grid = new System.Windows.Forms.DataGridView();
            this.lblIdProd = new System.Windows.Forms.Label();
            this.lblNomProd = new System.Windows.Forms.Label();
            this.lblDescProd = new System.Windows.Forms.Label();
            this.lblPrecio = new System.Windows.Forms.Label();
            this.lblImagen = new System.Windows.Forms.Label();
            this.txtIdProd = new System.Windows.Forms.TextBox();
            this.txtNomProd = new System.Windows.Forms.TextBox();
            this.txtDescProd = new System.Windows.Forms.TextBox();
            this.txtPrecio = new System.Windows.Forms.TextBox();
            this.txtImagen = new System.Windows.Forms.TextBox();
            this.btnNuevo = new System.Windows.Forms.Button();
            this.btnGuardar = new System.Windows.Forms.Button();
            this.btnEliminar = new System.Windows.Forms.Button();
            this.btnBuscar = new System.Windows.Forms.Button();
            this.panSuperior = new System.Windows.Forms.Panel();
            this.btnVolver = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.lbBuenosAires = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.grid)).BeginInit();
            this.panSuperior.SuspendLayout();
            this.SuspendLayout();
            // 
            // btnCargarProductos
            // 
            this.btnCargarProductos.Location = new System.Drawing.Point(634, 293);
            this.btnCargarProductos.Margin = new System.Windows.Forms.Padding(4);
            this.btnCargarProductos.Name = "btnCargarProductos";
            this.btnCargarProductos.Size = new System.Drawing.Size(139, 28);
            this.btnCargarProductos.TabIndex = 10;
            this.btnCargarProductos.Text = "Cargar productos";
            this.btnCargarProductos.UseVisualStyleBackColor = true;
            this.btnCargarProductos.Click += new System.EventHandler(this.btnCargarProductos_Click);
            // 
            // grid
            // 
            this.grid.ColumnHeadersHeight = 29;
            this.grid.Location = new System.Drawing.Point(94, 345);
            this.grid.Margin = new System.Windows.Forms.Padding(4);
            this.grid.Name = "grid";
            this.grid.RowHeadersWidth = 51;
            this.grid.Size = new System.Drawing.Size(761, 354);
            this.grid.TabIndex = 11;
            // 
            // lblIdProd
            // 
            this.lblIdProd.AutoSize = true;
            this.lblIdProd.Location = new System.Drawing.Point(192, 118);
            this.lblIdProd.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblIdProd.Name = "lblIdProd";
            this.lblIdProd.Size = new System.Drawing.Size(20, 16);
            this.lblIdProd.TabIndex = 2;
            this.lblIdProd.Text = "ID";
            this.lblIdProd.Click += new System.EventHandler(this.lblIdProd_Click);
            // 
            // lblNomProd
            // 
            this.lblNomProd.AutoSize = true;
            this.lblNomProd.Location = new System.Drawing.Point(192, 152);
            this.lblNomProd.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblNomProd.Name = "lblNomProd";
            this.lblNomProd.Size = new System.Drawing.Size(56, 16);
            this.lblNomProd.TabIndex = 3;
            this.lblNomProd.Text = "Nombre";
            this.lblNomProd.Click += new System.EventHandler(this.lblNomProd_Click);
            // 
            // lblDescProd
            // 
            this.lblDescProd.AutoSize = true;
            this.lblDescProd.Location = new System.Drawing.Point(192, 185);
            this.lblDescProd.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblDescProd.Name = "lblDescProd";
            this.lblDescProd.Size = new System.Drawing.Size(79, 16);
            this.lblDescProd.TabIndex = 4;
            this.lblDescProd.Text = "Descripción";
            this.lblDescProd.Click += new System.EventHandler(this.lblDescProd_Click);
            // 
            // lblPrecio
            // 
            this.lblPrecio.AutoSize = true;
            this.lblPrecio.Location = new System.Drawing.Point(192, 220);
            this.lblPrecio.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblPrecio.Name = "lblPrecio";
            this.lblPrecio.Size = new System.Drawing.Size(46, 16);
            this.lblPrecio.TabIndex = 5;
            this.lblPrecio.Text = "Precio";
            this.lblPrecio.Click += new System.EventHandler(this.lblPrecio_Click);
            // 
            // lblImagen
            // 
            this.lblImagen.AutoSize = true;
            this.lblImagen.Location = new System.Drawing.Point(192, 253);
            this.lblImagen.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblImagen.Name = "lblImagen";
            this.lblImagen.Size = new System.Drawing.Size(52, 16);
            this.lblImagen.TabIndex = 6;
            this.lblImagen.Text = "Imagen";
            this.lblImagen.Click += new System.EventHandler(this.lblImagen_Click);
            // 
            // txtIdProd
            // 
            this.txtIdProd.Enabled = false;
            this.txtIdProd.Location = new System.Drawing.Point(286, 114);
            this.txtIdProd.Margin = new System.Windows.Forms.Padding(4);
            this.txtIdProd.Name = "txtIdProd";
            this.txtIdProd.ReadOnly = true;
            this.txtIdProd.Size = new System.Drawing.Size(67, 22);
            this.txtIdProd.TabIndex = 1;
            this.txtIdProd.TextChanged += new System.EventHandler(this.txtIdProd_TextChanged);
            // 
            // txtNomProd
            // 
            this.txtNomProd.Location = new System.Drawing.Point(286, 149);
            this.txtNomProd.Margin = new System.Windows.Forms.Padding(4);
            this.txtNomProd.Name = "txtNomProd";
            this.txtNomProd.Size = new System.Drawing.Size(512, 22);
            this.txtNomProd.TabIndex = 3;
            this.txtNomProd.TextChanged += new System.EventHandler(this.txtNomProd_TextChanged);
            // 
            // txtDescProd
            // 
            this.txtDescProd.Location = new System.Drawing.Point(284, 182);
            this.txtDescProd.Margin = new System.Windows.Forms.Padding(4);
            this.txtDescProd.Name = "txtDescProd";
            this.txtDescProd.Size = new System.Drawing.Size(514, 22);
            this.txtDescProd.TabIndex = 4;
            this.txtDescProd.TextChanged += new System.EventHandler(this.txtDescProd_TextChanged);
            // 
            // txtPrecio
            // 
            this.txtPrecio.Location = new System.Drawing.Point(286, 216);
            this.txtPrecio.Margin = new System.Windows.Forms.Padding(4);
            this.txtPrecio.Name = "txtPrecio";
            this.txtPrecio.Size = new System.Drawing.Size(99, 22);
            this.txtPrecio.TabIndex = 5;
            this.txtPrecio.TextChanged += new System.EventHandler(this.txtPrecio_TextChanged);
            // 
            // txtImagen
            // 
            this.txtImagen.Location = new System.Drawing.Point(284, 249);
            this.txtImagen.Margin = new System.Windows.Forms.Padding(4);
            this.txtImagen.Name = "txtImagen";
            this.txtImagen.Size = new System.Drawing.Size(514, 22);
            this.txtImagen.TabIndex = 6;
            this.txtImagen.TextChanged += new System.EventHandler(this.txtImagen_TextChanged);
            // 
            // btnNuevo
            // 
            this.btnNuevo.Location = new System.Drawing.Point(196, 293);
            this.btnNuevo.Margin = new System.Windows.Forms.Padding(4);
            this.btnNuevo.Name = "btnNuevo";
            this.btnNuevo.Size = new System.Drawing.Size(139, 28);
            this.btnNuevo.TabIndex = 7;
            this.btnNuevo.Text = "Nuevo";
            this.btnNuevo.UseVisualStyleBackColor = true;
            this.btnNuevo.Click += new System.EventHandler(this.btnNuevo_Click);
            // 
            // btnGuardar
            // 
            this.btnGuardar.Location = new System.Drawing.Point(343, 293);
            this.btnGuardar.Margin = new System.Windows.Forms.Padding(4);
            this.btnGuardar.Name = "btnGuardar";
            this.btnGuardar.Size = new System.Drawing.Size(139, 28);
            this.btnGuardar.TabIndex = 8;
            this.btnGuardar.Text = "Guardar";
            this.btnGuardar.UseVisualStyleBackColor = true;
            this.btnGuardar.Click += new System.EventHandler(this.btnGuardar_Click);
            // 
            // btnEliminar
            // 
            this.btnEliminar.Location = new System.Drawing.Point(490, 293);
            this.btnEliminar.Margin = new System.Windows.Forms.Padding(4);
            this.btnEliminar.Name = "btnEliminar";
            this.btnEliminar.Size = new System.Drawing.Size(136, 28);
            this.btnEliminar.TabIndex = 9;
            this.btnEliminar.Text = "Eliminar";
            this.btnEliminar.UseVisualStyleBackColor = true;
            this.btnEliminar.Click += new System.EventHandler(this.btnEliminar_Click);
            // 
            // btnBuscar
            // 
            this.btnBuscar.Location = new System.Drawing.Point(362, 112);
            this.btnBuscar.Margin = new System.Windows.Forms.Padding(4);
            this.btnBuscar.Name = "btnBuscar";
            this.btnBuscar.Size = new System.Drawing.Size(100, 28);
            this.btnBuscar.TabIndex = 2;
            this.btnBuscar.Text = "Buscar";
            this.btnBuscar.UseVisualStyleBackColor = true;
            this.btnBuscar.Click += new System.EventHandler(this.btnBuscar_Click);
            // 
            // panSuperior
            // 
            this.panSuperior.Controls.Add(this.btnVolver);
            this.panSuperior.Controls.Add(this.label1);
            this.panSuperior.Controls.Add(this.lbBuenosAires);
            this.panSuperior.Controls.Add(this.lblIdProd);
            this.panSuperior.Controls.Add(this.btnBuscar);
            this.panSuperior.Controls.Add(this.btnCargarProductos);
            this.panSuperior.Controls.Add(this.btnEliminar);
            this.panSuperior.Controls.Add(this.lblNomProd);
            this.panSuperior.Controls.Add(this.btnGuardar);
            this.panSuperior.Controls.Add(this.lblDescProd);
            this.panSuperior.Controls.Add(this.btnNuevo);
            this.panSuperior.Controls.Add(this.lblPrecio);
            this.panSuperior.Controls.Add(this.txtImagen);
            this.panSuperior.Controls.Add(this.lblImagen);
            this.panSuperior.Controls.Add(this.txtPrecio);
            this.panSuperior.Controls.Add(this.txtIdProd);
            this.panSuperior.Controls.Add(this.txtDescProd);
            this.panSuperior.Controls.Add(this.txtNomProd);
            this.panSuperior.Dock = System.Windows.Forms.DockStyle.Top;
            this.panSuperior.Location = new System.Drawing.Point(0, 0);
            this.panSuperior.Margin = new System.Windows.Forms.Padding(4);
            this.panSuperior.Name = "panSuperior";
            this.panSuperior.Size = new System.Drawing.Size(979, 337);
            this.panSuperior.TabIndex = 17;
            this.panSuperior.Paint += new System.Windows.Forms.PaintEventHandler(this.panSuperior_Paint);
            // 
            // btnVolver
            // 
            this.btnVolver.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnVolver.Location = new System.Drawing.Point(24, 21);
            this.btnVolver.Name = "btnVolver";
            this.btnVolver.Size = new System.Drawing.Size(132, 39);
            this.btnVolver.TabIndex = 13;
            this.btnVolver.Text = "VOLVER";
            this.btnVolver.UseVisualStyleBackColor = true;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 24F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(372, 21);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(202, 46);
            this.label1.TabIndex = 12;
            this.label1.Text = "Productos";
            // 
            // lbBuenosAires
            // 
            this.lbBuenosAires.AutoSize = true;
            this.lbBuenosAires.Location = new System.Drawing.Point(880, 21);
            this.lbBuenosAires.Name = "lbBuenosAires";
            this.lbBuenosAires.Size = new System.Drawing.Size(87, 16);
            this.lbBuenosAires.TabIndex = 11;
            this.lbBuenosAires.Text = "Buenos Aires";
            this.lbBuenosAires.Click += new System.EventHandler(this.lbBuenosAires_Click);
            // 
            // VentanaProducto
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(979, 719);
            this.Controls.Add(this.panSuperior);
            this.Controls.Add(this.grid);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "VentanaProducto";
            this.Text = "Mantenedor de Productos";
            ((System.ComponentModel.ISupportInitialize)(this.grid)).EndInit();
            this.panSuperior.ResumeLayout(false);
            this.panSuperior.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnCargarProductos;
        private System.Windows.Forms.DataGridView grid;
        private System.Windows.Forms.Label lblIdProd;
        private System.Windows.Forms.Label lblNomProd;
        private System.Windows.Forms.Label lblDescProd;
        private System.Windows.Forms.Label lblPrecio;
        private System.Windows.Forms.Label lblImagen;
        private System.Windows.Forms.TextBox txtIdProd;
        private System.Windows.Forms.TextBox txtNomProd;
        private System.Windows.Forms.TextBox txtDescProd;
        private System.Windows.Forms.TextBox txtPrecio;
        private System.Windows.Forms.TextBox txtImagen;
        private System.Windows.Forms.Button btnNuevo;
        private System.Windows.Forms.Button btnGuardar;
        private System.Windows.Forms.Button btnEliminar;
        private System.Windows.Forms.Button btnBuscar;
        private System.Windows.Forms.Panel panSuperior;
        private System.Windows.Forms.Label lbBuenosAires;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnVolver;
    }
}

