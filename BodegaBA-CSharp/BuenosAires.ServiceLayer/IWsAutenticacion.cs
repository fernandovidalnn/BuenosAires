using System.ServiceModel;
using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
	[ServiceContract]
	public interface IWsAutenticacion
	{
		[OperationContract]
        Respuesta Autenticar(string tipousu, string username, string password);
    }
}
