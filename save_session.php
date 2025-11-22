<?php
// Include your database connection
require_once 'database.php';

header('Content-Type: application/json');

try {
    // Get data from POST request (adjust based on what your app sends)
    $temperature = $_POST['temperature'] ?? $_GET['temperature'] ?? '165°F';
    $timer_duration = $_POST['timer_duration'] ?? $_GET['timer_duration'] ?? '14:58';
    $food_type = $_POST['food_type'] ?? $_GET['food_type'] ?? 'Chicken Breast (15 Min)';
    
    // For the session data from your image
    $session_data = json_encode([
        'sessions_date_to_save' => $_POST['sessions_date_to_save'] ?? '1 Object',
        'session_data' => $_POST['session_data'] ?? '1 Object'
    ]);
    
    // Insert into database
    $sql = "INSERT INTO cooking_sessions (temperature, timer_duration, food_type, session_data) 
            VALUES (:temperature, :timer_duration, :food_type, :session_data)";
    
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':temperature', $temperature);
    $stmt->bindParam(':timer_duration', $timer_duration);
    $stmt->bindParam(':food_type', $food_type);
    $stmt->bindParam(':session_data', $session_data);
    
    if ($stmt->execute()) {
        echo json_encode([
            'success' => true, 
            'message' => 'Session saved successfully',
            'session_id' => $conn->lastInsertId()
        ]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Failed to save session']);
    }
    
} catch(PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Database error: ' . $e->getMessage()]);
}
?>
