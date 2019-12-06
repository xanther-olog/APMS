<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
</head>
<body>
    <h3>Entry Log Details</h3>
<?
    function generatePng($str,$img){
        $location="/opt/lampp/htdocs/log_retrieval/".$img;
        $str = base64_decode($str);
        file_put_contents($location, $str);
    }
?>
<?
    $servername="localhost";
    $username="root";
    $password="";
    $dbname="minor_project";
    $name=$_POST["name"];
    $conn=new mysqli($servername , $username , $password , $dbname);
    if ($conn->connect_error){
        die("Connection failed: " . $conn->connect_error);
    }
    $query="SELECT * FROM log_table_in where name='$name'";
    $result=$conn->query($query);
    $cnt=1;
    if ($result->num_rows > 0) {
        echo "<table><tr><th>ID</th><th>Name</th><th>In Time</th><th>Image</th><th>Number Plate </th></tr>";
        while($row = $result->fetch_assoc()) {
          $tempStr=$row["img"];
          $imageName="ImageEntry".$cnt.".png";
          $cnt=$cnt+1;
          generatePng($tempStr,$imageName);
          echo '<tr><td>'.$row["rno"].'</td><td>'.$row["name"].'</td><td>'.$row["in_time"].'</td><td>'.'<img src="'.$imageName.'" size="200px" width="200px"/>'.'</td><td>'.$row["number_plate"].'</td></tr>';
        }
        echo "</table>";
    }
    else{
        echo "No records found!";
    }
?>
    <h3> Exit Log Details </h3>
    <?
        $servername="localhost";
        $username="root";
        $password="";
        $dbname="minor_project";
        $name=$_POST["name"];
        $conn=new mysqli($servername , $username , $password , $dbname);
        if ($conn->connect_error){
            die("Connection failed: " . $conn->connect_error);
        }
        $query="SELECT * FROM log_table_out where name='$name'";
        $result=$conn->query($query);
        $cnt=1;
        if ($result->num_rows > 0) {
            echo "<table><tr><th>ID</th><th>Name</th><th>Out Time</th><th>Image</th><th>Number Plate </th></tr>";
            while($row = $result->fetch_assoc()) {
              $tempStr=$row["img"];
              $imageName="ImageExit".$cnt.".png";
              $cnt=$cnt+1;
              generatePng($tempStr,$imageName);
              echo '<tr><td>'.$row["rno"].'</td><td>'.$row["name"].'</td><td>'.$row["out_time"].'</td><td>'.'<img src="'.$imageName.'" size="200px" width="200px"/>'.'</td><td>'.$row["number_plate"].'</td></tr>';
            }
            echo "</table>";
        }
        else{
            echo "No records found!";
        }
?>
</body>
</html>
