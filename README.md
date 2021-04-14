# JR_EGM722_Project
 Repository for the EGM722 Project at Ulster University

To get started with using this code and identifying potential Wildlife Corridors, locate the GitHub Repository at: 
https://github.com/JordanRathb/JR_EGM722_Project
You will require to use Git, GitHub Desktop and Anaconda Navigator for which you will clone the repository onto your local machine and import the environment into Anaconda to install the dependencies of the script to ensure successful execution.

## GitHub Desktop ## 
Install GitHub Desktop from here: https://desktop.github.com/
1.	Load GitHub Desktop and select ‘File’>’Clone Repository’>’URL’
2.	Enter the URL: https://github.com/JordanRathb/JR_EGM722_Project
3.	Select the local path on your machine where you’d like to store the repository.
4.	This will establish the repository on your local machine that allows you to access the files of the script, along with data files and an environment.yml file that will be used to install the main dependencies to successfully execute the code.
5.	Also provided is the licence for the code, establishing means of use along with a READ-ME that details these installation instructions.

## Anaconda Navigator ##
The main modules that are required to successfully execute the code are as follow:
-	Geopandas
-	Shapely
-	Cartopy
-	Matplot

These can be installed within a ‘conda’ environment, via the “environment.yml” file found within your local “JR_EGM722_Project” repository.
1.	To install Anaconda Navigator, please head here and follow the installation instructions: 
	https://docs.anaconda.com/anaconda/install/
2.	Once installed, open the ‘Environment’ panel and click ‘Import’ to select the environment:
3.	Under import, you will need to enter the local path for where the repository is saved, and here you will find the ‘environment.yml’ file to enter under ‘Specification File’: 
4.	Click import and allow the program to install the necessary modules.

## Python IDE ##
To be able to execute and edit the script, you’ll require a Python IDE to allow you to open the script. This project was developed within ‘PyCharm Community’, for which can be downloaded here: 
https://www.jetbrains.com/pycharm/download/#section=windows
It is vital to ensure that your ‘Conda’ environment within your IDE is established correctly, otherwise the required dependencies will not be identified. 
If you are using PyCharm Community, this can be set up within the settings (Ctrl – Alt – S) where under ‘Project: Interpreter’ you can select an existing environment. This should be where you ‘Conda’ environment is set up. 

One the Anaconda environment is established, the modules should be loaded correctly and the script can now be executed.
The script is set to use data located within the repository under a folder titled “data_files”. Here you can choose to replace these with your own dataset concerning the same features for your study region.
