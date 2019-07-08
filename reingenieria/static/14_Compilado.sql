USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_puntoservicio]    Script Date: 3/7/2019 09:57:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_puntoservicio]
ON [dbo].[Operarios_puntoservicio]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @tmp1_vregistro int;
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				INSERT INTO dbo.Operarios_puntoservicio
				(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
				VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp1_vregistro);
				select @nuevoID = SCOPE_IDENTITY();
				update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;

					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0
					FETCH NEXT FROM cursorSc0 INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0 INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0
					DEALLOCATE cursorSc0
					
						

					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
					VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
					update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
					select @nuevo_asignacionCab_id = SCOPE_IDENTITY();

						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0

					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1

							

					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

						/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,


							@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP
							DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';
							
			END
			FETCH NEXT FROM cursorIt INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_asigjefefiscal]    Script Date: 3/7/2019 09:55:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[trg_vrs_Operarios_asigjefefiscal]

 ON [dbo].[Operarios_asigjefefiscal]
INSTEAD OF UPDATE
AS
BEGIN
DECLARE @TransactionName varchar(20) = 'Transactional';
BEGIN TRAN @TransactionName  
BEGIN TRY
DECLARE @nuevoID int;
DECLARE @fechaCambio datetime;
DECLARE @p_id int;
DECLARE @tmp1_vregistro int;
DECLARE @p_userFiscal_id int ;

DECLARE @p_userJefe_id int;

DECLARE @p_vfecha_inicio datetime;

DECLARE @p_vfecha_fin datetime;

DECLARE @p_vregistro int;

SET @fechaCambio=CURRENT_TIMESTAMP
DECLARE cursorIt CURSOR FOR SELECT * FROM inserted
OPEN cursorIt
FETCH NEXT FROM cursorIt INTO @p_id,@p_userFiscal_id,@p_userJefe_id,@p_vfecha_inicio,@p_vfecha_fin,@p_vregistro

WHILE @@FETCH_STATUS = 0
BEGIN
 IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_asigjefefiscal set vfechaFin=@fechaCambio where id=@p_id;
			END
			ELSE
			BEGIN
				INSERT INTO dbo.Operarios_asigjefefiscal
				(userFiscal_id,userJefe_id,vfechaInicio,vfechaFin,vregistro)
				VALUES(@p_userFiscal_id,@p_userJefe_id,@fechaCambio,NULL,@p_vregistro);
				update dbo.Operarios_asigjefefiscal set vfechaFin=@fechaCambio where id=@p_id;
			END
FETCH NEXT FROM cursorIt INTO  @p_id,@p_userFiscal_id,@p_userJefe_id,@p_vfecha_inicio,@p_vfecha_fin,@p_vregistro

END
COMMIT TRANSACTION @TransactionName;
END TRY  
BEGIN CATCH 
print ERROR_MESSAGE();
SELECT ERROR_MESSAGE() AS ErrorMessage
ROLLBACK TRAN @TransactionName;  
END CATCH
CLOSE cursorIt
DEALLOCATE cursorIt

END
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_asigfiscalpuntoservicio]    Script Date: 3/7/2019 09:55:18 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[trg_vrs_Operarios_asigfiscalpuntoservicio]

 ON [dbo].[Operarios_asigfiscalpuntoservicio]
INSTEAD OF UPDATE
AS
BEGIN
DECLARE @TransactionName varchar(20) = 'Transactional';
BEGIN TRAN @TransactionName  
BEGIN TRY
DECLARE @nuevoID int;
DECLARE @fechaCambio datetime;
DECLARE @p_id int;
DECLARE @tmp1_vregistro int;

DECLARE @p_puntoServicio_id int;

DECLARE @p_userFiscal_id int;

DECLARE @p_vfecha_inicio datetime;

DECLARE @p_vfecha_fin datetime;

DECLARE @p_vregistro int;

SET @fechaCambio=CURRENT_TIMESTAMP
DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
OPEN cursorIt
FETCH NEXT FROM cursorIt INTO @p_id,@p_puntoServicio_id,@p_userFiscal_id,@p_vfecha_inicio,@p_vfecha_fin,@p_vregistro

WHILE @@FETCH_STATUS = 0
BEGIN
	 IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_asigfiscalpuntoservicio set vfechaFin=@fechaCambio where id=@p_id;
			END
			ELSE
			BEGIN
				INSERT INTO dbo.Operarios_asigfiscalpuntoservicio
					(puntoServicio_id,userFiscal_id,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_puntoServicio_id,@p_userFiscal_id,@fechaCambio,NULL,@p_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_asigfiscalpuntoservicio set vfechaFin=@fechaCambio where id=@p_id;
			END
FETCH NEXT FROM cursorIt INTO  @p_id,@p_puntoServicio_id,@p_userFiscal_id,@p_vfecha_inicio,@p_vfecha_fin,@p_vregistro
END
COMMIT TRANSACTION @TransactionName;
END TRY  
BEGIN CATCH  
SELECT ERROR_MESSAGE() AS ErrorMessage
ROLLBACK TRAN @TransactionName;  
END CATCH
CLOSE cursorIt
DEALLOCATE cursorIt
END
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_asignaciondet]    Script Date: 3/7/2019 09:56:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_asignaciondet]
ON [dbo].[Operarios_asignaciondet]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @tmp1_vregistro int;
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_asignacioncab ac on ac.puntoServicio_id=ps.id where ac.id=@hrm0_asignacionCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;
				/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0W CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0W
					FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
						VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
						select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();
				
					/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0


				
						FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0W
					DEALLOCATE cursorSc0W


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
					VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
					update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
					select @nuevo_asignacionCab_id = SCOPE_IDENTITY();



						
						/* 1.B.a - Asiginacion DET*/
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp1_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1

					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							
							/*1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';

				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
				END

			FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_asignacioncab]    Script Date: 3/7/2019 09:56:02 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_asignacioncab]
ON [dbo].[Operarios_asignacioncab]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @tmp1_vregistro int;
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			PRINT COLUMNS_UPDATED();
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@dp1_puntoServicio_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN
					
					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;

				/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0A CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0A
					FETCH NEXT FROM cursorSc0A INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					
					/* 1.A - Relavamiento CAB */
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0


				
						FETCH NEXT FROM cursorSc0A INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0A
					DEALLOCATE cursorSc0A


					/* 1.B - Asiginacion */
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp1_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();

						
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							
							/*1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';

				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
				END

			FETCH NEXT FROM cursorIt INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_planificacionope]    Script Date: 3/7/2019 09:54:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_planificacionope]
ON [dbo].[Operarios_planificacionope]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @tmp1_vregistro int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm10_id int;
		DECLARE @hrm10_frecuencia nvarchar(max);
		DECLARE @hrm10_relevamientoCab_id int;
		DECLARE @hrm10_tipoHora_id int;
		DECLARE @hrm10_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_planificacioncab pc on pc.puntoServicio_id=ps.id where pc.id=@hrm1_planificacionCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0W CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0W
					FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm10_id,@hrm10_frecuencia,@hrm10_relevamientoCab_id,@hrm10_tipoHora_id,@hrm10_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm10_frecuencia, @nuevo_relevamientoCab_id,@hrm10_tipoHora_id,@hrm10_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm10_id,@hrm10_frecuencia,@hrm10_relevamientoCab_id,@hrm10_tipoHora_id,@hrm10_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0W
					DEALLOCATE cursorSc0W


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/

					DECLARE cursorScX CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorScX
					FETCH NEXT FROM cursorScX INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
					
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						

							/* 1.C.a - Planificacion OPE*/
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp1_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							
							
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorScX INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorScX
					DEALLOCATE cursorScX





				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO

/****** Object:  Trigger [dbo].[trg_vrs_Operarios_planificacionesp]    Script Date: 3/7/2019 02:13:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_planificacionesp]
ON [dbo].[Operarios_planificacionesp]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @tmp1_vregistro int;
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@p_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_planificacioncab pc on pc.puntoServicio_id=ps.id where pc.id=@hrm0_planificacionCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0W CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0W
					FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0W
					DEALLOCATE cursorSc0W


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/

					DECLARE cursorScX CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorScX
					FETCH NEXT FROM cursorScX INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
					
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp1_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							
					FETCH NEXT FROM cursorScX INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorScX
					DEALLOCATE cursorScX





				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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

ALTER TABLE [dbo].[Operarios_planificacionesp] ENABLE TRIGGER [trg_vrs_Operarios_planificacionesp]
GO


USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_planificacioncab]    Script Date: 3/7/2019 09:54:31 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_planificacioncab]
ON [dbo].[Operarios_planificacioncab]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp1_vregistro int;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_planificacioncab pc on pc.puntoServicio_id=ps.id where pc.puntoServicio_id=@dp2_puntoServicio_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0W CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0W
					FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0W INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0W
					DEALLOCATE cursorSc0W


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp1_vregistro);
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/


				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_relevamientomensualeros]    Script Date: 3/7/2019 09:54:49 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_relevamientomensualeros]
ON [dbo].[Operarios_relevamientomensualeros]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;
			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id where rc.id=@hrm0_relevamientoCab_id
				print @p_id;
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;


					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0A CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0A
					FETCH NEXT FROM cursorSc0A INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
							INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2


						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp1_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						

						FETCH NEXT FROM cursorSc0A INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0A
					DEALLOCATE cursorSc0A


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0

					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,


							@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';

				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_ Operarios_relevamientocupohoras]    Script Date: 3/7/2019 10:01:45 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_ Operarios_relevamientocupohoras]
ON [dbo].[Operarios_relevamientocupohoras]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id where  rc.id=@hrm1_relevamientoCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN




					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0F CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0F
					FETCH NEXT FROM cursorSc0F INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,

					@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2


						/* 1.A.c - Relavamiento CUP */
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp1_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						
						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0F INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0F
					DEALLOCATE cursorSc0F


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,


							@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';







				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_relevamientoesp]    Script Date: 3/7/2019 10:03:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_relevamientoesp]
ON [dbo].[Operarios_relevamientoesp]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id where rc.id=@hrm3_relevamientoCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN




					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0E CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0E
					FETCH NEXT FROM cursorSc0E INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,

					@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();



						/* 1.A.a - Relavamiento ESP */
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp1_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2


						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0E INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0E
					DEALLOCATE cursorSc0E


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';







				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_relevamientodet]    Script Date: 3/7/2019 10:02:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_relevamientodet]
ON [dbo].[Operarios_relevamientodet]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			IF  UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				select @p_id=ps.id from dbo.Operarios_puntoservicio ps left join dbo.Operarios_relevamientocab rc on rc.puntoServicio_id=ps.id where rc.id=@hrm2_relevamientoCab_id
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@p_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN




					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					DECLARE cursorSc0D CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocab where puntoServicio_id=@p_id
					OPEN cursorSc0D
					FETCH NEXT FROM cursorSc0D INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					WHILE @@FETCH_STATUS = 0
					BEGIN
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp_vregistro)
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();

						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp1_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;


						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where

						relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

						FETCH NEXT FROM cursorSc0D INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc0D
					DEALLOCATE cursorSc0D


					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';
							/* 1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';







				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
					

			END
			FETCH NEXT FROM cursorIt INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
			print '77';
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
USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_relevamientocab]    Script Date: 3/7/2019 10:01:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_relevamientocab]
ON [dbo].[Operarios_relevamientocab]
INSTEAD OF UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @p_id int;
		DECLARE @p_CodPuntoServicio nvarchar(max);
		DECLARE @p_NombrePServicio nvarchar(max);
		DECLARE @p_DireccionContrato nvarchar(max);
		DECLARE @p_Barrios nvarchar(max);
		DECLARE @p_Contacto nvarchar(max);
		DECLARE @p_MailContacto nvarchar(max);
		DECLARE @p_TelefonoContacto nvarchar(max);
		DECLARE @p_Coordenadas nvarchar(max);
		DECLARE @p_Ciudad_id int;
		DECLARE @p_Cliente_id int;
		DECLARE @p_NumeroMarcador nvarchar(max);
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
		DECLARE @hrm3_id int;
		DECLARE @hrm3_frecuencia nvarchar(max);
		DECLARE @hrm3_relevamientoCab_id int;
		DECLARE @hrm3_tipo_id int;
		DECLARE @hrm3_cantHoras nvarchar(max);
		DECLARE @hrm2_id int;
		DECLARE @hrm2_orden int;
		DECLARE @hrm2_lunEnt time;
		DECLARE @hrm2_lunSal time;
		DECLARE @hrm2_marEnt time;
		DECLARE @hrm2_marSal time;
		DECLARE @hrm2_mieEnt time;
		DECLARE @hrm2_mieSal time;
		DECLARE @hrm2_jueEnt time;
		DECLARE @hrm2_jueSal time;
		DECLARE @hrm2_vieEnt time;
		DECLARE @hrm2_vieSal time;
		DECLARE @hrm2_sabEnt time;
		DECLARE @hrm2_sabSal time;
		DECLARE @hrm2_domEnt time;
		DECLARE @hrm2_domSal time;
		DECLARE @hrm2_relevamientoCab_id int;
		DECLARE @hrm2_tipoServPart_id int;
		DECLARE @hrm1_id int;
		DECLARE @hrm1_frecuencia nvarchar(max);
		DECLARE @hrm1_relevamientoCab_id int;
		DECLARE @hrm1_tipoHora_id int;
		DECLARE @hrm1_cantHoras nvarchar(max);
		DECLARE @hrm0_id int;
		DECLARE @hrm0_relevamientoCab_id int;
		DECLARE @hrm0_mensuCantidad int;
		DECLARE @hrm0_sueldo int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
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
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
		DECLARE @hrm1_cantidad int;
		DECLARE @hrm1_lun bit ;
		DECLARE @hrm1_mar bit ;
		DECLARE @hrm1_mie bit ;
		DECLARE @hrm1_jue bit ;
		DECLARE @hrm1_vie bit ;
		DECLARE @hrm1_sab bit ;
		DECLARE @hrm1_dom bit ;
		DECLARE @hrm1_fer bit ;
		DECLARE @hrm1_ent time;
		DECLARE @hrm1_sal time;
		DECLARE @hrm1_especialista_id int;
		DECLARE @hrm1_planificacionCab_id int;
		DECLARE @hrm1_corte nvarchar(max);
		DECLARE @hrm1_total nvarchar(max);
		DECLARE @hrm0_frecuencia nvarchar(max);
		DECLARE @hrm0_especialista_id int;
		DECLARE @hrm0_planificacionCab_id int;
		DECLARE @hrm0_tipo_id int;
		DECLARE @hrm0_cantHoras nvarchar(max);
		DECLARE @hrm0_fechaLimpProf date;
		DECLARE @nuevo_relevamientoCab_id int;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE @fechaCambio datetime;

			SET @fechaCambio=CURRENT_TIMESTAMP;
			PRINT COLUMNS_UPDATED();
			IF UPDATE(vfechaFin)
			BEGIN
				update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
			END
			ELSE
			BEGIN

				/* 1 - Punto de Servicio*/
				DECLARE cursorSc0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_puntoservicio where id=@dp0_puntoServicio_id
				OPEN cursorSc0
				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				WHILE @@FETCH_STATUS = 0
				BEGIN

					INSERT INTO dbo.Operarios_puntoservicio
					(CodPuntoServicio,NombrePServicio,DireccionContrato,Barrios,Contacto,MailContacto,TelefonoContacto,Coordenadas,Ciudad_id,Cliente_id,NumeroMarcador,vfechaInicio,vfechaFin,vregistro)
					VALUES(@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@fechaCambio,NULL,@tmp_vregistro);
					select @nuevoID = SCOPE_IDENTITY();
					update dbo.Operarios_puntoservicio set vfechaFin=@fechaCambio where id=@p_id;



					/* 1.A - Relavamiento CAB */
					INSERT INTO dbo.Operarios_relevamientocab (fecha,cantidad,puntoServicio_id,cantidadHrTotal,cantidadHrEsp,fechaInicio,usuario_id,tipoSalario_id,comentario,cantAprendices,estado,fechaFin,vfechaInicio,vfechaFin,vregistro)
					VALUES(@dp0_fecha,@dp0_cantidad,@nuevoID,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@fechaCambio,NULL,@tmp1_vregistro)
					select @nuevo_relevamientoCab_id = SCOPE_IDENTITY();
					update dbo.Operarios_relevamientocab set vfechaFin=@fechaCambio where id=@dp0_id;
						/* 1.A.a - Relavamiento ESP */
						DECLARE cursorHrm0_3 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientoesp where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_3
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientoesp(frecuencia,relevamientoCab_id,tipo_id,cantHoras,vfechaInicio,vfechaFin,vregistro)
						VALUES(@hrm3_frecuencia,@nuevo_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientoesp set vfechaFin=@fechaCambio where id=@hrm3_id;
						FETCH NEXT FROM cursorHrm0_3 INTO @hrm3_id,@hrm3_frecuencia,@hrm3_relevamientoCab_id,@hrm3_tipo_id,@hrm3_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_3
						DEALLOCATE cursorHrm0_3


						/* 1.A.b - Relavamiento DET */
						DECLARE cursorHrm0_2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientodet where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_2
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientodet(orden,lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,relevamientoCab_id,tipoServPart_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal, @nuevo_relevamientoCab_id,@hrm2_tipoServPart_id,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientodet set vfechaFin=@fechaCambio where id=@hrm2_id;
						FETCH NEXT FROM cursorHrm0_2 INTO @hrm2_id,@hrm2_orden,@hrm2_lunEnt,@hrm2_lunSal,@hrm2_marEnt,@hrm2_marSal,@hrm2_mieEnt,@hrm2_mieSal,@hrm2_jueEnt,@hrm2_jueSal,@hrm2_vieEnt,@hrm2_vieSal,@hrm2_sabEnt,@hrm2_sabSal,@hrm2_domEnt,@hrm2_domSal,@hrm2_relevamientoCab_id,@hrm2_tipoServPart_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
						END
						CLOSE cursorHrm0_2
						DEALLOCATE cursorHrm0_2



						/* 1.A.c - Relavamiento CUP */
						DECLARE cursorHrm0_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientocupohoras where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_1
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientocupohoras(frecuencia,relevamientoCab_id,tipoHora_id,cantHoras,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@hrm1_frecuencia, @nuevo_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@fechaCambio,NULL,@tmp_vregistro)
						update dbo.Operarios_relevamientocupohoras set vfechaFin=@fechaCambio where id=@hrm1_id;
						FETCH NEXT FROM cursorHrm0_1 INTO @hrm1_id,@hrm1_frecuencia,@hrm1_relevamientoCab_id,@hrm1_tipoHora_id,@hrm1_cantHoras,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_1
						DEALLOCATE cursorHrm0_1

						/* 1.A.d - Relavamiento MEN */
						DECLARE cursorHrm0_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_relevamientomensualeros where relevamientoCab_id=@dp0_id
						OPEN cursorHrm0_0
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						WHILE @@FETCH_STATUS = 0
						BEGIN
						INSERT INTO dbo.Operarios_relevamientomensualeros(relevamientoCab_id,mensuCantidad,sueldo,vfechaInicio,vfechaFin,vregistro) 
						VALUES( @nuevo_relevamientoCab_id,@hrm0_mensuCantidad,@hrm0_sueldo,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_relevamientomensualeros set vfechaFin=@fechaCambio where id=@hrm0_id;
						FETCH NEXT FROM cursorHrm0_0 INTO @hrm0_id,@hrm0_mensuCantidad,@hrm0_sueldo,@hrm0_relevamientoCab_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

						END
						CLOSE cursorHrm0_0
						DEALLOCATE cursorHrm0_0

					/* 1.B - Asiginacion */
					DECLARE cursorSc1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignacioncab where puntoServicio_id=@p_id
					OPEN cursorSc1
					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_asignacioncab (fechaUltimaMod,totalasignado,puntoServicio_id,usuario_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp1_fechaUltimaMod,@dp1_totalasignado,@nuevoID,@dp1_usuario_id,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_asignacioncab set vfechaFin=@fechaCambio where id=@dp1_id;
						select @nuevo_asignacionCab_id = SCOPE_IDENTITY();
						/* 1.B.a - Asiginacion DET*/
							DECLARE cursorHrm1_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_asignaciondet where asignacionCab_id=@dp1_id
							OPEN cursorHrm1_0
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_asignaciondet(lunEnt,lunSal,marEnt,marSal,mieEnt,mieSal,jueEnt,jueSal,vieEnt,vieSal,sabEnt,sabSal,domEnt,domSal,asignacionCab_id,operario_id,fechaInicio,totalHoras,fechaFin,supervisor,perfil_id,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@nuevo_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_asignaciondet set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm1_0 INTO @hrm0_id,@hrm0_lunEnt,@hrm0_lunSal,@hrm0_marEnt,@hrm0_marSal,@hrm0_mieEnt,@hrm0_mieSal,@hrm0_jueEnt,@hrm0_jueSal,@hrm0_vieEnt,@hrm0_vieSal,@hrm0_sabEnt,@hrm0_sabSal,@hrm0_domEnt,@hrm0_domSal,@hrm0_asignacionCab_id,@hrm0_operario_id,@hrm0_fechaInicio,@hrm0_totalHoras,@hrm0_fechaFin,@hrm0_supervisor,@hrm0_perfil_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm1_0
							DEALLOCATE cursorHrm1_0





					FETCH NEXT FROM cursorSc1 INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					END
					CLOSE cursorSc1
					DEALLOCATE cursorSc1


					/* 1.C - Planificacion*/
					DECLARE cursorSc2 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacioncab where puntoServicio_id=@p_id
					OPEN cursorSc2
					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

					WHILE @@FETCH_STATUS = 0
					BEGIN
						INSERT INTO dbo.Operarios_planificacioncab (fecha,cantidad,cantHoras,cantHorasNoc,cantHorasEsp,puntoServicio_id,vfechaInicio,vfechaFin,vregistro) 
						VALUES(@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@nuevoID,@fechaCambio,NULL,@tmp_vregistro);
						update dbo.Operarios_planificacioncab set vfechaFin=@fechaCambio where id=@dp2_id;
						select @nuevo_planificacionCab_id = SCOPE_IDENTITY();

							
							/*1.C.b - Planificacion ESP*/
							/*DECLARE cursorHrm2_0 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionesp where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_0
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionesp(frecuencia,especialista_id,planificacionCab_id,tipo_id,cantHoras,fechaLimpProf,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@fechaCambio,NULL,@tmp_vregistro)
							update dbo.Operarios_planificacionesp set vfechaFin=@fechaCambio where id=@hrm0_id;
							FETCH NEXT FROM cursorHrm2_0 INTO @hrm0_id,@hrm0_frecuencia,@hrm0_especialista_id,@hrm0_planificacionCab_id,@hrm0_tipo_id,@hrm0_cantHoras,@hrm0_fechaLimpProf,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							END
							CLOSE cursorHrm2_0
							DEALLOCATE cursorHrm2_0
							print '66';*/

							/* 1.C.a - Planificacion OPE*/
							DECLARE cursorHrm2_1 CURSOR LOCAL FOR SELECT * FROM dbo.Operarios_planificacionope where planificacionCab_id=@dp2_id
							OPEN cursorHrm2_1
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
							WHILE @@FETCH_STATUS = 0
							BEGIN
							INSERT INTO dbo.Operarios_planificacionope(cantidad,lun,mar,mie,jue,vie,sab,dom,fer,ent,sal,especialista_id,planificacionCab_id,corte,total,vfechaInicio,vfechaFin,vregistro) 
							VALUES(@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@nuevo_planificacionCab_id,@hrm1_corte,@hrm1_total,@fechaCambio,NULL,@tmp_vregistro);
							update dbo.Operarios_planificacionope set vfechaFin=@fechaCambio where id=@hrm1_id;
							FETCH NEXT FROM cursorHrm2_1 INTO @hrm1_id,@hrm1_cantidad,@hrm1_lun,@hrm1_mar,@hrm1_mie,@hrm1_jue,@hrm1_vie,@hrm1_sab,@hrm1_dom,@hrm1_fer,@hrm1_ent,@hrm1_sal,@hrm1_especialista_id,@hrm1_planificacionCab_id,@hrm1_corte,@hrm1_total,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro

							END
							CLOSE cursorHrm2_1
							DEALLOCATE cursorHrm2_1
							print '55 b';

					FETCH NEXT FROM cursorSc2 INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
					END
					CLOSE cursorSc2
					DEALLOCATE cursorSc2
					print '55';

				FETCH NEXT FROM cursorSc0 INTO @p_id,@p_CodPuntoServicio,@p_NombrePServicio,@p_DireccionContrato,@p_Barrios,@p_Contacto,@p_MailContacto,@p_TelefonoContacto,@p_Coordenadas,@p_Ciudad_id,@p_Cliente_id,@p_NumeroMarcador,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro
				END
				CLOSE cursorSc0
				DEALLOCATE cursorSc0
				END

			FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
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

USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_relevamientocab]    Script Date: 3/7/2019 10:01:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_header_relevamientocab]
ON [dbo].[Operarios_relevamientocab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @dp0_id int;
		DECLARE @dp0_fecha datetime2 ;
		DECLARE @dp0_cantidad int;
		DECLARE @dp0_puntoServicio_id int;
		DECLARE @dp0_cantidadHrTotal nvarchar(max);
		DECLARE @dp0_cantidadHrEsp nvarchar(max);
		DECLARE @dp0_fechaInicio date;
		DECLARE @dp0_usuario_id int;
		DECLARE @dp0_tipoSalario_id int;
		DECLARE @dp0_comentario nvarchar(max);
		DECLARE @dp0_cantAprendices int;
		DECLARE @dp0_estado nvarchar(max);
		DECLARE @dp0_fechaFin date;
        DECLARE @dp1_id int;
		DECLARE @dp1_fecha datetime2 ;
		DECLARE @dp1_cantidad int;
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_cantidadHrTotal nvarchar(max);
		DECLARE @dp1_cantidadHrEsp nvarchar(max);
		DECLARE @dp1_fechaInicio date;
		DECLARE @dp1_usuario_id int;
		DECLARE @dp1_tipoSalario_id int;
		DECLARE @dp1_comentario nvarchar(max);
		DECLARE @dp1_cantAprendices int;
		DECLARE @dp1_estado nvarchar(max);
		DECLARE @dp1_fechaFin date;
		DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @tmp1_vregistro int;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
		WHILE @@FETCH_STATUS = 0
		BEGIN
			DECLARE cursorDt CURSOR LOCAL FOR SELECT * FROM deleted where id=dp0_id
            OPEN cursorDt
            FETCH NEXT FROM cursorDt INTO @dp1_id,@dp1_fecha,@dp1_cantidad,@dp1_puntoServicio_id,@dp1_cantidadHrTotal,@dp1_cantidadHrEsp,@dp1_fechaInicio,@dp1_usuario_id,@dp1_tipoSalario_id,@dp1_comentario,@dp1_cantAprendices,@dp1_estado,@dp1_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
            WHILE @@FETCH_STATUS = 0
            BEGIN
                if(dp1_cantidadHrTotal!=dp0_cantidadHrTotal)
                BEGIN
                    UPDATE [dbo].[Operarios_planificacioncab] set rePlanificar=True where puntoServicio_id=@dp0_puntoServicio_id and vfechaFin is NULL;
                    UPDATE [dbo].[Operarios_asignacioncab] set reAsignar=True where puntoServicio_id=@dp0_puntoServicio_id and vfechaFin is NULL;
                END
            FETCH NEXT FROM cursorDt INTO @dp1_id,@dp1_fecha,@dp1_cantidad,@dp1_puntoServicio_id,@dp1_cantidadHrTotal,@dp1_cantidadHrEsp,@dp1_fechaInicio,@dp1_usuario_id,@dp1_tipoSalario_id,@dp1_comentario,@dp1_cantAprendices,@dp1_estado,@dp1_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
            END		
		FETCH NEXT FROM cursorIt INTO @dp0_id,@dp0_fecha,@dp0_cantidad,@dp0_puntoServicio_id,@dp0_cantidadHrTotal,@dp0_cantidadHrEsp,@dp0_fechaInicio,@dp0_usuario_id,@dp0_tipoSalario_id,@dp0_comentario,@dp0_cantAprendices,@dp0_estado,@dp0_fechaFin,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro
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

USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_planificacioncab]    Script Date: 3/7/2019 09:54:31 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_hd_planificacioncab]
ON [dbo].[Operarios_planificacioncab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @dp2_id int;
		DECLARE @dp2_fecha datetime2 ;
		DECLARE @dp2_cantidad int;
		DECLARE @dp2_cantHoras nvarchar(max);
		DECLARE @dp2_cantHorasNoc nvarchar(max);
		DECLARE @dp2_cantHorasEsp nvarchar(max);
		DECLARE @dp2_puntoServicio_id int;
        DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp1_vregistro int;
		DECLARE @tmp_vregistro int;
		DECLARE @nuevo_asignacionCab_id int;
		DECLARE @nuevo_planificacionCab_id int;
        DECLARE @replanificar bit;
		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro,@replanificar
		WHILE @@FETCH_STATUS = 0
		BEGIN
			if(@replanificar='True')
            BEGIN
                update dbo.Operarios_planificacioncab set rePlanificar='False' where id=@dp2_id;
            END
            FETCH NEXT FROM cursorIt INTO @dp2_id,@dp2_fecha,@dp2_cantidad,@dp2_cantHoras,@dp2_cantHorasNoc,@dp2_cantHorasEsp,@dp2_puntoServicio_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp1_vregistro,@replanificar
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


USE [aireinegnier]
GO
/****** Object:  Trigger [dbo].[trg_vrs_Operarios_asignacioncab]    Script Date: 3/7/2019 09:56:02 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[trg_vrs_Operarios_hd_asignacioncab]
ON [dbo].[Operarios_asignacioncab]
AFTER UPDATE
AS
	BEGIN
	DECLARE @TransactionName varchar(20) = 'Transactional';
	BEGIN TRAN @TransactionName 
	BEGIN TRY
		DECLARE @nuevoID int;
		DECLARE @dp1_id int;
		DECLARE @dp1_fechaUltimaMod datetime2 ;
		DECLARE @dp1_totalasignado nvarchar(max);
		DECLARE @dp1_puntoServicio_id int;
		DECLARE @dp1_usuario_id int;
        DECLARE @tmp_fechaIncio datetime;
		DECLARE @tmp_fechaFin datetime;
		DECLARE @tmp_vregistro int;
		DECLARE @reasignar bit;

		DECLARE cursorIt CURSOR LOCAL FOR SELECT * FROM inserted
		OPEN cursorIt
		FETCH NEXT FROM cursorIt INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro,@reasignar
		WHILE @@FETCH_STATUS = 0
		BEGIN
			if(@reasignar='True')
            BEGIN
                update dbo.Operarios_asignacioncab set reAsignar='False' where id=@dp1_id;
            END
            FETCH NEXT FROM cursorIt INTO @dp1_id,@dp1_fechaUltimaMod,@dp1_totalasignado,@dp1_puntoServicio_id,@dp1_usuario_id,@tmp_fechaIncio,@tmp_fechaFin,@tmp_vregistro,@reasignar
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

