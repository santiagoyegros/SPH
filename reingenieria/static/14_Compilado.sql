CREATE OR ALTER DATABASE reingenieria SET COMPATIBILITY_LEVEL =  130 go
USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamientomensualeros_trg]    Script Date: 25/7/2019 22:23:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[relevamientomensualeros_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_sueldo int;
		DECLARE @p_mensuCantidad int;
		DECLARE @p_relevamientocab_id int;
		DECLARE @p_id int;

		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_sueldo="value" from OpenJson(@json) where "key"='sueldo' and "value"!='None';
		select @p_mensuCantidad="value" from OpenJson(@json) where "key"='mensuCantidad' and "value"!='None';
		select @p_relevamientocab_id="value" from OpenJson(@json) where "key"='relevamientocab_id' and "value"!='None';
		select @p_id_tmp="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histrelevamientomensualeros(sueldo,mensuCantidad,relevamientocab_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select sueldo,mensuCantidad,relevamientocab_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_relevamientomensualeros where id=@p_id;
			end
			update dbo.Operarios_histrelevamientomensualeros set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histrelevamientomensualeros(sueldo,mensuCantidad,relevamientocab_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_sueldo,@p_mensuCantidad,@p_relevamientocab_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_relevamientomensualeros set 
					 sueldo=@p_sueldo,mensuCantidad=@p_mensuCantidad,relevamientocab_id=@p_relevamientocab_id where id=@p_id;
			end
			if @delete is not NULL and @delete='True'
			begin
        update Operarios_histrelevamientomensualeros set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_relevamientomensualeros  where id=@p_id;
			end
		end


		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			INSERT INTO dbo.Operarios_relevamientomensualeros(sueldo,mensuCantidad,relevamientocab_id)
			select @p_sueldo,@p_mensuCantidad,@p_relevamientocab_id;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histrelevamientomensualeros(sueldo,mensuCantidad,relevamientocab_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_sueldo,@p_mensuCantidad,@p_relevamientocab_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamientoesp_trg]    Script Date: 25/7/2019 22:23:30 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[relevamientoesp_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_cantHoras nvarchar(max);
		DECLARE @p_tipo_id int;
		DECLARE @p_relevamientocab_id int;
		DECLARE @p_frecuencia nvarchar(max);
		DECLARE @p_id int;
		declare @p_tipo nvarchar(max);

		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_cantHoras="value" from OpenJson(@json) where "key"='cantHoras';
		select @p_tipo_id="value" from OpenJson(@json) where "key"='tipo_id';
		select @p_tipo="value" from OpenJson(@json) where "key"='tipoServicio';
		select @p_relevamientocab_id="value" from OpenJson(@json) where "key"='relevamientocab_id' and "value"!='None';
		select @p_frecuencia="value" from OpenJson(@json) where "key"='frecuencia';
		select @p_id_tmp="value" from OpenJson(@json) where "key"='id' and "value"!='None';

		sELECT @p_tipo_id=id from dbo.Operarios_tiposervicio where tipoServicio like @p_tipo
		if  @p_tipo_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe tipo servicio particular');
		END

		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histrelevamientoesp(cantHoras,tipo_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select cantHoras,tipo_id,relevamientocab_id,frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_relevamientoesp where id=@p_id;
			end
			update dbo.Operarios_histrelevamientoesp set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histrelevamientoesp(cantHoras,tipo_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_cantHoras,@p_tipo_id,@p_relevamientocab_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_relevamientoesp set 
					 cantHoras=@p_cantHoras,tipo_id=@p_tipo_id,relevamientocab_id=@p_relevamientocab_id,frecuencia=@p_frecuencia where id=@p_id;
			end
			if @delete is not NULL and @delete='True'
			begin
        update Operarios_histrelevamientoesp set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_relevamientoesp  where id=@p_id;
				
			end
		end


		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			INSERT INTO dbo.Operarios_relevamientoesp(cantHoras,tipo_id,relevamientocab_id,frecuencia)
			select @p_cantHoras,@p_tipo_id,@p_relevamientocab_id,@p_frecuencia;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histrelevamientoesp(cantHoras,tipo_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_cantHoras,@p_tipo_id,@p_relevamientocab_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END



GO


USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamientodet_trg]    Script Date: 25/7/2019 22:23:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[relevamientodet_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_tipoServPart_id int;
		DECLARE @p_relevamientocab_id int;
		DECLARE @p_domSal time;
		DECLARE @p_domEnt time;
		DECLARE @p_sabSal time;
		DECLARE @p_sabEnt time;
		DECLARE @p_vieSal time;
		DECLARE @p_vieEnt time;
		DECLARE @p_jueSal time;
		DECLARE @p_jueEnt time;
		DECLARE @p_mieSal time;
		DECLARE @p_mieEnt time;
		DECLARE @p_marSal time;
		DECLARE @p_marEnt time;
		DECLARE @p_lunSal time;
		DECLARE @p_lunEnt time;
		DECLARE @p_orden int;
		DECLARE @p_id int;
		declare @p_tipoServPart nvarchar(max);

		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_tipoServPart_id="value" from OpenJson(@json) where "key"='tipoServPart_id';
		select @p_tipoServPart="value" from OpenJson(@json) where "key"='tipoServPart';
		select @p_relevamientocab_id="value" from OpenJson(@json) where "key"='relevamientocab_id' and "value"!='None';
		select @p_domSal="value" from OpenJson(@json) where "key"='domSal' and "value"!='None';
		select @p_domEnt="value" from OpenJson(@json) where "key"='domEnt' and "value"!='None';
		select @p_sabSal="value" from OpenJson(@json) where "key"='sabSal' and "value"!='None';
		select @p_sabEnt="value" from OpenJson(@json) where "key"='sabEnt' and "value"!='None';
		select @p_vieSal="value" from OpenJson(@json) where "key"='vieSal' and "value"!='None';
		select @p_vieEnt="value" from OpenJson(@json) where "key"='vieEnt' and "value"!='None';
		select @p_jueSal="value" from OpenJson(@json) where "key"='jueSal' and "value"!='None';
		select @p_jueEnt="value" from OpenJson(@json) where "key"='jueEnt' and "value"!='None';
		select @p_mieSal="value" from OpenJson(@json) where "key"='mieSal' and "value"!='None';
		select @p_mieEnt="value" from OpenJson(@json) where "key"='mieEnt' and "value"!='None';
		select @p_marSal="value" from OpenJson(@json) where "key"='marSal' and "value"!='None';
		select @p_marEnt="value" from OpenJson(@json) where "key"='marEnt' and "value"!='None';
		select @p_lunSal="value" from OpenJson(@json) where "key"='lunSal' and "value"!='None';
		select @p_lunEnt="value" from OpenJson(@json) where "key"='lunEnt' and "value"!='None';
		select @p_orden="value" from OpenJson(@json) where "key"='orden' and "value"!='None';
		select @p_id_tmp="value" from OpenJson(@json) where "key"='id' and "value"!='None';

		sELECT @p_tipoServPart_id=id from dbo.Operarios_tiposervicioparticular where tipoServicioParticular like @p_tipoServPart
		if  @p_tipoServPart_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe tipo servicio particular');
		END

		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END


		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=@retorno-1;
				INSERT INTO dbo.Operarios_histrelevamientodet(tipoServPart_id,relevamientocab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,orden,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select tipoServPart_id,relevamientocab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,orden,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_relevamientodet where id=@p_id;
			end
			
			update dbo.Operarios_histrelevamientodet set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histrelevamientodet(tipoServPart_id,relevamientocab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,orden,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_tipoServPart_id,@p_relevamientocab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@p_orden,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_relevamientodet set 
					 tipoServPart_id=@p_tipoServPart_id,relevamientocab_id=@p_relevamientocab_id,domSal=@p_domSal,domEnt=@p_domEnt,sabSal=@p_sabSal,sabEnt=@p_sabEnt,vieSal=@p_vieSal,vieEnt=@p_vieEnt,jueSal=@p_jueSal,jueEnt=@p_jueEnt,mieSal=@p_mieSal,mieEnt=@p_mieEnt,marSal=@p_marSal,marEnt=@p_marEnt,lunSal=@p_lunSal,lunEnt=@p_lunEnt,orden=@p_orden where id=@p_id;
			end
			if @delete is not NULL and @delete='True'
			begin
				update Operarios_histrelevamientodet set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_relevamientodet  where id=@p_id;
			end
		end


		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			INSERT INTO dbo.Operarios_relevamientodet(tipoServPart_id,relevamientocab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,orden)
			select @p_tipoServPart_id,@p_relevamientocab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@p_orden;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histrelevamientodet(tipoServPart_id,relevamientocab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,orden,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_tipoServPart_id,@p_relevamientocab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@p_orden,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamientocupohoras_trg]    Script Date: 25/7/2019 22:24:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[relevamientocupohoras_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_tipoHora nvarchar(max);
		DECLARE @p_cantHoras nvarchar(max);
		DECLARE @p_tipoHora_id int;
		DECLARE @p_relevamientocab_id int;
		DECLARE @p_frecuencia nvarchar(max);
		DECLARE @p_id int;
		
		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_cantHoras="value" from OpenJson(@json) where "key"='cantCHoras';
		select @p_tipoHora_id="value" from OpenJson(@json) where "key"='tipoHora_id';
		select @p_tipoHora="value" from OpenJson(@json) where "key"='tipoHora';
		select @p_relevamientocab_id="value" from OpenJson(@json) where "key"='relevamientocab_id' and "value"!='None';
		select @p_frecuencia="value" from OpenJson(@json) where "key"='frecuencia';
		select @p_id_tmp="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		
		sELECT @p_tipoHora_id=id from dbo.Operarios_tipohorario where tipoHorario like @p_tipoHora
		if  @p_tipoHora_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe tipo hORA');
		END


		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histrelevamientocupohoras(cantHoras,tipoHora_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select cantHoras,tipoHora_id,relevamientocab_id,frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_relevamientocupohoras where id=@p_id;
			end
			update dbo.Operarios_histrelevamientocupohoras set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histrelevamientocupohoras(cantHoras,tipoHora_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_cantHoras,@p_tipoHora_id,@p_relevamientocab_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_relevamientocupohoras set 
					 cantHoras=@p_cantHoras,tipoHora_id=@p_tipoHora_id,relevamientocab_id=@p_relevamientocab_id,frecuencia=@p_frecuencia where id=@p_id;
			end
			if @delete is not NULL and @delete='True'
			begin
       	update Operarios_histrelevamientocupohoras set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_relevamientocupohoras  where id=@p_id;
			end

		end


		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@p_relevamientocab_id;
			INSERT INTO dbo.Operarios_relevamientocupohoras(cantHoras,tipoHora_id,relevamientocab_id,frecuencia)
			select @p_cantHoras,@p_tipoHora_id,@p_relevamientocab_id,@p_frecuencia;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histrelevamientocupohoras(cantHoras,tipoHora_id,relevamientocab_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_cantHoras,@p_tipoHora_id,@p_relevamientocab_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END



GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamiento_cab_trg]    Script Date: 31/7/2019 11:53:17 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER PROCEDURE [dbo].[relevamiento_cab_trg]   
  

	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;
		
		Declare @tmp1_vregistro int;
		DECLARE @dp0_id int;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_id_tmp nvarchar(max);
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_tipoSalario nvarchar(max);
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_fechaFin date;
		DECLARE @dp0_fecha datetime2;
		Declare @delete nvarchar(max);
		select @dp0_id_tmp="value" from OpenJson(@json) where "key"='id' and value!='None';
		select @dp0_fecha=cast("value"as date) from OpenJson(@json) where "key"='fechaInicio';
		select @dp0_cantidad="value" from OpenJson(@json) where "key"='cantidad';
		select @dp0_puntoServicio_id="value" from OpenJson(@json) where "key"='puntoServicio_id';
		select @dp0_cantidadHrTotal="value" from OpenJson(@json) where "key"='cantidadHrTotal';
		select @dp0_cantidadHrEsp="value" from OpenJson(@json) where "key"='cantidadHrEsp';
		select @dp0_fechaInicio=cast("value"as date) from OpenJson(@json) where "key"='fechaInicio';
		select @dp0_usuario_id="value" from OpenJson(@json) where "key"='usuario_id' and "value"!='None';
		select @dp0_tipoSalario="value" from OpenJson(@json) where "key"='tipoSalario';
		select @dp0_comentario="value" from OpenJson(@json) where "key"='comentario';
		select @dp0_cantAprendices="value" from OpenJson(@json) where "key"='cantAprendices';
		select @dp0_estado="value" from OpenJson(@json) where "key"='estado';
		if @dp0_estado is NULL
		begin
			SET @dp0_estado='Aprobado'
		end
		sELECT @dp0_tipoSalario_id=id from dbo.Operarios_tiposalario where tipoSalario like @dp0_tipoSalario
		if  @dp0_tipoSalario_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe tipo servicio');
		END
		
		if  @dp0_id_tmp  is not NULL and @dp0_id_tmp!='None'
		BEGIN
			select @dp0_id=cast(@dp0_id_tmp as int)
		END

		if  @dp0_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histrelevamientocab where vactual_id=@dp0_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histrelevamientocab(fecha,cantidad,puntoServicio_id,cantidadHrTotal,
				cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,
				estado,fechaFin,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select fecha,cantidad,puntoServicio_id,cantidadHrTotal,
				cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,
				estado,fechaFin,@fechaCambio,NULL,@tmp1_vregistro,@dp0_id from dbo.Operarios_relevamientocab where id=@dp0_id;
			end

			update dbo.Operarios_histrelevamientocab set vfechaFin=@fechaCambio where vactual_id=@dp0_id and vregistro=@tmp1_vregistro;
			set @tmp1_vregistro=@tmp1_vregistro+1;
			INSERT INTO dbo.Operarios_histrelevamientocab(fecha,cantidad,puntoServicio_id,cantidadHrTotal,
				cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,
				estado,fechaFin,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,
				@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,
				@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp1_vregistro,@dp0_id

			update dbo.Operarios_relevamientocab set 
				fecha= @dp0_fecha,
				cantidad= @dp0_cantidad,
				puntoServicio_id= @dp0_puntoServicio_id,
				cantidadHrTotal= @dp0_cantidadHrTotal,
				cantidadHrEsp= @dp0_cantidadHrEsp,
				fechaInicio= @dp0_fechaInicio,
				usuario_id= @dp0_usuario_id,
				tipoSalario_id= @dp0_tipoSalario_id,
				comentario= @dp0_comentario,
				cantAprendices= @dp0_cantAprendices,
				estado= @dp0_estado,
				fechaFin= @dp0_fechaFin where id=@dp0_id;
		end

		if  @dp0_id is NULL
		begin
			set @tmp1_vregistro=1;
			INSERT INTO dbo.Operarios_relevamientocab(fecha,cantidad,puntoServicio_id,cantidadHrTotal,
				cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,
				estado,fechaFin)
			select @dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,
				@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,
				@dp0_estado,@dp0_fechaFin;

			set @dp0_id=SCOPE_IDENTITY();

			INSERT INTO dbo.Operarios_histrelevamientocab(fecha,cantidad,puntoServicio_id,cantidadHrTotal,
				cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,
				estado,fechaFin,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,
				@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,
				@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp1_vregistro,@dp0_id
		end
		Select @retorno as resultado;

END		


USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[relevamiento_manager]    Script Date: 25/7/2019 21:36:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[relevamiento_manager]   
	@json_cab nvarchar(max),
	@json_det nvarchar(max),
	@json_men nvarchar(max),
	@json_cup nvarchar(max),
	@json_esp nvarchar(max),
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;
	DECLARE @TransactionName varchar(20) = 'Transactional';
	Declare @err_msg nvarchar(max);
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @fechaCambio datetime;
		SET @fechaCambio=CURRENT_TIMESTAMP;
			DECLARE @RC int;
			DECLARE @cab int;
			DECLARE @tmp nvarchar(max);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_cab);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_det);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_men);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_cup);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_esp);
			EXECUTE @RC = [dbo].[relevamiento_cab_trg] @json_cab,@fechaCambio,0
			/*det*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_det)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[relevamientodet_trg] @tmp,@fechaCambio,@retorno
				end



			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
			/*ESP*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_esp)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[relevamientoesp_trg] @tmp,@fechaCambio,@retorno
				end
			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
			/*MENSUALEROS*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_men)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[relevamientomensualeros_trg] @tmp,@fechaCambio,@retorno
				end
			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt


			/*CUPO HORAS*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_cup)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[relevamientocupohoras_trg] @tmp,@fechaCambio,@retorno
				end
			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
			SET @retorno=0;
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH
		set @err_msg=ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into dbo.infolog(fechaHora,info) values(current_timestamp, @err_msg);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_cab);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_det);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_men);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_cup);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_esp);
	END CATCH
	Select @retorno as resultado;

END		

GO


GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[puntoServicio_trigger]    Script Date: 24/7/2019 12:04:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER  PROCEDURE [dbo].[puntoServicio_trigger]   
  

	@p_id int,
	@p_CodPuntoServicio nvarchar(max),
	@p_NombrePServicio nvarchar(max),
	@p_DireccionContrato nvarchar(max),
	@p_Barrios nvarchar(max),
	@p_Contacto nvarchar(max),
	@p_MailContacto nvarchar(max),
	@p_TelefonoContacto nvarchar(max),
	@p_Coordenadas nvarchar(max),
	@p_Ciudad_Nombre nvarchar(max),
	@p_Cliente_Nombre nvarchar(max),
	@p_NumeroMarcador nvarchar(max),
	@tmp1_vregistro int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;

	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		SELECT top 1 @p_Ciudad_id=id from dbo.Operarios_ciudad where NombreCiudad=@p_Ciudad_Nombre ;
		SELECT top 1 @p_Cliente_id=id from dbo.Operarios_cliente where Cliente=@p_Cliente_Nombre;
		DECLARE @p_vfecha_inicio datetime;
		DECLARE @p_vfecha_fin datetime;
		DECLARE @p_vregistro int;
		Declare @fechaCambio datetime;

		SET @fechaCambio=CURRENT_TIMESTAMP;
	
		
		



		/* 1 - Punto de Servicio*/
				
				select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histpuntoservicio where vactual_id=@p_id;
				if @tmp1_vregistro is NULL
				begin
					set @tmp1_vregistro=1;
					INSERT INTO [dbo].[Operarios_histpuntoservicio]
					   ([CodPuntoServicio],[NombrePServicio],[DireccionContrato]
					   ,[Barrios],[Contacto],[MailContacto]
					   ,[TelefonoContacto],[Coordenadas],[NumeroMarcador]
					   ,[vfechaInicio],[vfechaFin],[vregistro]
					   ,[Ciudad_id],[Cliente_id],[vactual_id])
					SELECT 
						[CodPuntoServicio],[NombrePServicio],[DireccionContrato],
						[Barrios],[Contacto],[MailContacto],
						[TelefonoContacto],[Coordenadas],[NumeroMarcador],
						@fechaCambio,NULL,1,
						[Ciudad_id],[Cliente_id],@p_id
						from dbo.Operarios_puntoservicio where id=@p_id;
				end

				update dbo.Operarios_histpuntoservicio set vfechaFin=@fechaCambio where vactual_id=@p_id;

				update dbo.Operarios_puntoservicio set
					CodPuntoServicio=@p_CodPuntoServicio,
					NombrePServicio=@p_NombrePServicio,
					DireccionContrato=@p_DireccionContrato,
					Barrios=@p_Barrios,
					Contacto=@p_Contacto,
					MailContacto=@p_MailContacto,
					TelefonoContacto=@p_TelefonoContacto,
					Coordenadas=@p_Coordenadas,
					Ciudad_id=@p_Ciudad_id,
					Cliente_id=@p_Cliente_id,
					NumeroMarcador=@p_NumeroMarcador
					where id=@p_id;

				INSERT INTO dbo.Operarios_histpuntoservicio (CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro,vactual_id)
				VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp1_vregistro+1,@p_id);




			COMMIT TRANSACTION @TransactionName;
			SET @retorno=0;
	END TRY 
	BEGIN CATCH 
		print error_message();
		SELECT ERROR_MESSAGE() AS ErrorMessage
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;

	END CATCH

	Select @retorno as resultado;

END	
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[planificacionope_trg]    Script Date: 26/7/2019 11:06:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[planificacionope_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_total nvarchar(max);
		DECLARE @p_corte nvarchar(max);
		DECLARE @p_planificacionCab_id int;
		DECLARE @p_especialista_id int;
		DECLARE @p_sal time;
		DECLARE @p_ent time;
		DECLARE @p_fer bit ;
		DECLARE @p_dom bit ;
		DECLARE @p_sab bit ;
		DECLARE @p_vie bit ;
		DECLARE @p_jue bit ;
		DECLARE @p_mie bit ;
		DECLARE @p_mar bit ;
		DECLARE @p_lun bit ;
		DECLARE @p_cantidad int;
		DECLARE @p_id int;
		Declare @p_especialista nvarchar(max);
		

		select @p_total="value" from OpenJson(@json) where "key"='total';
		select @p_corte="value" from OpenJson(@json) where "key"='corte';
		select @p_planificacionCab_id="value" from OpenJson(@json) where "key"='planificacionCab_id';
		select @p_especialista_id="value" from OpenJson(@json) where "key"='especialista_id';
		select @p_especialista="value" from OpenJson(@json) where "key"='especialista';
		select @p_sal="value" from OpenJson(@json) where "key"='sal' and "value"!='None';
		select @p_ent="value" from OpenJson(@json) where "key"='ent' and "value"!='None';
		select @p_fer="value" from OpenJson(@json) where "key"='fer';
		select @p_dom="value" from OpenJson(@json) where "key"='dom';
		select @p_sab="value" from OpenJson(@json) where "key"='sab';
		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_vie="value" from OpenJson(@json) where "key"='vie';
		select @p_jue="value" from OpenJson(@json) where "key"='jue';
		select @p_mie="value" from OpenJson(@json) where "key"='mie';
		select @p_mar="value" from OpenJson(@json) where "key"='mar';
		select @p_lun="value" from OpenJson(@json) where "key"='lun';
		select @p_cantidad="value" from OpenJson(@json) where "key"='cantidad';
		select @p_id="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		
		sELECT @p_especialista_id=id from dbo.Operarios_especializacion where especializacion like @p_especialista
		if  @p_especialista_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe especialidad');
		END
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histplanificacioncab where vactual_id=@p_planificacionCab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histplanificacionope(total,corte,planificacionCab_id,especialista_id,sal,ent,fer,dom,sab,vie,jue,mie,mar,lun,cantidad,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select total,corte,planificacionCab_id,especialista_id,sal,ent,fer,dom,sab,vie,jue,mie,mar,lun,cantidad,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_planificacionope where id=@p_id;
			end
			update dbo.Operarios_histplanificacionope set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histplanificacionope(total,corte,planificacionCab_id,especialista_id,sal,ent,fer,dom,sab,vie,jue,mie,mar,lun,cantidad,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_total,@p_corte,@p_planificacionCab_id,@p_especialista_id,@p_sal,@p_ent,@p_fer,@p_dom,@p_sab,@p_vie,@p_jue,@p_mie,@p_mar,@p_lun,@p_cantidad,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_planificacionope set 
					 total=@p_total,corte=@p_corte,planificacionCab_id=@p_planificacionCab_id,especialista_id=@p_especialista_id,sal=@p_sal,ent=@p_ent,fer=@p_fer,dom=@p_dom,sab=@p_sab,vie=@p_vie,jue=@p_jue,mie=@p_mie,mar=@p_mar,lun=@p_lun,cantidad=@p_cantidad where id=@p_id;
			end
			if @delete is not NULL and @delete='True'
			begin
        update Operarios_histplanificacionope set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_planificacionope  where id=@p_id;
			end
		end
		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histplanificacioncab where vactual_id=@p_planificacionCab_id;
			INSERT INTO dbo.Operarios_planificacionope(total,corte,planificacionCab_id,especialista_id,sal,ent,fer,dom,sab,vie,jue,mie,mar,lun,cantidad)
			select @p_total,@p_corte,@p_planificacionCab_id,@p_especialista_id,@p_sal,@p_ent,@p_fer,@p_dom,@p_sab,@p_vie,@p_jue,@p_mie,@p_mar,@p_lun,@p_cantidad;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histplanificacionope(total,corte,planificacionCab_id,especialista_id,sal,ent,fer,dom,sab,vie,jue,mie,mar,lun,cantidad,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_total,@p_corte,@p_planificacionCab_id,@p_especialista_id,@p_sal,@p_ent,@p_fer,@p_dom,@p_sab,@p_vie,@p_jue,@p_mie,@p_mar,@p_lun,@p_cantidad,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END



GO


USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[planificacionesp_trg]    Script Date: 26/7/2019 11:06:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[planificacionesp_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_fechaLimpProf date;
		DECLARE @p_cantHoras nvarchar(max);
		DECLARE @p_tipo_id int;
		DECLARE @p_planificacionCab_id int;
		DECLARE @p_especialista_id int;
		DECLARE @p_especialista nvarchar(max);
		DECLARE @p_tipo nvarchar(max);
		DECLARE @p_frecuencia nvarchar(max) ;
		DECLARE @p_id int;

		select @p_fechaLimpProf="value" from OpenJson(@json) where "key"='fechaLimpProf' and "value"!='None';
		select @p_cantHoras="value" from OpenJson(@json) where "key"='cantHoras';
		select @p_tipo="value" from OpenJson(@json) where "key"='tipo';
		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_planificacionCab_id="value" from OpenJson(@json) where "key"='planificacionCab_id';
		select @p_especialista="value" from OpenJson(@json) where "key"='especialista';
		select @p_frecuencia="value" from OpenJson(@json) where "key"='frecuencia';
		select @p_id="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		
		sELECT @p_especialista_id=id from dbo.Operarios_especializacion where especializacion like @p_especialista
		if  @p_especialista_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe especialidad');
		END

		sELECT @p_tipo_id=id from dbo.Operarios_tiposervicio where tipoServicio like @p_tipo
		if  @p_tipo_id is NULL
		BEGIN
			RAISERROR(15000,0,0,'NO existe tipo servicio particular');
		END




		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histplanificacioncab where vactual_id=@p_planificacionCab_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histplanificacionesp(fechaLimpProf,cantHoras,tipo_id,planificacionCab_id,especialista_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select fechaLimpProf,cantHoras,tipo_id,planificacionCab_id,especialista_id,frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_planificacionesp where id=@p_id;
			end
			update dbo.Operarios_histplanificacionesp set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histplanificacionesp(fechaLimpProf,cantHoras,tipo_id,planificacionCab_id,especialista_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_fechaLimpProf,@p_cantHoras,@p_tipo_id,@p_planificacionCab_id,@p_especialista_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_planificacionesp set 
					 fechaLimpProf=@p_fechaLimpProf,cantHoras=@p_cantHoras,tipo_id=@p_tipo_id,planificacionCab_id=@p_planificacionCab_id,especialista_id=@p_especialista_id,frecuencia=@p_frecuencia where id=@p_id;
			end

			if @delete is not NULL and @delete='True'
			begin
        update Operarios_histplanificacionesp set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_planificacionesp  where id=@p_id;
			end
			

		end
		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histplanificacioncab where vactual_id=@p_planificacionCab_id;
			INSERT INTO dbo.Operarios_planificacionesp(fechaLimpProf,cantHoras,tipo_id,planificacionCab_id,especialista_id,frecuencia)
			select @p_fechaLimpProf,@p_cantHoras,@p_tipo_id,@p_planificacionCab_id,@p_especialista_id,@p_frecuencia;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histplanificacionesp(fechaLimpProf,cantHoras,tipo_id,planificacionCab_id,especialista_id,frecuencia,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_fechaLimpProf,@p_cantHoras,@p_tipo_id,@p_planificacionCab_id,@p_especialista_id,@p_frecuencia,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[planificacioncab_trg]    Script Date: 31/7/2019 11:53:14 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[planificacioncab_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_puntoServicio_id int;
		DECLARE @p_cantHorasEsp nvarchar(max);
		DECLARE @p_cantHorasNoc nvarchar(max);
		DECLARE @p_cantHoras nvarchar(max);
		DECLARE @p_cantidad int;
		DECLARE @p_usuario_id int;
		DECLARE @p_fecha datetime2 ;
		DECLARE @p_id int;

		select @p_puntoServicio_id="value" from OpenJson(@json) where "key"='puntoServicio_id';
		select @p_cantHorasEsp="value" from OpenJson(@json) where "key"='cantHorasEsp';
		select @p_cantHorasNoc="value" from OpenJson(@json) where "key"='cantHorasNoc';
		select @p_cantHoras="value" from OpenJson(@json) where "key"='cantHoras';
		select @p_usuario_id="value" from OpenJson(@json) where "key"='usuario_id' and "value"!='None';
		select @p_cantidad="value" from OpenJson(@json) where "key"='cantidad';
		select @p_fecha="value" from OpenJson(@json) where "key"='fecha' and "value"!='None';
		select @p_id="value" from OpenJson(@json) where "key"='id';
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if @p_fecha is NULL
		begin
			SET @p_fecha=CURRENT_TIMESTAMP
		end


		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histplanificacioncab where vactual_id=@p_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histplanificacioncab(puntoServicio_id,cantHorasEsp,cantHorasNoc,cantHoras,cantidad,fecha,vfechaInicio,vfechaFin,vregistro,vactual_id,rePlanificar,usuario_id)
				select puntoServicio_id,cantHorasEsp,cantHorasNoc,cantHoras,cantidad,fecha,@fechaCambio,NULL,@tmp1_vregistro,@p_id,rePlanificar,usuario_id from dbo.Operarios_planificacioncab where id=@p_id;
			end
			update dbo.Operarios_histplanificacioncab set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro;
			set @tmp1_vregistro=@tmp1_vregistro+1;
			INSERT INTO dbo.Operarios_histplanificacioncab(puntoServicio_id,cantHorasEsp,cantHorasNoc,cantHoras,cantidad,fecha,vfechaInicio,vfechaFin,vregistro,vactual_id,rePlanificar,usuario_id)
			select @p_puntoServicio_id,@p_cantHorasEsp,@p_cantHorasNoc,@p_cantHoras,@p_cantidad,@p_fecha,@fechaCambio,NULL,@tmp1_vregistro,@p_id,'False',@p_usuario_id
			update dbo.Operarios_planificacioncab set 
				 puntoServicio_id=@p_puntoServicio_id,cantHorasEsp=@p_cantHorasEsp,cantHorasNoc=@p_cantHorasNoc,cantHoras=@p_cantHoras,cantidad=@p_cantidad,fecha=@p_fecha, rePlanificar='False',usuario_id=@p_usuario_id where id=@p_id;
		end
		if  @p_id is NULL
		begin
			set @tmp1_vregistro=1;
			INSERT INTO dbo.Operarios_planificacioncab(puntoServicio_id,cantHorasEsp,cantHorasNoc,cantHoras,cantidad,fecha,rePlanificar,usuario_id)
			select @p_puntoServicio_id,@p_cantHorasEsp,@p_cantHorasNoc,@p_cantHoras,@p_cantidad,@p_fecha,'False',@p_usuario_id;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histplanificacioncab(puntoServicio_id,cantHorasEsp,cantHorasNoc,cantHoras,cantidad,fecha,vfechaInicio,vfechaFin,vregistro,vactual_id,rePlanificar,usuario_id)
			select @p_puntoServicio_id,@p_cantHorasEsp,@p_cantHorasNoc,@p_cantHoras,@p_cantidad,@p_fecha,@fechaCambio,NULL,@tmp1_vregistro,@p_id,'False',@p_usuario_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[planificacion_manager]    Script Date: 24/7/2019 12:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR CREATE OR ALTER  PROCEDURE [dbo].[planificacion_manager]   
	@json_cab nvarchar(max),
	@json_ope nvarchar(max),
	@json_esp nvarchar(max),
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;

	DECLARE @TransactionName varchar(20) = 'Transactional';
	Declare @err_msg nvarchar(max);
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @fechaCambio datetime;
		SET @fechaCambio=CURRENT_TIMESTAMP;
			DECLARE @RC int;
			DECLARE @tmp nvarchar(max);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_cab);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_ope);
			insert into infolog(fechaHora,info) values(@fechaCambio,@json_esp);

			EXECUTE @RC = [dbo].[planificacioncab_trg] @json_cab,@fechaCambio,@retorno
			/*det*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_ope)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[planificacionope_trg] @tmp,@fechaCambio,@retorno
				end



			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
			/*ESP*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT "value" FROM OpenJson(@json_esp)
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @tmp
			WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @tmp is not NULL and @tmp!='{}'
				begin
					EXECUTE @RC = [dbo].[planificacionesp_trg] @tmp,@fechaCambio,@retorno
				end
			FETCH NEXT FROM cursorIt INTO @tmp
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH
		set @err_msg=ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into dbo.infolog(fechaHora,info) values(current_timestamp, @err_msg);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_cab);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_ope);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_esp);
	END CATCH
	Select @retorno as resultado;

END	

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asig_jefeyfiscal_trigger]    Script Date: 25/7/2019 10:05:05 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER PROCEDURE [dbo].[asig_jefeyfiscal_trigger]   
  

	@p_userJefe_id int,
	@p_userFiscal_id int,
	@veregistro int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
	SET NOCOUNT ON;
	Declare @error nvarchar(max);
	declare @nuevoId int;
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		 INSERT INTO [dbo].[Operarios_asigjefefiscal]([userFiscal_id],[userJefe_id])
		 select @p_userFiscal_id,@p_userJefe_id where not exists(select * from
		 dbo.Operarios_asigjefefiscal where userFiscal_id=@p_userFiscal_id and userJefe_id=@p_userJefe_id)
		 set @nuevoId=SCOPE_IDENTITY();
		 select @veregistro=max(vregistro) from dbo.Operarios_histasigjefefiscal where userFiscal_id=@p_userFiscal_id and userJefe_id=@p_userJefe_id;
		 if @veregistro is NUll
		 begin
			set @veregistro=0;
		 end
		 INSERT INTO [dbo].[Operarios_histasigjefefiscal]([userFiscal_id],[userJefe_id],[vfechaFin],[vfechaInicio],[vregistro],vactual_id)
		 values( @p_userFiscal_id,@p_userJefe_id,NULL,CURRENT_TIMESTAMP,@veregistro+1,@nuevoId); 
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH 
		set @error=ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into infolog(fechaHora,info) values(CURRENT_TIMESTAMP,@error)
	END CATCH

	Select @retorno as resultado;

END	
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asignaciondet_trg]    Script Date: 26/7/2019 11:06:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[asignaciondet_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_perfil_id int;
		DECLARE @p_supervisor bit;
		DECLARE @p_totalHoras nvarchar(max);		
		DECLARE @p_operario_id int;
		DECLARE @p_asignacionCab_id int;

		DECLARE @p_domSal time;
		DECLARE @p_domEnt time;
		DECLARE @p_sabSal time;
		DECLARE @p_sabEnt time;
		DECLARE @p_vieSal time;
		DECLARE @p_vieEnt time;
		DECLARE @p_jueSal time;
		DECLARE @p_jueEnt time;
		DECLARE @p_mieSal time;
		DECLARE @p_mieEnt time;
		DECLARE @p_marSal time;
		DECLARE @p_marEnt time;
		DECLARE @p_lunSal time;
		DECLARE @p_lunEnt time;
		DECLARE @p_id int;

		select @p_perfil_id="value" from OpenJson(@json) where "key"='perfil_id' and "value"!='None';
		select @p_supervisor="value" from OpenJson(@json) where "key"='supervisor';
		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_totalHoras="value" from OpenJson(@json) where "key"='totalHoras' and "value"!='None' and "value"!='00';
		select @p_fechaInicio=cast("value" as date) from OpenJson(@json) where "key"='fechaInicio' and "value"!='None';
		select @p_fechaFin=cast("value" as date) from OpenJson(@json) where "key"='fechaFin' and "value"!='None';	
		select @p_operario_id="value" from OpenJson(@json) where "key"='operario_id' and "value"!='None';
		select @p_asignacionCab_id="value" from OpenJson(@json) where "key"='asignacionCab_id';
		select @p_domSal=cast("value" as time) from OpenJson(@json) where "key"='domSal' and "value"!='None';
		select @p_domEnt=cast("value" as time) from OpenJson(@json) where "key"='domEnt' and "value"!='None';
		select @p_sabSal=cast("value" as time) from OpenJson(@json) where "key"='sabSal' and "value"!='None';
		select @p_sabEnt=cast("value" as time) from OpenJson(@json) where "key"='sabEnt' and "value"!='None';
		select @p_vieSal=cast("value" as time) from OpenJson(@json) where "key"='vieSal' and "value"!='None';
		select @p_vieEnt=cast("value" as time) from OpenJson(@json) where "key"='vieEnt' and "value"!='None';
		select @p_jueSal=cast("value" as time) from OpenJson(@json) where "key"='jueSal' and "value"!='None';
		select @p_jueEnt=cast("value" as time) from OpenJson(@json) where "key"='jueEnt' and "value"!='None';
		select @p_mieSal=cast("value" as time) from OpenJson(@json) where "key"='mieSal' and "value"!='None';
		select @p_mieEnt=cast("value" as time) from OpenJson(@json) where "key"='mieEnt' and "value"!='None';
		select @p_marSal=cast("value" as time) from OpenJson(@json) where "key"='marSal' and "value"!='None';
		select @p_marEnt=cast("value" as time) from OpenJson(@json) where "key"='marEnt' and "value"!='None';
		select @p_lunSal=cast("value" as time) from OpenJson(@json) where "key"='lunSal' and "value"!='None';
		select @p_lunEnt=cast("value" as time) from OpenJson(@json) where "key"='lunEnt' and "value"!='None';
		select @p_id="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasignacioncab where vactual_id=@p_asignacionCab_id
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_asignaciondet where id=@p_id;
			end
			update dbo.Operarios_histasignaciondet set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro-1;
			if @delete is not NULL and @delete='False'
			begin
				INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select @p_perfil_id,@p_supervisor,@p_fechaFin,@p_totalHoras,@p_fechaInicio,@p_operario_id,@p_asignacionCab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@p_id
				update dbo.Operarios_asignaciondet set 
					 perfil_id=@p_perfil_id,supervisor=@p_supervisor,fechaFin=@p_fechaFin,totalHoras=@p_totalHoras,fechaInicio=@p_fechaInicio,operario_id=@p_operario_id,asignacionCab_id=@p_asignacionCab_id,domSal=@p_domSal,domEnt=@p_domEnt,sabSal=@p_sabSal,sabEnt=@p_sabEnt,vieSal=@p_vieSal,vieEnt=@p_vieEnt,jueSal=@p_jueSal,jueEnt=@p_jueEnt,mieSal=@p_mieSal,mieEnt=@p_mieEnt,marSal=@p_marSal,marEnt=@p_marEnt,lunSal=@p_lunSal,lunEnt=@p_lunEnt where id=@p_id;
			end

			if @delete is not NULL and @delete='True'
			begin
        -- insert en hist updat hist set vactual_id=NULL where vactual_id=@p_id; delete where  where id=@p_id;
				--INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
				--select @p_perfil_id,@p_supervisor,@p_fechaFin,@p_totalHoras,@p_fechaInicio,@p_operario_id,@p_asignacionCab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@p_id
			    update Operarios_histasignaciondet set vactual_id=NULL where vactual_id=@p_id;
				delete from dbo.Operarios_asignaciondet  where id=@p_id;
			end

			

		end
		if  @p_id is NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasignacioncab where vactual_id=@p_asignacionCab_id;
			INSERT INTO dbo.Operarios_asignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt)
			select @p_perfil_id,@p_supervisor,@p_fechaFin,@p_totalHoras,@p_fechaInicio,@p_operario_id,@p_asignacionCab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_perfil_id,@p_supervisor,@p_fechaFin,@p_totalHoras,@p_fechaInicio,@p_operario_id,@p_asignacionCab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asignacioncab_trg]    Script Date: 26/7/2019 11:06:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[asignacioncab_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_usuario_id int;
		DECLARE @p_puntoServicio_id int;
		DECLARE @p_totalasignado nvarchar(max);
		DECLARE @p_fechaUltimaMod datetime2 ;
		DECLARE @p_id int;

		select @p_usuario_id="value" from OpenJson(@json) where "key"='usuario_id' and "value"!='None';
		select @p_puntoServicio_id="value" from OpenJson(@json) where "key"='puntoServicio_id' and "value"!='None';
		select @p_totalasignado="value" from OpenJson(@json) where "key"='totalasignado' and "value"!='None';
		select @p_fechaUltimaMod="value" from OpenJson(@json) where "key"='fechaUltimaMod' and  "value"!='None' and "value"!='00';

		if @p_fechaUltimaMod is NULL
		begin
			set @p_fechaUltimaMod = CURRENT_TIMESTAMP
		end

		select @p_id=cast("value" as int) from OpenJson(@json) where "key"='id' and "value"!='None';
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasignacioncab where vactual_id=@p_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histasignacioncab(usuario_id,puntoServicio_id,totalasignado,fechaUltimaMod,vfechaInicio,vfechaFin,vregistro,vactual_id,reAsignar)
				select usuario_id,puntoServicio_id,totalasignado,fechaUltimaMod,@fechaCambio,NULL,@tmp1_vregistro,@p_id,'False' from dbo.Operarios_asignacioncab where id=@p_id;
			end
			update dbo.Operarios_histasignacioncab set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro;
			set @tmp1_vregistro=@tmp1_vregistro+1;
			INSERT INTO dbo.Operarios_histasignacioncab(usuario_id,puntoServicio_id,totalasignado,fechaUltimaMod,vfechaInicio,vfechaFin,vregistro,vactual_id,reAsignar)
			select @p_usuario_id,@p_puntoServicio_id,@p_totalasignado,@p_fechaUltimaMod,@fechaCambio,NULL,@tmp1_vregistro,@p_id,'False'
			update dbo.Operarios_asignacioncab set 
				 usuario_id=@p_usuario_id,puntoServicio_id=@p_puntoServicio_id,totalasignado=@p_totalasignado,fechaUltimaMod=@p_fechaUltimaMod where id=@p_id;
		end
		if  @p_id is NULL
		begin
			set @tmp1_vregistro=1;
			INSERT INTO dbo.Operarios_asignacioncab(usuario_id,puntoServicio_id,totalasignado,fechaUltimaMod)
			select @p_usuario_id,@p_puntoServicio_id,@p_totalasignado,@p_fechaUltimaMod;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histasignacioncab(usuario_id,puntoServicio_id,totalasignado,fechaUltimaMod,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_usuario_id,@p_puntoServicio_id,@p_totalasignado,@p_fechaUltimaMod,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asignacion_manager]    Script Date: 9/8/2019 08:39:30 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create or CREATE OR ALTER PROCEDURE [dbo].[asignacion_manager]   
	@json_cab nvarchar(max),
	@asig_cab int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;

	DECLARE @TransactionName varchar(20) = 'Transactional';
	Declare @err_msg nvarchar(max);
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @fechaCambio datetime;
		DECLARE @hrm0_id int;
		DECLARE @hrm0_lunEnt time;
		DECLARE @hrm0_lunSal time;
		DECLARE @hrm0_marEnt time;
		DECLARE @hrm0_marSal time;
		DECLARE @hrm0_mieEnt time;
		DECLARE @hrm0_mieSal time;
		DECLARE @hrm0_jueEnt time;
		DECLARE @hrm0_jueSal time;
		DECLARE @hrm0_vieEnt time;
		DECLARE @hrm0_vieSal time;
		DECLARE @hrm0_sabEnt time;
		DECLARE @hrm0_sabSal time;
		DECLARE @hrm0_domEnt time;
		DECLARE @hrm0_domSal time;
		DECLARE @hrm0_asignacionCab_id int;
		DECLARE @hrm0_operario_id int;
		DECLARE @hrm0_fechaInicio date;
		DECLARE @hrm0_totalHoras nvarchar(max);
		DECLARE @hrm0_fechaFin date;
		DECLARE @hrm0_supervisor bit;
		DECLARE @hrm0_perfil_id int;
		declare @tmp1_vregistro int;
		DECLARE @hrm0_eliminado nvarchar(max);
		SET @fechaCambio=CURRENT_TIMESTAMP;
			DECLARE @RC int;
			DECLARE @tmp int;
			
			EXECUTE @RC = [dbo].[asignacioncab_trg] @json_cab,@fechaCambio,@retorno

			INSERT INTO dbo.Operarios_asignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,eliminado)
			select perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,eliminado from dbo.Operarios_asignaciondettemp where asignacionCab_id=@asig_cab and eliminado='False'
				


			/*det no borrados*/
			DECLARE cursorIt CURSOR LOCAL FOR SELECT id,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,eliminado FROM dbo.Operarios_asignaciondet where asignacionCab_id=@asig_cab
			OPEN cursorIt
			FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@hrm0_eliminado
			WHILE @@FETCH_STATUS = 0
			BEGIN
				select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasignacioncab where vactual_id=@asig_cab
				if @tmp1_vregistro is NULL
				begin
					set @tmp1_vregistro=1;
					INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
					select perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@hrm0_id from dbo.Operarios_asignaciondet where id=@hrm0_id;
				end
				update dbo.Operarios_histasignaciondet set vfechaFin=@fechaCambio where vactual_id=@hrm0_id and vregistro=@tmp1_vregistro-1;
				if @hrm0_eliminado is not NULL and @hrm0_eliminado=0
				begin
					INSERT INTO dbo.Operarios_histasignaciondet(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,vfechaInicio,vfechaFin,vregistro,vactual_id)
					select @hrm0_perfil_id,@hrm0_supervisor,@hrm0_fechaFin,@hrm0_totalHoras,@hrm0_fechaInicio,@hrm0_operario_id,@hrm0_asignacionCab_id,@hrm0_domSal,@hrm0_domEnt,@hrm0_sabSal,@hrm0_sabEnt,@hrm0_vieSal,@hrm0_vieEnt,@hrm0_jueSal,@hrm0_jueEnt,@hrm0_mieSal,@hrm0_mieEnt,@hrm0_marSal,@hrm0_marEnt,@hrm0_lunSal,@hrm0_lunEnt,@fechaCambio,NULL,@tmp1_vregistro,@hrm0_id
				end
				if @hrm0_eliminado is not NULL and @hrm0_eliminado=1
				begin
        			update Operarios_histasignaciondet set vactual_id=NULL where vactual_id=@hrm0_id;
					delete from dbo.Operarios_asignaciondet  where id=@hrm0_id;
				end
			FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@hrm0_eliminado
			END
			CLOSE cursorIt
			DEALLOCATE cursorIt
			delete from dbo.Operarios_asignaciondettemp where asignacionCab_id=@asig_cab


		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH
		set @err_msg=ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into dbo.infolog(fechaHora,info) values(current_timestamp, @err_msg);
		insert into infolog(fechaHora,info) values(@fechaCambio,@json_cab);
	END CATCH
	Select @retorno as resultado;

END	

GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asigjefefiscal_trg]    Script Date: 24/7/2019 12:04:03 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[asigjefefiscal_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_userJefe_id int;
		DECLARE @p_userFiscal_id int ;
		DECLARE @p_id int;

		select @p_userJefe_id="value" from OpenJson(@json) where "key"='userJefe_id';
		select @p_userFiscal_id="value" from OpenJson(@json) where "key"='userFiscal_id';
		select @p_id="value" from OpenJson(@json) where "key"='id';
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasigjefefiscal where vactual_id=@p_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histasigjefefiscal(userJefe_id,userFiscal_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select userJefe_id,userFiscal_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_asigjefefiscal where id=@p_id;
			end
			update dbo.Operarios_histasigjefefiscal set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro;
			set @tmp1_vregistro=@tmp1_vregistro+1;
			INSERT INTO dbo.Operarios_histasigjefefiscal(userJefe_id,userFiscal_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_userJefe_id,@p_userFiscal_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
			update dbo.Operarios_asigjefefiscal set 
				 userJefe_id=@p_userJefe_id,userFiscal_id=@p_userFiscal_id where id=@p_id;
		end
		if  @p_id is NULL
		begin
			set @tmp1_vregistro=1;
			INSERT INTO dbo.Operarios_asigjefefiscal(userJefe_id,userFiscal_id)
			select @p_userJefe_id,@p_userFiscal_id;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histasigjefefiscal(userJefe_id,userFiscal_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_userJefe_id,@p_userFiscal_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END

GO


USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asigjefefisc_des_trigger]    Script Date: 24/7/2019 15:43:59 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER  PROCEDURE [dbo].[asigjefefisc_des_trigger]   
  

	@p_userJefe_id int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;
	DECLARE @TransactionName varchar(20) = 'Transactional';
	declare @err nvarchar(max);
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @fechaCambio datetime;
		SET @fechaCambio=CURRENT_TIMESTAMP;
		update dbo.Operarios_histasigjefefiscal set vfechaFin=@fechaCambio,vactual_id=NULL where userJefe_id=@p_userJefe_id and vfechaFin is NULL
		delete from dbo.Operarios_asigjefefiscal where userJefe_id=@p_userJefe_id;
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH 
		set @err= ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into dbo.infolog(fechaHora,info) values(CURRENT_TIMESTAMP,@err);
	END CATCH

	Select @retorno as resultado;

END	



USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asigfiscalpuntoservicio_trg]    Script Date: 24/7/2019 12:03:58 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER   PROCEDURE [dbo].[asigfiscalpuntoservicio_trg]   
	@json nvarchar(max),
	@fechaCambio datetime,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_userFiscal_id int;
		DECLARE @p_puntoServicio_id int;
		DECLARE @p_id int;

		select @p_userFiscal_id="value" from OpenJson(@json) where "key"='userFiscal_id';
		select @p_puntoServicio_id="value" from OpenJson(@json) where "key"='puntoServicio_id';
		select @p_id="value" from OpenJson(@json) where "key"='id';
		if  @p_id_tmp  is not NULL and @p_id_tmp!='None'
		BEGIN
			select @p_id=cast(@p_id_tmp as int)
		END
		if  @p_id is not NULL
		begin
			select @tmp1_vregistro=max(vregistro) from dbo.Operarios_histasigfiscalpuntoservicio where vactual_id=@p_id;
			if @tmp1_vregistro is NULL
			begin
				set @tmp1_vregistro=1;
				INSERT INTO dbo.Operarios_histasigfiscalpuntoservicio(userFiscal_id,puntoServicio_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
				select userFiscal_id,puntoServicio_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id from dbo.Operarios_asigfiscalpuntoservicio where id=@p_id;
			end
			update dbo.Operarios_histasigfiscalpuntoservicio set vfechaFin=@fechaCambio where vactual_id=@p_id and vregistro=@tmp1_vregistro;
			set @tmp1_vregistro=@tmp1_vregistro+1;
			INSERT INTO dbo.Operarios_histasigfiscalpuntoservicio(userFiscal_id,puntoServicio_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_userFiscal_id,@p_puntoServicio_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
			update dbo.Operarios_asigfiscalpuntoservicio set 
				 userFiscal_id=@p_userFiscal_id,puntoServicio_id=@p_puntoServicio_id where id=@p_id;
		end
		if  @p_id is NULL
		begin
			set @tmp1_vregistro=1;
			INSERT INTO dbo.Operarios_asigfiscalpuntoservicio(userFiscal_id,puntoServicio_id)
			select @p_userFiscal_id,@p_puntoServicio_id;
			set @p_id=SCOPE_IDENTITY();
			INSERT INTO dbo.Operarios_histasigfiscalpuntoservicio(userFiscal_id,puntoServicio_id,vfechaInicio,vfechaFin,vregistro,vactual_id)
			select @p_userFiscal_id,@p_puntoServicio_id,@fechaCambio,NULL,@tmp1_vregistro,@p_id
		end
		SET @retorno=0;
		Select @retorno as resultado;
END


go

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asig_psfiscal_trigger]    Script Date: 24/7/2019 15:44:21 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER  PROCEDURE [dbo].[asig_psfiscal_trigger]   
  

	@p_userFiscal_id int,
	@p_puntoServ_id int,
	@veregistro int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
	SET NOCOUNT ON;
	Declare @error nvarchar(max);
	declare @nuevoId int;
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		 INSERT INTO [dbo].[Operarios_asigfiscalpuntoservicio](puntoServicio_id,userFiscal_id)
		 select @p_puntoServ_id,@p_userFiscal_id where not exists(select * from
		 dbo.Operarios_asigfiscalpuntoservicio where userFiscal_id=@p_userFiscal_id and puntoServicio_id=@p_puntoServ_id)
		 set @nuevoId=SCOPE_IDENTITY();
		 select @veregistro=max(vregistro) from dbo.Operarios_histasigfiscalpuntoservicio where userFiscal_id=@p_userFiscal_id and puntoServicio_id=@p_puntoServ_id;
		 if @veregistro is NUll
		 begin
			set @veregistro=0;
		 end
		 set @veregistro=@veregistro+1;
		 INSERT INTO [dbo].[Operarios_histasigfiscalpuntoservicio](puntoServicio_id,userFiscal_id,[vfechaFin],[vfechaInicio],[vregistro],vactual_id)
		 values( @p_puntoServ_id,@p_userFiscal_id,NULL,CURRENT_TIMESTAMP,@veregistro,@nuevoId); 
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH 
		set @error=ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into infolog(fechaHora,info) values(CURRENT_TIMESTAMP,@error)
	END CATCH

	Select @retorno as resultado;

END	
go

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asigpsfisc_des_trigger]    Script Date: 24/7/2019 15:44:45 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR CREATE OR ALTER  PROCEDURE [dbo].[asigpsfisc_des_trigger]   
  

	@p_userFiscal_id int,
	@retorno int OUTPUT
	--@operario int
AS   
	
  BEGIN
  SET NOCOUNT ON;
	DECLARE @TransactionName varchar(20) = 'Transactional';
	declare @err nvarchar(max);
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @fechaCambio datetime;
		SET @fechaCambio=CURRENT_TIMESTAMP;
		update dbo.Operarios_histasigfiscalpuntoservicio set vfechaFin=@fechaCambio,vactual_id=NULL where userFiscal_id=@p_userFiscal_id and vfechaFin is NULL
		delete from dbo.Operarios_asigfiscalpuntoservicio where userFiscal_id=@p_userFiscal_id;
		COMMIT TRANSACTION @TransactionName;
		SET @retorno=0;
	END TRY 
	BEGIN CATCH 
		set @err= ERROR_MESSAGE();
		ROLLBACK TRAN @TransactionName; 
		SET @retorno=1;
		insert into dbo.infolog(fechaHora,info) values(CURRENT_TIMESTAMP,@err);
	END CATCH

	Select @retorno as resultado;

END	
go

USE [reingenieria]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_hd_asignacioncab]    Script Date: 25/7/2019 19:46:55 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[trg_vrs_Operarios_hd_asignacioncab]
ON [dbo].[Operarios_asignacioncab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @dp1_id int;
		DECLARE @dp0_id int;
		DECLARE @reasignar bit;
		DECLARE @od_reasignar bit;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT id,reAsignar FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp1_id,@reasignar
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE cursorDt CURSOR LOCAL FOR SELECT id,reAsignar FROM deleted where id=@dp1_id
			OPEN cursorDt
			FETCH NEXT FROM cursorDt INTO @dp0_id,@od_reasignar 
			WHILE @@FETCH_STATUS = 0
			BEGIN
				if @reasignar=@od_reasignar
				BEGIN
					update dbo.Operarios_asignacioncab set reAsignar='False' where id=@dp1_id;
				END
            FETCH NEXT FROM cursorDt INTO @dp0_id,@od_reasignar
			END
		FETCH NEXT FROM cursorIt INTO @dp1_id,@reasignar
		END
	COMMIT TRANSACTION @TransactionName;
	END TRY 
	BEGIN CATCH 
		print error_message();
		SELECT ERROR_MESSAGE() AS ErrorMessage
		ROLLBACK TRAN @TransactionName; 
	END CATCH
	CLOSE cursorIt
	DEALLOCATE cursorIt
END	



go
USE [reingenieria]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_hd_planificacioncab]    Script Date: 25/7/2019 19:46:40 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[trg_vrs_Operarios_hd_planificacioncab]
ON [dbo].[Operarios_planificacioncab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @dp2_id int;
        DECLARE @replanificar bit;
		DECLARE @dp0_id int;
        DECLARE @od_replanificar bit;


		DECLARE cursorIt CURSOR LOCAL FOR SELECT id,rePlanificar FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp2_id,@replanificar
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE cursorDt CURSOR LOCAL FOR SELECT id,rePlanificar FROM deleted where id=@dp2_id
			OPEN cursorDt
			FETCH NEXT FROM cursorDt INTO @dp0_id,@od_replanificar
			WHILE @@FETCH_STATUS = 0
			BEGIN
				if @od_replanificar=@replanificar
				BEGIN
					update dbo.Operarios_planificacioncab set rePlanificar='False' where id=@dp0_id;
				END
            FETCH NEXT FROM cursorDt INTO @dp0_id,@od_replanificar
			END
		   FETCH NEXT FROM cursorIt INTO @dp2_id,@replanificar
		END
		COMMIT TRANSACTION @TransactionName;
	END TRY 
	BEGIN CATCH 
		print error_message();
		SELECT ERROR_MESSAGE() AS ErrorMessage
		ROLLBACK TRAN @TransactionName; 
	END CATCH
	CLOSE cursorIt
	DEALLOCATE cursorIt
END	

go

USE [reingenieria]
GO
/****** Object:  Trigger [dbo].[trg_header_relevamientocab]    Script Date: 25/7/2019 19:46:30 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[trg_header_relevamientocab]
ON [dbo].[Operarios_relevamientocab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		
		DECLARE @dp0_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		declare @dp0_puntoServicio_id int;
		DECLARE @dp1_cantidadHrTotal nvarchar(max);

		DECLARE cursorIt CURSOR LOCAL FOR SELECT id,cantidadHrTotal,puntoServicio_id FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_cantidadHrTotal,@dp0_puntoServicio_id
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE cursorDt CURSOR LOCAL FOR SELECT cantidadHrTotal FROM deleted where id=@dp0_id
            OPEN cursorDt
            FETCH NEXT FROM cursorDt INTO @dp1_cantidadHrTotal
            WHILE @@FETCH_STATUS = 0
            BEGIN
                if(@dp1_cantidadHrTotal!=@dp0_cantidadHrTotal)
                BEGIN
				
					CREATE OR ALTER  TABLE [dbo].[Operarios_planificacioncab] DISABLE TRIGGER trg_vrs_Operarios_hd_planificacioncab;
					CREATE OR ALTER  TABLE [dbo].[Operarios_asignacioncab]    DISABLE TRIGGER trg_vrs_Operarios_hd_asignacioncab;
                    UPDATE [dbo].[Operarios_planificacioncab] set rePlanificar='True' where puntoServicio_id=@dp0_puntoServicio_id;
                    UPDATE [dbo].[Operarios_asignacioncab] set reAsignar='True' where puntoServicio_id=@dp0_puntoServicio_id;
					CREATE OR ALTER  TABLE [dbo].[Operarios_planificacioncab] ENABLE TRIGGER trg_vrs_Operarios_hd_planificacioncab;
					CREATE OR ALTER  TABLE [dbo].[Operarios_asignacioncab]    ENABLE TRIGGER trg_vrs_Operarios_hd_asignacioncab;
                END
            FETCH NEXT FROM cursorDt INTO @dp1_cantidadHrTotal
            END		
		FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_cantidadHrTotal,@dp0_puntoServicio_id
		END

		COMMIT TRANSACTION @TransactionName;
	END TRY 
	BEGIN CATCH 
		print error_message();
		SELECT ERROR_MESSAGE() AS ErrorMessage
		ROLLBACK TRAN @TransactionName; 
	END CATCH
	CLOSE cursorIt
	DEALLOCATE cursorIt
END	
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[asignaciondet_tmptrg]    Script Date: 9/8/2019 08:39:39 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create or CREATE OR ALTER PROCEDURE [dbo].[asignaciondet_tmptrg]   
	@json nvarchar(max),
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		
		declare @fechaCambio datetime;
		DECLARE @tmp1_vregistro int;
		DECLARE @p_id_tmp nvarchar(max);
		DECLARE @p_fechaInicio date;
		DECLARE @p_fechaFin date;
		DECLARE @delete nvarchar(max);
		DECLARE @p_perfil_id int;
		DECLARE @p_supervisor bit;
		DECLARE @p_totalHoras nvarchar(max);		
		DECLARE @p_operario_id int;
		DECLARE @p_asignacionCab_id int;

		set @fechaCambio= CURRENT_TIMESTAMP;
		DECLARE @p_domSal time;
		DECLARE @p_domEnt time;
		DECLARE @p_sabSal time;
		DECLARE @p_sabEnt time;
		DECLARE @p_vieSal time;
		DECLARE @p_vieEnt time;
		DECLARE @p_jueSal time;
		DECLARE @p_jueEnt time;
		DECLARE @p_mieSal time;
		DECLARE @p_mieEnt time;
		DECLARE @p_marSal time;
		DECLARE @p_marEnt time;
		DECLARE @p_lunSal time;
		DECLARE @p_lunEnt time;
		DECLARE @p_id int;

		select @p_perfil_id="value" from OpenJson(@json) where "key"='perfil_id' and "value"!='None';
		select @p_supervisor="value" from OpenJson(@json) where "key"='supervisor';
		select @delete="value" from OpenJson(@json) where "key"='DELETE';
		select @p_totalHoras="value" from OpenJson(@json) where "key"='totalHoras' and "value"!='None' and "value"!='00';
		select @p_fechaInicio=cast("value" as date) from OpenJson(@json) where "key"='fechaInicio' and "value"!='None';
		select @p_fechaFin=cast("value" as date) from OpenJson(@json) where "key"='fechaFin' and "value"!='None';	
		select @p_operario_id="value" from OpenJson(@json) where "key"='operario_id' and "value"!='None';
		select @p_asignacionCab_id="value" from OpenJson(@json) where "key"='asignacionCab_id';
		select @p_domSal=cast("value" as time) from OpenJson(@json) where "key"='domSal' and "value"!='None';
		select @p_domEnt=cast("value" as time) from OpenJson(@json) where "key"='domEnt' and "value"!='None';
		select @p_sabSal=cast("value" as time) from OpenJson(@json) where "key"='sabSal' and "value"!='None';
		select @p_sabEnt=cast("value" as time) from OpenJson(@json) where "key"='sabEnt' and "value"!='None';
		select @p_vieSal=cast("value" as time) from OpenJson(@json) where "key"='vieSal' and "value"!='None';
		select @p_vieEnt=cast("value" as time) from OpenJson(@json) where "key"='vieEnt' and "value"!='None';
		select @p_jueSal=cast("value" as time) from OpenJson(@json) where "key"='jueSal' and "value"!='None';
		select @p_jueEnt=cast("value" as time) from OpenJson(@json) where "key"='jueEnt' and "value"!='None';
		select @p_mieSal=cast("value" as time) from OpenJson(@json) where "key"='mieSal' and "value"!='None';
		select @p_mieEnt=cast("value" as time) from OpenJson(@json) where "key"='mieEnt' and "value"!='None';
		select @p_marSal=cast("value" as time) from OpenJson(@json) where "key"='marSal' and "value"!='None';
		select @p_marEnt=cast("value" as time) from OpenJson(@json) where "key"='marEnt' and "value"!='None';
		select @p_lunSal=cast("value" as time) from OpenJson(@json) where "key"='lunSal' and "value"!='None';
		select @p_lunEnt=cast("value" as time) from OpenJson(@json) where "key"='lunEnt' and "value"!='None';
		select @p_id="value" from OpenJson(@json) where "key"='id' and "value"!='None';
		
		INSERT INTO dbo.Operarios_asignaciondettemp(perfil_id,supervisor,fechaFin,totalHoras,fechaInicio,operario_id,asignacionCab_id,domSal,domEnt,sabSal,sabEnt,vieSal,vieEnt,jueSal,jueEnt,mieSal,mieEnt,marSal,marEnt,lunSal,lunEnt,eliminado,fechaCreacion)
		select @p_perfil_id,@p_supervisor,@p_fechaFin,@p_totalHoras,@p_fechaInicio,@p_operario_id,@p_asignacionCab_id,@p_domSal,@p_domEnt,@p_sabSal,@p_sabEnt,@p_vieSal,@p_vieEnt,@p_jueSal,@p_jueEnt,@p_mieSal,@p_mieEnt,@p_marSal,@p_marEnt,@p_lunSal,@p_lunEnt,'False',CURRENT_TIMESTAMP;
			
		SET @retorno=0;
		Select @retorno as resultado;
END
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[clean_asignaciondet]    Script Date: 9/8/2019 08:39:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create or CREATE OR ALTER   PROCEDURE [dbo].[clean_asignaciondet]
	@p_asignacionCab_id int,
	@retorno int OUTPUT
	--@operario int
AS   
	
	BEGIN
	SET NOCOUNT ON;
		declare @fechaCambio datetime;
		set @fechaCambio= CURRENT_TIMESTAMP;
		update dbo.Operarios_asignaciondet set eliminado='False' where asignacionCab_id=@p_asignacionCab_id;
		delete from dbo.Operarios_asignaciondettemp where asignacionCab_id=@p_asignacionCab_id;
		SET @retorno=0;
		Select @retorno as resultado;
END
GO

USE [reingenieria]
GO
/****** Object:  StoredProcedure [dbo].[operarios_disponibles_v3]    Script Date: 10/8/2019 20:18:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER  PROCEDURE [dbo].[operarios_disponibles_v3]   
    @puntoServicio int,   
    @totalHoras float,
	@lunEntReq time(7),
	@lunSalReq time(7),
	@marEntReq time(7),
	@marSalReq time(7),
	@mierEntReq time(7),
	@mierSalReq time(7),
	@jueEntReq time(7),
	@jueSalReq time(7),
	@vieEntReq time(7),
	@vieSalReq time(7),
	@sabEntReq time(7),
	@sabSalReq time(7),
	@domEntReq time(7),
	@domSalReq time(7), 
	@fechaInicioOperario nvarchar(10),
	@fechaFinOperario nvarchar(10),
	@perfil nvarchar(3)
AS   
    BEGIN
		LINENO 0;
		DECLARE @horasMaximas int
		DECLARE @traslado int
		DECLARE @lunEntReqTras time(7)
		DECLARE @marEntReqTras time(7)
		DECLARE @mierEntReqTras time(7)
		DECLARE @jueEntReqTras time(7)
		DECLARE @vieEntReqTras time(7)
		DECLARE @sabEntReqTras time(7)
		DECLARE @domEntReqTras time (7)
		DECLARE @fechaFin date
		declare @totalConverted float;
		select @totalConverted=@totalHoras;
		--obtenemos la cantidad de horas maximas permitidas por semana
		SELECT @horasMaximas=cast(valor as int) FROM dbo.Operarios_parametros WHERE tipo='BUSQUEDA' AND parametro='MAXIMO_ASIGNACION'
		--obtenemos el tiempo maximo de traslado de un punto a otro
		SELECT @traslado=cast(valor as int)*-1 FROM dbo.Operarios_parametros WHERE tipo='BUSQUEDA' AND parametro='TIEMPO_TRASLADO'
		--hora requeridas que tienen en cuenta el traslado de un PS a otro PS
		SELECT @lunEntReqTras=CAST (DATEADD(MINUTE, @traslado, @lunEntReq) AS TIME)  
		SELECT @marEntReqTras=CAST (DATEADD(MINUTE, @traslado, @marEntReq) AS TIME)
		SELECT @mierEntReqTras=CAST (DATEADD(MINUTE, @traslado, @mierEntReq) AS TIME)
		SELECT @jueEntReqTras=CAST(DATEADD(MINUTE, @traslado, @jueEntReq) AS TIME)
		SELECT @vieEntReqTras=CAST(DATEADD(MINUTE, @traslado, @vieEntReq) AS TIME)
		SELECT @sabEntReqTras=CAST(DATEADD(MINUTE, @traslado, @sabEntReq) AS TIME)
		SELECT @domEntReqTras=CAST(DATEADD(MINUTE, @traslado, @domEntReq) AS TIME)
		if  LEN(@fechaFinOperario)>0  
		BEGIN
			SET @fechaFin=convert(date, @fechaInicioOperario)	 
		END
		ELSE 
		BEGIN
			SET @fechaFin=CONVERT(date, '2099-01-01', 23)
		END
		SELECT op.* FROM dbo.detalle_lista_operarios3 op 
			where  op.id_operario NOT IN (
			SELECT op.id_operario FROM dbo.detalle_lista_operarios3 op
			INNER JOIN Operarios_asignaciondet asd on asd.operario_id=op.id_operario 
			inner JOIN Operarios_asignacioncab ac on ac.id=asd.asignacionCab_id
			inner JOIN Operarios_puntoservicio ps on ps.id=ac.puntoServicio_id
			inner JOIN Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id AND  rc.estado='Aprobado' 
			LEFT JOIN Operarios_dialibre dl on dl.id_operario_id=op.id_operario
			WHERE 
			(
			
			op.totalHoras+cast(isnull(@totalHoras,0)  as float)>@horasMaximas
			
			
			or(
				(@fechaFin>=asd.fechaInicio and (@fechaFin <=asd.fechaFin or asd.fechaFin is null))
				or (convert(date, @fechaInicioOperario, 23)>=asd.fechaInicio and (convert(date, @fechaInicioOperario)<=asd.fechaFin or asd.fechaFin is null))
				or (convert(date, @fechaInicioOperario, 23) <=asd.fechaInicio and (@fechaFin>=asd.fechaFin or asd.fechaFin is NULL))
				)
			AND(
				(asd.lunEnt between @lunEntReqTras and @lunSalReq) or (asd.lunSal  between @lunEntReqTras and @lunSalReq) 
				or (asd.marEnt between @marEntReqTras and @marSalReq) or (asd.marSal   between @marEntReqTras and @marSalReq)
				or (asd.mieEnt between @mierEntReqTras and @mierSalReq) or (asd.mieSal  between @mierEntReqTras and @mierSalReq)
				or (asd.jueEnt between @jueEntReqTras and @jueSalReq) or (asd.jueSal between @jueEntReqTras and  @jueSalReq)
				or (asd.vieEnt between @vieEntReqTras and @vieSalReq) or (asd.vieSal  between  @vieEntReqTras and @vieSalReq)
				or (asd.sabEnt between @sabEntReqTras and @sabSalReq) or (asd.sabSal  between @sabEntReqTras and @sabSalReq)
				or (asd.domEnt between @domEntReqTras and @domSalReq) or (asd.domSal  between @domEntReqTras and @domSalReq)
			
			)
			
			
			/**traemos los que tienen dia libre en ese dia del requerimiento**/
			or (dl.lunEnt between @lunEntReq and @lunSalReq) or (dl.lunSal between @lunEntReq and @lunSalReq)
			or (dl.marEnt between @marEntReq and @marSalReq) or (dl.marSal between @marEntReqTras and @marSalReq)
			or (dl.mieEnt between @mierEntReq and @mierSalReq) or (dl.mieSal  between @mierEntReq and @mierSalReq)
			or (dl.jueEnt between  @jueEntReq and @jueSalReq)
			or (dl.jueSal between  @jueEntReq and @jueSalReq)
			or (dl.vieEnt between  @vieEntReq and @vieSalReq)  
			or (dl.sabEnt between @sabEntReq and @sabSalReq) or (dl.sabSal  between @sabEntReq and @sabSalReq)
			or (dl.domEnt  between @domEntReq and @domSalReq) or (dl.domSal  between @domEntReq and @domSalReq)
			)) AND op.id_operario NOT IN (
			SELECT op.id_operario FROM dbo.detalle_lista_operarios3 op
			INNER JOIN Operarios_asignaciondettemp asd on asd.operario_id=op.id_operario 
			inner JOIN Operarios_asignacioncab ac on ac.id=asd.asignacionCab_id
			inner JOIN Operarios_puntoservicio ps on ps.id=ac.puntoServicio_id
			inner JOIN Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id AND  rc.estado='Aprobado' 
			LEFT JOIN Operarios_dialibre dl on dl.id_operario_id=op.id_operario
			WHERE 
			(op.totalHoras+cast(isnull(@totalHoras,0)  as float)>@horasMaximas
			
			
			or(
				(@fechaFin>=asd.fechaInicio and (@fechaFin <=asd.fechaFin or asd.fechaFin is null))
				or (convert(date, @fechaInicioOperario, 23)>=asd.fechaInicio and (convert(date, @fechaInicioOperario)<=asd.fechaFin or asd.fechaFin is null))
				or (convert(date, @fechaInicioOperario, 23) <=asd.fechaInicio and (@fechaFin>=asd.fechaFin or asd.fechaFin is NULL))
				)
			AND(
				(asd.lunEnt between @lunEntReqTras and @lunSalReq) or (asd.lunSal  between @lunEntReqTras and @lunSalReq) 
				or (asd.marEnt between @marEntReqTras and @marSalReq) or (asd.marSal   between @marEntReqTras and @marSalReq)
				or (asd.mieEnt between @mierEntReqTras and @mierSalReq) or (asd.mieSal  between @mierEntReqTras and @mierSalReq)
				or (asd.jueEnt between @jueEntReqTras and @jueSalReq) or (asd.jueSal between @jueEntReqTras and  @jueSalReq)
				or (asd.vieEnt between @vieEntReqTras and @vieSalReq) or (asd.vieSal  between  @vieEntReqTras and @vieSalReq)
				or (asd.sabEnt between @sabEntReqTras and @sabSalReq) or (asd.sabSal  between @sabEntReqTras and @sabSalReq)
				or (asd.domEnt between @domEntReqTras and @domSalReq) or (asd.domSal  between @domEntReqTras and @domSalReq)
			
			)
			
			/**traemos los que tienen dia libre en ese dia del requerimiento**/
			or (dl.lunEnt between @lunEntReq and @lunSalReq) or (dl.lunSal between @lunEntReq and @lunSalReq)
			or (dl.marEnt between @marEntReq and @marSalReq) or (dl.marSal between @marEntReqTras and @marSalReq)
			or (dl.mieEnt between @mierEntReq and @mierSalReq) or (dl.mieSal  between @mierEntReq and @mierSalReq)
			or (dl.jueEnt between  @jueEntReq and @jueSalReq)
			or (dl.jueSal between  @jueEntReq and @jueSalReq)
			or (dl.vieEnt between  @vieEntReq and @vieSalReq)  
			or (dl.sabEnt between @sabEntReq and @sabSalReq) or (dl.sabSal  between @sabEntReq and @sabSalReq)
			or (dl.domEnt  between @domEntReq and @domSalReq) or (dl.domSal  between @domEntReq and @domSalReq)
			)
			)
		AND ((LEN(@perfil)>0 and op.ids_perfil like '%'+@perfil+'%') or LEN(@perfil)=0)
		ORDER BY op.totalHoras asc, op.nombres asc
	END
	go


USE [reingenieria]
GO
/****** Object:  UserDefinedFunction [dbo].[listarasignaciones]    Script Date: 9/8/2019 08:40:01 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create or CREATE OR ALTER FUNCTION [dbo].[listarasignaciones](@asigcab integer)
RETURNS @query TABLE (
	 id int,
	lunEnt time,
	lunSal time,
	marEnt time,
	marSal time,
	mieEnt time,
	mieSal time,
	jueEnt time,
	jueSal time,
	vieEnt time,
	vieSal time,
	sabEnt time,
	sabSal time,
	domEnt time,
	domSal time,
	asignacionCab_id int ,
	operario_id int ,
	fechaInicio date,
	totalHoras nvarchar(8) ,
	fechaFin date,
	supervisor bit ,
	perfil_id int,
	eliminado bit ,
	tipo nvarchar(12)
)
BEGIN
	insert @query
	SELECT [id],[lunEnt],[lunSal],[marEnt],[marSal],[mieEnt],[mieSal],[jueEnt],[jueSal],[vieEnt],[vieSal],[sabEnt],[sabSal],[domEnt],[domSal],
	[asignacionCab_id],[operario_id],[fechaInicio],[totalHoras],[fechaFin],[supervisor],[perfil_id],[eliminado],'persistido'
	FROM [dbo].[Operarios_asignaciondet] where asignacionCab_id=@asigcab
	union 
	SELECT [id],[lunEnt],[lunSal],[marEnt],[marSal],[mieEnt],[mieSal],[jueEnt],[jueSal],[vieEnt],[vieSal],[sabEnt],[sabSal],[domEnt],[domSal],
	[asignacionCab_id],[operario_id],[fechaInicio],[totalHoras],[fechaFin],[supervisor],[perfil_id],[eliminado],'temporal'
	FROM [dbo].[Operarios_asignaciondettemp] where  asignacionCab_id=@asigcab
	RETURN
END
Go

USE [reingenieria]
GO

/****** Object:  View [dbo].[detalle_lista_operarios3]    Script Date: 10/8/2019 20:18:33 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create or CREATE OR ALTER   VIEW [dbo].[detalle_lista_operarios3]
AS
SELECT        id_operario, nombres, nroLegajo, nombres_puntoServicio, ids_puntoServicio, totalHoras,
                             (SELECT DISTINCT STRING_AGG(esp.especializacion, ', ') AS Expr1
                               FROM            dbo.Operarios_operario_profesion AS opf LEFT OUTER JOIN
                                                         dbo.Operarios_especializacion AS esp ON esp.id = opf.especializacion_id
                               WHERE        (opf.operario_id = op_1.id_operario)) AS perfil, antiguedad,
                             (SELECT DISTINCT STRING_AGG(especializacion_id, ', ') AS Expr1
                               FROM            dbo.Operarios_operario_profesion AS opf
                               WHERE        (operario_id = op_1.id_operario)) AS ids_perfil
FROM            (SELECT        op.id AS id_operario, { fn CONCAT({ fn CONCAT(op.nombre, ' ') }, op.apellido) } AS nombres, op.nroLegajo, ISNULL(STRING_AGG(ps.NombrePServicio, ', '), '') AS nombres_puntoServicio, ISNULL(STRING_AGG(ps.id, 
                                                    ', '), ' ') AS ids_puntoServicio, SUM(CAST(ISNULL(aod.totalHoras, 0) AS float))+SUM(CAST(ISNULL(aodt.totalHoras, 0) AS float)) AS totalHoras, DATEDIFF(year, op.fechaInicio, GETDATE()) AS antiguedad
                          FROM            dbo.Operarios_operario AS op LEFT OUTER JOIN
                                                    dbo.Operarios_asignaciondet AS aod ON op.id = aod.operario_id LEFT OUTER JOIN
													dbo.Operarios_asignaciondettemp AS aodt ON op.id = aodt.operario_id LEFT OUTER JOIN
                                                    dbo.Operarios_asignacioncab AS aoc ON aod.asignacionCab_id = aoc.id OR aodt.asignacionCab_id = aoc.id LEFT OUTER JOIN
                                                    dbo.Operarios_puntoservicio AS ps ON ps.id = aoc.puntoServicio_id
                          GROUP BY op.id, op.nombre, op.apellido, op.nroLegajo, op.fechaInicio) AS op_1
GO

USE [reingenieria]
GO

SET ANSI_PADDING ON
GO

/****** Object:  Index [ClusteredIndex-20190813-093028]    Script Date: 13/8/2019 09:33:49 ******/
CREATE CLUSTERED INDEX [ClusteredIndex-20190813-093028] ON [dbo].[ESME_EM_Marcaciones]
(
	[CodPersona] ASC,
	[CodUbicacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
