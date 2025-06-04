﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de interfaz "IWsGuiaDespacho" en el código y en el archivo de configuración a la vez.
    [ServiceContract]
    public interface IWsGuiaDespacho
    {
        [OperationContract]
        Respuesta GuiaDespacho();

        [OperationContract]
        Respuesta ActualizarEstadoGuiaDespacho(int nroGD, string estadoGD); // ✅ Agregado
    }
}
