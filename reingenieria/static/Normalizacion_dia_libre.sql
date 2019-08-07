DECLARE @id INT;
DECLARE @MyCursor CURSOR;
BEGIN
    SET @MyCursor = CURSOR FOR
      SELECT id FROM   Operarios_operario WHERE id NOT IN (SELECT Operarios_dialibre.id_operario_id 
                   FROM Operarios_dialibre )

	OPEN @MyCursor 
    FETCH NEXT FROM @MyCursor 
    INTO @id

	WHILE @@FETCH_STATUS = 0
		BEGIN
			INSERT INTO Operarios_dialibre(fechaCreacion, domEnt,domSal,id_operario_id) VALUES(CURRENT_TIMESTAMP,'00:00:00','23:59:00',@id);

			FETCH NEXT FROM @MyCursor 
			INTO @id
		END;
		
    CLOSE @MyCursor ;
    DEALLOCATE @MyCursor;
END;



	
