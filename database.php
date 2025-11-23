<?php
$servername = "localhost";
$username = "PocketAdmin";
$password = "KingClarke25#";
$dbname = "PocketChef";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    // Connection successful
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>
