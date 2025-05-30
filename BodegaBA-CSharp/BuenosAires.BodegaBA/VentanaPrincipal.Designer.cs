namespace BuenosAires.BodegaBA
{
    partial class VentanaPrincipal
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lbBodega = new System.Windows.Forms.Label();
            this.lbBuenosAires = new System.Windows.Forms.Label();
            this.btnConsultar = new System.Windows.Forms.Button();
            this.btnAdministrar = new System.Windows.Forms.Button();
            this.btnSalir = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // lbBodega
            // 
            this.lbBodega.AutoSize = true;
            this.lbBodega.Font = new System.Drawing.Font("Microsoft Sans Serif", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbBodega.Location = new System.Drawing.Point(155, 61);
            this.lbBodega.Name = "lbBodega";
            this.lbBodega.Size = new System.Drawing.Size(497, 36);
            this.lbBodega.TabIndex = 0;
            this.lbBodega.Text = "Sistema de Bodega - Menú Principal";
            this.lbBodega.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.lbBodega.Click += new System.EventHandler(this.label1_Click);
            // 
            // lbBuenosAires
            // 
            this.lbBuenosAires.AutoSize = true;
            this.lbBuenosAires.Location = new System.Drawing.Point(701, 9);
            this.lbBuenosAires.Name = "lbBuenosAires";
            this.lbBuenosAires.Size = new System.Drawing.Size(87, 16);
            this.lbBuenosAires.TabIndex = 1;
            this.lbBuenosAires.Text = "Buenos Aires";
            // 
            // btnConsultar
            // 
            this.btnConsultar.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnConsultar.Location = new System.Drawing.Point(201, 145);
            this.btnConsultar.Name = "btnConsultar";
            this.btnConsultar.Size = new System.Drawing.Size(382, 56);
            this.btnConsultar.TabIndex = 2;
            this.btnConsultar.Text = "Consultar Productos en Bodega";
            this.btnConsultar.UseVisualStyleBackColor = true;
            this.btnConsultar.Click += new System.EventHandler(this.btnConsultar_Click);
            // 
            // btnAdministrar
            // 
            this.btnAdministrar.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnAdministrar.Location = new System.Drawing.Point(201, 207);
            this.btnAdministrar.Name = "btnAdministrar";
            this.btnAdministrar.Size = new System.Drawing.Size(382, 55);
            this.btnAdministrar.TabIndex = 3;
            this.btnAdministrar.Text = "Administrar Guías de Despacho";
            this.btnAdministrar.UseVisualStyleBackColor = true;
            // 
            // btnSalir
            // 
            this.btnSalir.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSalir.Location = new System.Drawing.Point(201, 268);
            this.btnSalir.Name = "btnSalir";
            this.btnSalir.Size = new System.Drawing.Size(382, 49);
            this.btnSalir.TabIndex = 5;
            this.btnSalir.Text = "Salir";
            this.btnSalir.UseVisualStyleBackColor = true;
            this.btnSalir.Click += new System.EventHandler(this.btnSalir_Click);
            // 
            // VentanaPrincipal
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.btnSalir);
            this.Controls.Add(this.btnAdministrar);
            this.Controls.Add(this.btnConsultar);
            this.Controls.Add(this.lbBuenosAires);
            this.Controls.Add(this.lbBodega);
            this.Name = "VentanaPrincipal";
            this.Text = "Ventana Principal";
            this.Load += new System.EventHandler(this.VentanaPrincipal_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lbBodega;
        private System.Windows.Forms.Label lbBuenosAires;
        private System.Windows.Forms.Button btnConsultar;
        private System.Windows.Forms.Button btnAdministrar;
        private System.Windows.Forms.Button btnSalir;
    }
}