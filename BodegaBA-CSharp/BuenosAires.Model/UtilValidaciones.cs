namespace BuenosAires.Model.Utiles
{
    public static class UtilValidaciones
    {
        public static string NombreSistema = "Sistema Buenos Aires";

        public static string ValidarCampoRequerido(string nombreCampo, string valor)
        {
            if (valor.Trim() == "")
                return $"{nombreCampo} es un campo requerido, por lo que debe tener un valor.";
            return "";
        }
    }
}
