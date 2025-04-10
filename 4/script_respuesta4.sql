-- a. Escribe una consulta que cuente cuántos casos hay por cada TipoAsuntoId.

SELECT TipoAsuntoId, COUNT(*) AS TotalCasos
FROM Asuntos
GROUP BY TipoAsuntoId;


-- b. Escribe otra consulta que calcule el promedio de días entre FechaAlta y FechaResolucion, agrupado por ResolucionId

SELECT ResolucionId, AVG(DATEDIFF(FechaResolucion, FechaAlta)) AS PromedioDias
FROM Asuntos
WHERE FechaResolucion IS NOT NULL AND FechaAlta IS NOT NULL
GROUP BY ResolucionId;
