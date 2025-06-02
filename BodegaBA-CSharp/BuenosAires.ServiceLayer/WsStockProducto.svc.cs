using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using System.Net.Http;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;


namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de clase "WsStockProducto" en el código, en svc y en el archivo de configuración a la vez.
    // NOTA: para iniciar el Cliente de prueba WCF para probar este servicio, seleccione WsStockProducto.svc o WsStockProducto.svc.cs en el Explorador de soluciones e inicie la depuración.
    public class WsStockProducto : IWsStockProducto
    {
        public Respuesta StockProducto()
        {
            var resp = new Respuesta();
            resp.Accion = "stockProducto";
            resp.Mensaje = "";
            resp.JsonListaProducto = "";


            string apiUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/obtener_equipos_en_bodega";

            try {
                using (HttpClient client = new HttpClient()) {
                    HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonListaProducto = response.Content.ReadAsStringAsync().Result;
                        return resp;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = $"Error en la API (No fue posible conectarse a la base de datos, contactese con el administrador): {(int)response.StatusCode} - {response.ReasonPhrase}";
                        return resp;
                    }
                }       
            }
            catch (Exception ex) {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsStockProducto.StockProducto", ex);
                return resp;
            }
        }
    }
}
