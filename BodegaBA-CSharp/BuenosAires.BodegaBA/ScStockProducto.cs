using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using BuenosAires.BodegaBA.WsStockProductoReference;
using BuenosAires.Model;
using Newtonsoft.Json;
using static BuenosAires.ServiceProxy.ScStockProducto;

namespace BuenosAires.ServiceProxy
{
    public class ScStockProducto
    {
        public class ProductoDisponible
        {

            public int IdProd { get; set; }
            public string NomProd { get; set; }
            public int Cantidad { get; set; }
            public string Estado { get; set; }
        }
        public class RespuestaStockProducto
        {
            public List<ProductoDisponible> Productos { get; set; }
            public static RespuestaStockProducto DesdeJson(string json)
            {
                var productos = JsonConvert.DeserializeObject<List<ProductoDisponible>>(json);
                return new RespuestaStockProducto { Productos = productos };
            }
        }

        public int IdStock = 0;
        public int IdProd = 0;
        public string NomProd = "";
        public int NroFac = 0;
        public string Estado = "";
        public string JsonListaProducto = "";
        public List<ProductoDisponible> ListaProductos { get; set; } = new List<ProductoDisponible>();


        public void CopiarPropiedades(Respuesta resp)
        {
            this.JsonListaProducto = resp.JsonListaProducto;
            if (!string.IsNullOrWhiteSpace(resp.JsonListaProducto))
            {
                RespuestaStockProducto deserializado = RespuestaStockProducto.DesdeJson(resp.JsonListaProducto);
                this.ListaProductos = deserializado.Productos;
            }
        }
        public WsStockProductoClient GetWs()
        {
            var ws = new WsStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            return ws;
        }

        public void StockProducto()
        {
            CopiarPropiedades(GetWs().StockProducto());
        }

    }
}
