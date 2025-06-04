package buenosaires.proxy.wsstockproducto;

import org.json.simple.JSONValue;
import java.util.ArrayList;
import java.util.List;
import buenosaires.proxy.wsstockproducto.XmlSerializer;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

public class ScStockProducto {
    
    private ArrayList<StockProducto> lista;
    
    
    //CONSTRUCTOR
    public ScStockProducto() {
    }
    
     // Getter
    public List<FilaStockProducto> getProductos() {
        WsStockProducto ws = new WsStockProducto();
        var port = ws.getBasicHttpBindingIWsStockProducto();
        Respuesta resp = port.stockProducto();
        JSONArray arreglo = (JSONArray) JSONValue.parse(resp.jsonListaProducto.getValue());
        
        List<FilaStockProducto> productos = new ArrayList<>();
        for (Object obj : arreglo) {
            JSONObject item = (JSONObject) obj;

            FilaStockProducto producto = new FilaStockProducto();
            producto.IdProd = ((Long) item.get("idprod")).intValue();
            producto.NomProd = (String) item.get("nomprod");
            producto.NroFac = ((Long) item.get("cantidad")).intValue();
            producto.Estado = (String) item.get("estado");
            
            // Solo si decides agregar cantidad y usarla en la clase
            // producto.Cantidad = ((Long) item.get("cantidad")).intValue(); 

            productos.add(producto);
        }
        /*JSONObject lista = (JSONObject)jsonObject;
        lista.get(jsonObject)
                  
        grid.Columns["IdProd"].HeaderText = "ID Producto";
        grid.Columns["NomProd"].HeaderText = "Nombre";
        grid.Columns["Cantidad"].HeaderText = "Cantidad";  // ✅ NUEVA COLUMNA
        grid.Columns["Estado"].HeaderText = "Estado";
        
        XmlSerializer.deserialize(resp.jsonListaProducto, clazz)
        
        */
        return productos;
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

