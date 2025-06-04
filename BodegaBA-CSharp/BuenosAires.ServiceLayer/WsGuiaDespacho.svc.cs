using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using System.Net.Http;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;
using Newtonsoft.Json;


namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de clase "WsGuiaDespacho" en el código, en svc y en el archivo de configuración a la vez.
    // NOTA: para iniciar el Cliente de prueba WCF para probar este servicio, seleccione WsGuiaDespacho.svc o WsGuiaDespacho.svc.cs en el Explorador de soluciones e inicie la depuración.
    public class WsGuiaDespacho : IWsGuiaDespacho
    {
        public Respuesta GuiaDespacho()
        {
            var resp = new Respuesta();
            resp.Accion = "guiadespacho";
            resp.Mensaje = "";
            resp.JsonGuiaDespacho = "";

            string apiUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/obtener_guias_despacho";
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonGuiaDespacho = response.Content.ReadAsStringAsync().Result;
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
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsGuiaDespacho.GuiaDespacho", ex);
                return resp;
            }
            
        }

        public Respuesta ActualizarEstadoGuiaDespacho(int nroGD, string estadoGD)
        {
            var resp = new Respuesta();
            resp.Accion = "actualizar_estado";
            resp.Mensaje = "";

            string apiUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/obtener_guias_despacho";

            try
            {
                using (HttpClient client = new HttpClient())
                {
                    var body = new
                    {
                        nroGD = nroGD,
                        estadoGD = estadoGD
                    };

                    var json = JsonConvert.SerializeObject(body);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    HttpResponseMessage response = client.PostAsync(apiUrl, content).Result;

                    if (response.IsSuccessStatusCode)
                    {
                        // ✅ ahora la API retorna una lista, no un objeto
                        resp.JsonGuiaDespacho = response.Content.ReadAsStringAsync().Result;
                        resp.Mensaje = $"Guía {nroGD} actualizada a estado {estadoGD}";
                        return resp;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = $"Error en la API al actualizar guía: {(int)response.StatusCode} - {response.ReasonPhrase}";
                        return resp;
                    }
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsGuiaDespacho.ActualizarEstadoGuiaDespacho", ex);
                return resp;
            }
        }



    }
}
