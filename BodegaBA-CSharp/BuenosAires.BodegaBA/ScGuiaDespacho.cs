using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using BuenosAires.BodegaBA.WsGuiaDespachoReference;
using BuenosAires.Model;
using Newtonsoft.Json;

namespace BuenosAires.BodegaBA
{
    public class ScGuiaDespacho
    {
        public class GuiaDespachoItem
        {
            public int NroGD { get; set; }
            public string Producto { get; set; }
            public string EstadoGD { get; set; }
            public int NroFac { get; set; }
            public string Cliente { get; set; }
        }

        public class RespuestaGuiaDespacho
        {
            public List<GuiaDespachoItem> Guias { get; set; }

            public static RespuestaGuiaDespacho DesdeJson(string json)
            {
                var guias = JsonConvert.DeserializeObject<List<GuiaDespachoItem>>(json);
                return new RespuestaGuiaDespacho { Guias = guias };
            }
        }

        public string JsonGuiaDespacho = "";
        public List<GuiaDespachoItem> ListaGuias { get; set; } = new List<GuiaDespachoItem>();
        public string Mensaje = "";
        public bool HayErrores = false;

        private WsGuiaDespachoClient GetWs()
        {
            var ws = new WsGuiaDespachoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            return ws;
        }

        private void RecuperarRespuesta(Respuesta resp)
        {
            this.JsonGuiaDespacho = resp.JsonGuiaDespacho;
            this.Mensaje = resp.Mensaje;
            this.HayErrores = resp.HayErrores;

            if (!string.IsNullOrWhiteSpace(resp.JsonGuiaDespacho))
            {
                var deserializado = RespuestaGuiaDespacho.DesdeJson(resp.JsonGuiaDespacho);
                this.ListaGuias = deserializado.Guias;
            }
        }

        public void ObtenerGuias()
        {
            var resp = GetWs().GuiaDespacho();
            RecuperarRespuesta(resp);
        }

        public void ActualizarEstadoGuiaDespacho(int nroGD, string estadoGD)
        {
            var resp = GetWs().ActualizarEstadoGuiaDespacho(nroGD, estadoGD);
            RecuperarRespuesta(resp);
        }
    }
}
