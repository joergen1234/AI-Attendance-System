<?php
    if (isset($_POST['upload'])) {

        $file_name = $_FILES['file']['name'];
        $file_type = $_FILES['file']['type'];
        $file_size = $_FILES['file']['size'];
        $file_tem_loc = $_FILES['file']['tmp_name'];
        $file_store = "G:/oneshot/Training_images/".$file_name;

        move_uploaded_file($file_tem_loc, $file_store);

    }
?>




<!DOCTYPE html>
<html>
<head>
    <br>
    <br> 
    <br>
    <br>
    <br>
    <br>    
    <br>
    <br>
    <br>
    <br>
    <title>Photo Upload</title>
    <link rel="stylesheet" type="text/css" href="Student.css">
</head>
<body>
    <h1>Photo Upload</h1>
   <form action="?" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" name="upload" value="Upload Image">
    </form>

</body>
</html>
