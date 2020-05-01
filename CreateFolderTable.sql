CREATE PROCEDURE `CreateFolderTable`(
	IN `folderName` VARCHAR ( 255 ))
BEGIN
	
	SET @cmd = CONCAT( 'DROP TABLE IF EXISTS ', folderName );
	PREPARE stmt 
	FROM
		@cmd;
	EXECUTE stmt;
	
	SET @cmd = CONCAT( 'CREATE TABLE ', folderName, '
		(PackageID INT PRIMARY KEY AUTO_INCREMENT, 
		PackageIndex INT, 
		PackageName VARCHAR(255), 
	PackageData LONGBLOB)' );
	PREPARE stmt 
	FROM
		@cmd;
	EXECUTE stmt;

END