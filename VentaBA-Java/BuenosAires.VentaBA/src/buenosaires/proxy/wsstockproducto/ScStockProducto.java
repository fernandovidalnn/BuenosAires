package buenosaires.proxy.wsstockproducto;

import org.json.simple.JSONValue;
import java.util.ArrayList;
import java.util.List;
import buenosaires.proxy.wsstockproducto.XmlSerializer;
import org.json.simple.JSONObject;

public class ScStockProducto {
    
    private ArrayList<StockProducto> lista;
    
    
    //CONSTRUCTOR
    public ScStockProducto() {
    }
    
     // Getter
    public List<StockProducto> getProductos() {
        WsStockProducto ws = new WsStockProducto();
        var port = ws.getBasicHttpBindingIWsStockProducto();
        Respuesta resp = port.stockProducto();
        Object jsonObject = JSONValue.parse(resp.jsonListaProducto.getValue());
        JSONObject lista = (JSONObject)jsonObject;
        /*
        lista.get(jsonObject)
                  
        grid.Columns["IdProd"].HeaderText = "ID Producto";
        grid.Columns["NomProd"].HeaderText = "Nombre";
        grid.Columns["Cantidad"].HeaderText = "Cantidad";  // ✅ NUEVA COLUMNA
        grid.Columns["Estado"].HeaderText = "Estado";
        
        XmlSerializer.deserialize(resp.jsonListaProducto, clazz)
        
        */
        return null;
    }

    /*
    public void setProductos(List<Producto> productos) {
        this.productos = productos;
    }
    
    public void agregarProducto(Producto producto) {
        this.productos.add(producto);
    }
    */
    
}

