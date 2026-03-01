
<?php
session_start();

// Check if user is not logged in
if (!isset($_SESSION['username'])) {
    header("Location: updatedlogin.php");
    exit;
}

// Get the logged-in username
$username = $_SESSION['username'];

// Handle the file downloading logic
$folderPath = "G:/oneshot/Attendance"; // Replace with the actual path to the folder

if (isset($_GET['file'])) {
    $fileName = $_GET['file'];

    // Validate the file name to prevent unauthorized access
    $validFiles = scandir($folderPath);
    if (in_array($fileName, $validFiles)) {
        $filePath = $folderPath . '/' . $fileName;

        // Send the file to the user for download
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . $fileName . '"');
        header('Content-Length: ' . filesize($filePath));
        readfile($filePath);
        exit;
    } else {
        echo "Invalid file.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f2f2f2;
        }

        h2 {
            color: #333;
            text-align: center;
        }

        p {
            color: #666;
            text-align: center;
        }

        h3 {
            color: #333;
        }

        ul {
            padding: 0;
            list-style-type: none;
        }

        li {
            margin-bottom: 10px;
        }

        a {
            color: #0000ff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .logout-link {
            position: absolute;
            top: 20px;
            right: 20px;
        }
    </style>
    <title>Dashboard</title>
</head>
<body>
    <h2>Welcome, <?php echo $username; ?></h2>
    <p>This is your dashboard.</p>

    <h3>Attendance</h3>
    <ul>
        <?php
        $folderContents = scandir($folderPath);
        foreach ($folderContents as $file) {
            if ($file !== '.' && $file !== '..') {
                echo '<li><a href="?file=' . urlencode($file) . '">' . $file . '</a></li>';
            }
        }
        ?>
    </ul>
    <a class="logout-link" href="logout.php">Logout</a>


</body>
</html>