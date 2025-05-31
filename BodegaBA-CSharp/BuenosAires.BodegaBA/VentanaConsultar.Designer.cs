namespace BuenosAires.BodegaBA
{
    partial class VentanaConsultar
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
            this.lbProductoDisponible = new System.Windows.Forms.Label();
            this.lbBuenosAires = new System.Windows.Forms.Label();
            this.btnVolver = new System.Windows.Forms.Button();
            this.grid = new System.Windows.Forms.DataGridView();
            ((System.ComponentModel.ISupportInitialize)(this.grid)).BeginInit();
            this.SuspendLayout();
            // 
            // lbProductoDisponible
            // 
            this.lbProductoDisponible.AutoSize = true;
            this.lbProductoDisponible.Font = new System.Drawing.Font("Microsoft Sans Serif", 22.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbProductoDisponible.Location = new System.Drawing.Point(216, 46);
            this.lbProductoDisponible.Name = "lbProductoDisponible";
            this.lbProductoDisponible.Size = new System.Drawing.Size(583, 42);
            this.lbProductoDisponible.TabIndex = 0;
            this.lbProductoDisponible.Text = "Productos Disponibles en Bodega";
            // 
            // lbBuenosAires
            // 
            this.lbBuenosAires.AutoSize = true;
            this.lbBuenosAires.Location = new System.Drawing.Point(902, 28);
            this.lbBuenosAires.Name = "lbBuenosAires";
            this.lbBuenosAires.Size = new System.Drawing.Size(87, 16);
            this.lbBuenosAires.TabIndex = 1;
            this.lbBuenosAires.Text = "Buenos Aires";
            // 
            // btnVolver
            // 
            this.btnVolver.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnVolver.Location = new System.Drawing.Point(12, 12);
            this.btnVolver.Name = "btnVolver";
            this.btnVolver.Size = new System.Drawing.Size(130, 42);
            this.btnVolver.TabIndex = 2;
            this.btnVolver.Text = "VOLVER";
            this.btnVolver.UseVisualStyleBackColor = true;
            // 
            // grid
            // 
            this.grid.AllowUserToAddRows = false;
            this.grid.AllowUserToDeleteRows = false;
            this.grid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.grid.Location = new System.Drawing.Point(130, 196);
            this.grid.Name = "grid";
            this.grid.ReadOnly = true;
            this.grid.RowHeadersWidth = 51;
            this.grid.RowTemplate.Height = 24;
            this.grid.Size = new System.Drawing.Size(739, 359);
            this.grid.TabIndex = 3;
            // 
            // VentanaConsultar
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1001, 601);
            this.Controls.Add(this.grid);
            this.Controls.Add(this.btnVolver);
            this.Controls.Add(this.lbBuenosAires);
            this.Controls.Add(this.lbProductoDisponible);
            this.Name = "VentanaConsultar";
            this.Text = "VentanaConsultar";
            ((System.ComponentModel.ISupportInitialize)(this.grid)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lbProductoDisponible;
        private System.Windows.Forms.Label lbBuenosAires;
        private System.Windows.Forms.Button btnVolver;
        private System.Windows.Forms.DataGridView grid;
    }
}