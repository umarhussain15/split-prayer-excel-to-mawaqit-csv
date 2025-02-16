# Convert Presidency of Religious Affairs Prayer Time to Mawaqit Prayer Time

This script reads the excel file exported from [Presidency of Religious Affairs](https://namazvakitleri.diyanet.gov.tr/) for a year, then prepares the 12 csv files for each month in the format which can be uploaded to [Mawaqit Admin panel](https://mawaqit.net/en/backoffice/mosque) to set a mosque's prayer times.

Example of all months which Mawaqit expects for a mosque's prayer time: https://mawaqit.net/static/paris-uoif.zip

The script also removes day light saving present in the excel file, as the csv expected by Mawaqit needs to be without daylight saving in the prayer times.

![mawait-warning](images/warning-mawaqit.png)

## Run Script

To run the script first install the required dependencies:

```shell
pip install -r requirements.txt
```

Then you can run the script by providing the excel file name as argument:

```shell
python split-excel-to-csv.py prayer-time-dresden.xlsx
```

The output csv files will be in `mawaqit-<year>`.

Disclaimer: Script generated mostly via ChatGPT.
