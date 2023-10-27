# AutoLivePlot V1.0
_Written by Maria Buckley_

AutoLivePlot is a python script to plot the data from csvs that are being written to in real-time.

All that is required from you is to supply the csvs that the data is being written to, and your data will be plotted in seperate graphs.

## Running the application ##
The program takes three command line arguments:
```
usage: AutoLivePlot.py [-h] [-n NAME] [-x XLABEL] -c CSVS [CSVS ...]

set user arguments

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name to save plot under
  -x XLABEL, --xlabel XLABEL
                        X axis label
  -c CSVS [CSVS ...], --csvs CSVS [CSVS ...]
                        <Required> Path to the csvs to plot
```

Name and Xlabel are aptional for adding further detail to your plot.

The application should be run from a terminal using the comand:
```
  python 3 AutoLivePlot.py -c <path-to-csv1> <path-to-csv2>...
```
