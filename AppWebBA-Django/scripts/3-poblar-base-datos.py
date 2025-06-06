from django.db import connection

SP_OBTENER_EQUIPOS_EN_BODEGA = """
CREATE OR ALTER PROCEDURE [dbo].[SP_OBTENER_EQUIPOS_EN_BODEGA]
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        p.idprod,
        p.nomprod,
        ISNULL(COUNT(s.idstock), 0) AS cantidad,
        CASE 
            WHEN COUNT(s.idstock) > 0 THEN 'Disponible'
            ELSE 'Agotado'
        END AS estado
    FROM 
        Producto p
        LEFT JOIN StockProducto s ON p.idprod = s.idprod AND s.nrofac IS NULL
    WHERE
        p.idprod < 9999
    GROUP BY 
        p.idprod, p.nomprod
END
"""

SP_OBTENER_PRODUCTOS = """
CREATE PROCEDURE [dbo].[SP_OBTENER_PRODUCTOS]
AS
BEGIN
	SET NOCOUNT ON;

	SELECT * FROM Producto WHERE idprod <> 9999
END
"""

SP_OBTENER_SOLICITUDES_DE_SERVICIO = """
CREATE PROCEDURE [dbo].[SP_OBTENER_SOLICITUDES_DE_SERVICIO]
	@tipousu VARCHAR(50),
	@rut     VARCHAR(50)
AS
BEGIN
	/*
		Ejemplos de ejecucion del procedimiento:
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '6666-6'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '7777-7'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Técnico', '8888-8'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Cliente', '1111-1'
		EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Todos', ''
	*/

	SET NOCOUNT ON;

	IF (@tipousu = 'Técnico')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			pertec.rut = @rut
		ORDER BY 
			usucli.first_name

	IF (@tipousu = 'Cliente')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		WHERE
			percli.rut = @rut
		ORDER BY 
			usutec.first_name

	IF (@tipousu = 'Todos')
		SELECT 
			sol.nrosol, 
			usucli.first_name + ' '  + usucli.last_name AS nomcli, 
			sol.tiposol,
			sol.fechavisita, 
			'10:00:00'                                  AS hora,
			usutec.first_name + ' '  + usutec.last_name AS nomtec,
			sol.descsol       + ': ' + fac.descfac      AS descser,
			sol.estadosol
		FROM 
			SolicitudServicio sol 
			INNER JOIN Factura       fac    ON sol.nrofac     = fac.nrofac
			INNER JOIN PerfilUsuario percli ON fac.rutcli     = percli.rut
			INNER JOIN PerfilUsuario pertec ON sol.ruttec     = pertec.rut
			INNER JOIN auth_user     usucli ON percli.user_id =  usucli.id
			INNER JOIN auth_user     usutec ON pertec.user_id =  usutec.id
		ORDER BY
			usucli.first_name,
			usutec.first_name

END
"""

SP_OBTENER_TODOS_LOS_USUARIOS = """
CREATE PROCEDURE [dbo].[SP_OBTENER_TODOS_LOS_USUARIOS]
AS
BEGIN
	SET NOCOUNT ON;
	
	SELECT 
		*
	FROM 
		PerfilUsuario per
		INNER JOIN auth_user usu ON per.user_id = usu.id
END
"""


SP_RESERVAR_EQUIPO_ANWO = """
CREATE PROCEDURE [dbo].[SP_RESERVAR_EQUIPO_ANWO]
    @nroserieanwo NVARCHAR(100),
	@reservado NVARCHAR(1)
AS
BEGIN
	/*
		Ejemplos de ejecucion del procedimiento:
		
        EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'S'
        SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'S'

		EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'N'
        SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'N'
	*/

    SET NOCOUNT ON;

    UPDATE AnwoStockProducto
    SET reservado = @reservado
    WHERE nroserieanwo = @nroserieanwo;
END
"""
#------------------------------------------
#agregado por fernando obtener factura-------------------
SP_OBTENER_FACTURAS = """
CREATE PROCEDURE [dbo].[SP_OBTENER_FACTURAS]
    @rut VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        fac.nrofac,
        usu.first_name + ' ' + usu.last_name AS cliente,
        fac.fechafac,
        fac.descfac AS descripcion,
        fac.monto,
        ISNULL(gd.nrogd, 0) AS nroGD,
        ISNULL(gd.estadogd, 'Sin Guía') AS estadoGD,
        ISNULL(ss.nrosol, 0) AS nroSS,
        ISNULL(ss.estadosol, 'Sin Servicio') AS estadoSS
    FROM Factura fac
        INNER JOIN PerfilUsuario per ON fac.rutcli = per.rut
        INNER JOIN auth_user usu ON per.user_id = usu.id
        LEFT JOIN GuiaDespacho gd ON fac.nrofac = gd.nrofac
        LEFT JOIN SolicitudServicio ss ON fac.nrofac = ss.nrofac
    WHERE
        @rut = 'admin' OR fac.rutcli = @rut
    ORDER BY fac.fechafac DESC
END
"""

#agregado por fernando ----crear factura--------------------------
SP_CREAR_FACTURA = """
CREATE PROCEDURE [dbo].[SP_CREAR_FACTURA]
    @rutcli VARCHAR(50),
    @idprod INT = NULL,              -- ← ahora opcional
    @monto INT,
    @descfac NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @nrofac INT;
    SELECT @nrofac = ISNULL(MAX(nrofac), 0) + 1 FROM Factura;

    INSERT INTO Factura (nrofac, rutcli, idprod, fechafac, descfac, monto)
    VALUES (@nrofac, @rutcli, @idprod, GETDATE(), @descfac, @monto);

    SELECT @nrofac AS nrofac; -- Retorna el número de factura creado
END
"""

#agregado por fernando crear solicitud de instalación-------------------
SP_CREAR_SOLICITUD_SERVICIO = """
CREATE PROCEDURE [dbo].[SP_CREAR_SOLICITUD_SERVICIO]
    @nrofac INT,
    @fechavisita DATE,
    @descsol NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @ruttec NVARCHAR(50);
    DECLARE @nrosol INT;

    -- Obtener el técnico con menos solicitudes asignadas
    SELECT TOP 1 @ruttec = per.rut
    FROM PerfilUsuario per
    WHERE per.tipousu = 'Técnico'
    ORDER BY (
        SELECT COUNT(*) 
        FROM SolicitudServicio ss 
        WHERE ss.ruttec = per.rut
    ) ASC;

    -- Obtener nuevo número de solicitud
    SELECT @nrosol = ISNULL(MAX(nrosol), 0) + 1 FROM SolicitudServicio;

    -- Insertar nueva solicitud de servicio
    INSERT INTO SolicitudServicio (
        nrosol,
        nrofac,
        tiposol,
        fechavisita,
        ruttec,
        descsol,
        estadosol
    )
    VALUES (
        @nrosol,
        @nrofac,
        'Instalación',
        @fechavisita,
        @ruttec,
        @descsol,
        'Modificada'
    );
END
"""
#agregado por fernando crear guía de despacho--------------------------
SP_CREAR_GUIA_DESPACHO = """
CREATE PROCEDURE [dbo].[SP_CREAR_GUIA_DESPACHO]
    @nrofac INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @nrogd INT;
    DECLARE @idprod INT;

    -- Obtener el producto relacionado con la factura
    SELECT @idprod = idprod FROM Factura WHERE nrofac = @nrofac;

    -- Obtener nuevo número de guía
    SELECT @nrogd = ISNULL(MAX(nrogd), 0) + 1 FROM GuiaDespacho;

    -- Insertar la guía de despacho en estado 'EnBodega'
    INSERT INTO GuiaDespacho (nrogd, nrofac, idprod, estadogd)
    VALUES (@nrogd, @nrofac, @idprod, 'EnBodega');

    -- Devolver el número de guía generado (opcional)
    SELECT @nrogd AS nroGD;
END
"""


#----------------------------------------------
# agregado por fernando actualizar solicitud de servicio --------------------------
SP_ACTUALIZAR_SOLICITUD_DE_SERVICIO = """
CREATE PROCEDURE [dbo].[SP_ACTUALIZAR_SOLICITUD_DE_SERVICIO]
    @nrosol INT,
    @fechavisita DATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE SolicitudServicio
    SET fechavisita = @fechavisita,
        estadosol = 'Modificada'
    WHERE nrosol = @nrosol;
END
"""
# -------------------------------------------------------------------------------



def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def run():

    # Poblar tabla Producto

    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (1,N'Aire Wifi 9000 btu',  N'Enfría 9-16 m2',     299990,'images/0001.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (2,N'Split Inv 12000 btu', N'Frío/Calor AR12',    450000,'images/0002.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (3,N'Anwo VP',             N'9000 Virus Protect', 288990,'images/0003.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (4,N'Anwo Portátil',       N'12000 btu f/c',      131990,'images/0004.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (5,N'GPORT-14',            N'Anwo 14000 btu',     399990,'images/0005.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (6,N'Kendal 12000',        N'Climat 22-24 m2',    335990,'images/0006.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (7,N'Kendal Wifi 4000',    N'Climat 32-34 m2',    335990,'images/0006.png');")
    exec_sql("INSERT INTO dbo.Producto (idprod, nomprod, descprod, precio, imagen) VALUES (8,N'Anwo 12000',          N'Climat 42-44 m2',    335990,'images/0006.png');")
    exec_sql("INSERT INTO Producto (idprod, nomprod, descprod, precio, imagen) VALUES (9999, 'Servicio Técnico', 'Solicitud de mantención o reparación', 25000, 'images/servicio.png');")

    # Poblar tabla PerfilUsuario

    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'1234-5',  N'Superusuario',  N'La Florida',  1);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'1111-1',  N'Cliente',       N'La Florida',  2);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'2222-2',  N'Cliente',       N'Santiago',    3);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'3333-3',  N'Cliente',       N'Providencia', 4);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'4444-4',  N'Cliente',       N'Las Condes',  5);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'5555-5',  N'Cliente',       N'Maipú',       6);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'6666-6',  N'Técnico',       N'Cerro Navia', 7);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'7777-7',  N'Técnico',       N'Peñalolén',   8);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'8888-8',  N'Técnico',       N'La Reina',    9);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'9999-9',  N'Bodeguero',     N'La Florida',  10);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'0000-0',  N'Administrador', N'La Reina',    11);")
    exec_sql("INSERT INTO dbo.PerfilUsuario (rut, tipousu, dirusu, user_id) VALUES (N'4321-0',  N'Vendedor',      N'Las Condes',  12);")

    # Poblar tabla Factura

    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (1, N'1111-1', 1, CAST('20220223' AS datetime), N'Aire Wifi 9000 btu',  25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (2, N'2222-2', 2, CAST('20220224' AS datetime), N'Split Inv 12000 btu', 450000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (3, N'3333-3', 4, CAST('20220303' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (4, N'4444-4', 4, CAST('20220308' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (5, N'5555-5', 4, CAST('20220315' AS datetime), N'Anwo Portátil',       25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (6, N'1111-1', 5, CAST('20220327' AS datetime), N'Mantención',          25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (7, N'1111-1', 5, CAST('20220403' AS datetime), N'GPORT-14',            25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (8, N'1111-1', 3, CAST('20220408' AS datetime), N'Anwo VP',             25000);")
    exec_sql("INSERT INTO dbo.Factura (nrofac, rutcli, idprod, fechafac, descfac, monto) VALUES (9, N'1111-1', 5, CAST('20220415' AS datetime), N'GPORT-14',            25000);")

    # Poblar tabla GuiaDespacho

    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (11, 1, 1, N'Entregado');")
    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (22, 2, 2, N'Depachado');")
    exec_sql("INSERT INTO dbo.GuiaDespacho (nrogd, nrofac, idprod, estadogd) VALUES (88, 8, 3, N'EnBodega');")

    # Poblar tabla SolicitudServicio

    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (111, 1, N'Instalación', CAST('20220302 09:00' AS datetime), N'6666-6', N'Instalar equipo', N'Cerrada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (222, 2, N'Instalación', CAST('20220303 10:00' AS datetime), N'6666-6', N'Instalar equipo', N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (333, 3, N'Mantención',  CAST('20220310 15:00' AS datetime), N'6666-6', N'Cambiar enchufe', N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (444, 4, N'Mantención',  CAST('20220315 09:00' AS datetime), N'6666-6', N'Limpiar filtro',  N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (555, 5, N'Reparación',  CAST('20220322 17:00' AS datetime), N'6666-6', N'Reparar equipo',  N'Aceptada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (666, 6, N'Mantención',  CAST('20220403 11:00' AS datetime), N'7777-7', N'Limpiar filtro',  N'Cerrada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (777, 7, N'Reparación',  CAST('20220410 16:00' AS datetime), N'6666-6', N'Reparar aire',    N'Modificada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (888, 8, N'Instalación', CAST('20220415 10:00' AS datetime), N'7777-7', N'Instalar equipo', N'Modificada');")
    exec_sql("INSERT INTO dbo.SolicitudServicio (nrosol, nrofac, tiposol, fechavisita, ruttec, descsol, estadosol) VALUES (999, 9, N'Reparación',  CAST('20220422 18:00' AS datetime), N'8888-8', N'Enchufe quemado', N'Aceptada');")

    # Poblar tabla StockProducto

    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (11111, 1, 1);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (22222, 2, 2);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (88888, 3, 8);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90001, 1, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90002, 3, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90003, 4, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90004, 6, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90005, 1, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90006, 3, null);")
    exec_sql("INSERT INTO dbo.StockProducto (idstock, idprod, nrofac) VALUES (90007, 4, null);")

    # Poblar tabla AnwoStockProducto

    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A1', 'Aire Anwo 111',  '500000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A2', 'Aire Anwo 222',  '400000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A3', 'Aire Anwo 333',  '300000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A4', 'Aire Anwo 444',  '200000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A5', 'Aire Anwo 555',  '500000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A6', 'Aire Anwo 666',  '400000', 'N');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A7', 'Aire Anwo 777',  '300000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A8', 'Aire Anwo 888',  '200000', 'S');")
    exec_sql("INSERT INTO dbo.ANWOSTOCKPRODUCTO (NROSERIEANWO, NOMPRODANWO, PRECIOANWO, RESERVADO) VALUES ('A9', 'Aire Anwo 999',  '500000', 'N');")

    try:
        exec_sql(SP_OBTENER_EQUIPOS_EN_BODEGA)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_PRODUCTOS)
    except:
        pass

    try:
        exec_sql(SP_OBTENER_SOLICITUDES_DE_SERVICIO)
    except:
        pass
    
    try:
        exec_sql(SP_OBTENER_TODOS_LOS_USUARIOS)
    except:
        pass
    
    try:
        exec_sql(SP_RESERVAR_EQUIPO_ANWO)
    except:
        pass
    
    
    #agregado por fernando--inicio----------------------------------
    try:
        exec_sql(SP_OBTENER_FACTURAS)
    except Exception as e:
        print("Error al crear SP_OBTENER_FACTURAS:", e)
    
    try:
        exec_sql(SP_CREAR_FACTURA)
    except Exception as e:
        print("Error al crear SP_CREAR_FACTURA:", e)
        
    try:
        exec_sql(SP_CREAR_SOLICITUD_SERVICIO)
    except Exception as e:
        print("Error al crear SP_CREAR_SOLICITUD_SERVICIO:", e)
        
    try:
        exec_sql(SP_CREAR_GUIA_DESPACHO)
    except Exception as e:
        print("Error al crear SP_CREAR_GUIA_DESPACHO:", e)
        
    try:
        exec_sql(SP_ACTUALIZAR_SOLICITUD_DE_SERVICIO)
    except Exception as e:
        print("Error al crear SP_ACTUALIZAR_SOLICITUD_DE_SERVICIO:", e)




    #agregado por fernando---fin---------------------------------

