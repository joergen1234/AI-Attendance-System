<?php
session_start();

// Check if user is already logged in
if (isset($_SESSION['username'])) {
    header("Location: dashboard.php");
    exit;
}

// Check if the login form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Perform your login authentication logic here
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Assuming you have a MySQL database setup, you can use the following code to authenticate the user
    $db_host = 'your host';
    $db_username = 'your username';
    $db_password = 'your password';
    $db_name = 'your db name';

    $conn = new mysqli($db_host, $db_username, $db_password, $db_name);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows === 1) {
        $_SESSION['username'] = $username;
        header("Location: dashboard.php");
        exit;
    } else {
        $error = "Invalid username or password";
    }
}
?>


<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <!-- <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Rubik:400,700'> -->
  <link rel="stylesheet" href="./style.css">

</head>
<body>
<?php if (isset($error)) { ?>
        <p><?php echo $error; ?></p>
    <?php } ?>
<div class="login-form">
<form method="POST" action="<?php echo $_SERVER['PHP_SELF']; ?>">
    <h1>Login</h1>
    <div class="content">
      <div class="input-field">
        <input type="text" placeholder="Username" name = "username"autocomplete="nope">
      </div>
      <div class="input-field">
        <input type="password" placeholder="Password" name = "password"autocomplete="new-password">
    <br>
    <div class="action">
    <input type="submit" value="Login">
    </div>
  </form>
</div>


</body>
</html>
