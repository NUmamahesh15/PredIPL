----- DESIGNING MACHINE LEARNING MODELS--------
Before running the colab files to generate the machine learning models,
1.create a folder in google drive.
2.place the colab files IPL_EDA, IPL_models,IPL_preproc, matches.csv, and deliveries.csv in the folder.
3.Mount your drive to colab files in order to access the folder. You can use the below code
		from google.colab import drive
		drive.mount('/content/drive')
After google colab is setup,
1. Run the IPL_preproc.ipynb file. This file will generate the cleaned matches (matches_EDA.csv) and deliveries (deliveries_cleaned)
   files in the folder to be used for EDA and in our python application.
2. Additionaly, this will also generate matches_models.csv, to be used for developing machine learning models.
3. Next, run all the cells of IPL_EDA.ipynb files to get the visualisation.
   P.s. make sure the correct files, cleaned matches and deliveries file, is imported from the previous step.
4. Run the IPL_models.ipynb file. By the end, this file will generate 4 machine learning models such as
   logModel.pkl, NaiveModel.pkl, RandomForestModel.pkl, and SVMModel.pkl representing the models generated from their
   respective machine learning algorithms.
5. Additionally, this will also generate the eval_metric.pkl containing the performance metric of the models.


----- WEB APPLICATION ----
1. First, create a virtual environment in the local machine folder by name "env". This creates a folder by name "env".
2. Activate the virtual environment using command $env\Scripts\activate (windows) and install all the python packages mentioned 
   in the "requirement.txt" file using $ pip install (package).
3. Next, all the machine learning model files and evaluation file generated from the previous stage are downloaded 
   from the drive and placed inside the "models" folder.
4. Cleaned matches, and deliveries file, downloaded from the drive and placed in the "data" folder with the name
   matches_cleaned.csv and deliveries_cleaned.csv respectively.
5. Open the command prompt and run the app.py file using the command $python app.py
6. The app will be running on the local host http://127.0.0.1:5000/


