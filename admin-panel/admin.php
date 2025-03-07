<?php
$host = "eventdatabase.cxa6gecsas3w.us-east-1.rds.amazonaws.com";
$username = "admin";
$password = "**********";
$dbname = "test";

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch registered users
$sql = "SELECT id, name, email, event FROM registrations";
$result = $conn->query($sql);

echo "<h2>Registered Users</h2>";
if ($result->num_rows > 0) {
    echo "<table border='1'><tr><th>ID</th><th>Name</th><th>Email</th><th>Event</th></tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["id"] . "</td><td>" . $row["name"] . "</td><td>" . $row["email"] . "</td><td>" . $row["event"] . "</td></tr>";
    }
    echo "</table>";
} else {
    echo "No registrations found.";
}

$conn->close();
?>
