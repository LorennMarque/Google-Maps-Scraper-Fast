<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Home</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">

  <style>
    .selected td {
      background-color: #cce5ff;
      transition: background-color 0.3s ease;
      /* Light blue background for selected rows */
    }
  </style>
</head>

<body class="bg-light">
  <div class="container mt-5 card p-5">
    <div class="row sticky-top bg-white">
      <div class="col">
        <h1>CSV results:</h1>
      </div>
      <div class="col text-end">
        <h2 id="checkedCount">0 rows selected</h2>
      </div>
    </div>
    <hr>
    <table class="table table-bordered" id="dataTable">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Website</th>
          <th>Reviews Score</th>
          <th>Reviews Amount</th>
          <th>Phone number</th>
        </tr>
      </thead>
      <tbody>
        <?php
        // Open the CSV file
        $file = fopen('../places_data.csv', 'r');

        // Check if the file is opened successfully
        if ($file) {
          // Read and output each row
          $count = 0;
          while (($row = fgetcsv($file)) !== false) {
            // Assign values to variables
            $count++;
            $name = $row[0];
            $website = $row[1];
            $reviewsScore = $row[2];
            $reviewsAmount = $row[3];
            $phoneNumber = $row[4];
            $googleMapsLink = $row[5];

            // Output the row in the table
            echo '<tr>
                    <td>' . $count . '</td>
                    <td><a href="' . htmlspecialchars($googleMapsLink) . '">' . htmlspecialchars($name) . '</a></td>
                    <td>' . htmlspecialchars($website) . '</td>
                    <td>' . htmlspecialchars($reviewsScore) . '</td>
                    <td>' . htmlspecialchars($reviewsAmount) . '</td>
                    <td><a target="__blank" href="https://wa.me/+54' . htmlspecialchars($phoneNumber) . '">' . htmlspecialchars($phoneNumber) . '</a></td>
                  </tr>';
          }

          // Close the file
          fclose($file);
        } else {
          // Error opening the file
          echo 'Error opening the file.';
        }
        ?>
      </tbody>
    </table>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>

  <script>
    document.addEventListener("DOMContentLoaded", function() {
      const dataTable = document.getElementById("dataTable");
      const checkedCount = document.getElementById("checkedCount");

      // Attach click event listener to table rows
      dataTable.addEventListener("click", function(event) {
        if (event.target.tagName === "TD") {
          const row = event.target.parentElement;

          // Toggle selected class on the clicked row
          row.classList.toggle("selected");

          // Update checked count
          const selectedRows = dataTable.querySelectorAll(".selected").length;
          checkedCount.textContent = selectedRows + " row" + (selectedRows !== 1 ? "s" : "") + " selected";
        }
      });
    });
  </script>
</body>

</html>