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
    function convertToMonth($x){
        $result="";
        if($x=="01"){
            $result="Jan";
        }
        elseif($x=="02"){
            $result="Feb";
        }
        elseif($x=="03"){
            $result="Mar";
        }
        elseif($x=="04"){
            $result="Apr";
        }
        elseif($x=="05"){
            $result="May";
        }
        elseif($x=="06"){
            $result="Jun";
        }
        elseif($x=="07"){
            $result="Jul";
        }
        elseif($x=="08"){
            $result="Aug";
        }
        elseif($x=="09"){
            $result="Sep";
        }
        elseif($x=="10"){
            $result="Oct";
        }
        elseif($x=="11"){
            $result="Nov";
        }
        elseif($x=="12"){
            $result="Dec";
        }
        return $result;
    }
?>
<?
    $servername="localhost";
    $username="root";
    $password="";
    $dbname="minor_project";
    $date=$_POST["date"];
    $dateArray=explode("-",$date);
    $yr=$dateArray[0];
    $mon=convertToMonth((string)$dateArray[1]);
    $day=$dateArray[2];
    $conn=new mysqli($servername , $username , $password , $dbname);
    if ($conn->connect_error){
        die("Connection failed: " . $conn->connect_error);
    }
    $cnt=1;
    $query="SELECT * FROM log_table_in WHERE in_time LIKE '____$mon%' AND in_time LIKE '________$day%' AND in_time LIKE '%$yr'";
    $result=$conn->query($query);
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
        echo "No Records Found";
    }

?>
<h3> Exit Log Details </h3>
<?
    $servername="localhost";
    $username="root";
    $password="";
    $dbname="minor_project";
    $date=$_POST["date"];
    $dateArray=explode("-",$date);
    $yr=$dateArray[0];
    $mon=convertToMonth((string)$dateArray[1]);
    $day=$dateArray[2];
    $conn=new mysqli($servername , $username , $password , $dbname);
    if ($conn->connect_error){
        die("Connection failed: " . $conn->connect_error);
    }
    $cnt=1;
    $query="SELECT * FROM log_table_out WHERE out_time LIKE '____$mon%' AND out_time LIKE '________$day%' AND out_time LIKE '%$yr'";
    $result=$conn->query($query);
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
        echo "No Records Found";
    }

?>

</body>
</html>
