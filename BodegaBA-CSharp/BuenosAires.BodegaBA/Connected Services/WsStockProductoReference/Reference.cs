﻿//------------------------------------------------------------------------------
// <auto-generated>
//     Este código fue generado por una herramienta.
//     Versión de runtime:4.0.30319.42000
//
//     Los cambios en este archivo podrían causar un comportamiento incorrecto y se perderán si
//     se vuelve a generar el código.
// </auto-generated>
//------------------------------------------------------------------------------

namespace BuenosAires.BodegaBA.WsStockProductoReference {
    
    
    [System.CodeDom.Compiler.GeneratedCodeAttribute("System.ServiceModel", "4.0.0.0")]
    [System.ServiceModel.ServiceContractAttribute(ConfigurationName="WsStockProductoReference.IWsStockProducto")]
    public interface IWsStockProducto {
        
        [System.ServiceModel.OperationContractAttribute(Action="http://tempuri.org/IWsStockProducto/StockProducto", ReplyAction="http://tempuri.org/IWsStockProducto/StockProductoResponse")]
        BuenosAires.Model.Respuesta StockProducto();
        
        [System.ServiceModel.OperationContractAttribute(Action="http://tempuri.org/IWsStockProducto/StockProducto", ReplyAction="http://tempuri.org/IWsStockProducto/StockProductoResponse")]
        System.Threading.Tasks.Task<BuenosAires.Model.Respuesta> StockProductoAsync();
    }
    
    [System.CodeDom.Compiler.GeneratedCodeAttribute("System.ServiceModel", "4.0.0.0")]
    public interface IWsStockProductoChannel : BuenosAires.BodegaBA.WsStockProductoReference.IWsStockProducto, System.ServiceModel.IClientChannel {
    }
    
    [System.Diagnostics.DebuggerStepThroughAttribute()]
    [System.CodeDom.Compiler.GeneratedCodeAttribute("System.ServiceModel", "4.0.0.0")]
    public partial class WsStockProductoClient : System.ServiceModel.ClientBase<BuenosAires.BodegaBA.WsStockProductoReference.IWsStockProducto>, BuenosAires.BodegaBA.WsStockProductoReference.IWsStockProducto {
        
        public WsStockProductoClient() {
        }
        
        public WsStockProductoClient(string endpointConfigurationName) : 
                base(endpointConfigurationName) {
        }
        
        public WsStockProductoClient(string endpointConfigurationName, string remoteAddress) : 
                base(endpointConfigurationName, remoteAddress) {
        }
        
        public WsStockProductoClient(string endpointConfigurationName, System.ServiceModel.EndpointAddress remoteAddress) : 
                base(endpointConfigurationName, remoteAddress) {
        }
        
        public WsStockProductoClient(System.ServiceModel.Channels.Binding binding, System.ServiceModel.EndpointAddress remoteAddress) : 
                base(binding, remoteAddress) {
        }
        
        public BuenosAires.Model.Respuesta StockProducto() {
            return base.Channel.StockProducto();
        }
        
        public System.Threading.Tasks.Task<BuenosAires.Model.Respuesta> StockProductoAsync() {
            return base.Channel.StockProductoAsync();
        }
    }
}
