#!/usr/bin/env python
# coding: utf-8

# ## StatQuest!
# # Support Vector Machines in Python, From Start To Finish
# Copyright 2020, Joshua Starmer
# 
# ----
# 
# In this lesson we will build this **Support Vector Machine** for **classification** (shown below) using **scikit-learn** and the **Radial Basis Function (RBF) Kernel**. Our training data set contains continuous and categorical data from the **[UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)** to predict whether or not a patient has **[heart disease](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)**.
# 
# <img src="svm.png" alt="A Support Vector Machine" style="width: 600px;">
# 
# **Support Vector Machines** are one of the best machine learning methods when getting the correct answer is a higher priorty than understanding why you get the correct answer, and they work really well with relatively small datasets.
# 
# In this lesson you will learn about...
# 
# - **[Importing Data from a File](#download-the-data)**
# 
# - **[Missing Data](#identify-and-deal-with-missing-data)**
#     - Identifying Missing Data
#     - Dealing with Missing Data
#     
# 
# - **[Formatting the Data for Support Vector Machines](#format-the-data)**
# 
#     - Splitting data into Dependent and Independent Variables
#     - One-Hot-Encoding
#     - Centering and Scaling the Data
#     
# 
# - **[Building a Preliminary Support Vector Machine](#build-svm)**
# 
# - **[Opimizing Parameters with Cross Validation](#optimize-svm)**
#     - Using Cross Validation to find the best Values for Gamma and Regularization
# 
# 
# - **[Building, Evaluating, Drawing and Interpreting the Final Support Vector Machine](#draw-svm)**
# 
# #### NOTE:
# This tutorial assumes that you are already know the basics of coding in **Python** and are familiar with the theory behind **[Support Vector Machines](https://youtu.be/efR1C6CvhmE)**, the **[Radial Basis Function (RBF)](https://youtu.be/Qc5IyLW_hns)**, **[Regularization](https://youtu.be/Q81RR3yKn30)**, **[Cross Validation](https://youtu.be/fSytzGwwBVw)** and **[Confusion Matrices](https://youtu.be/Kdsp6soqA7o)**. If not, check out the **StatQuests** by clicking on the links for each topic.

# #### Also Note:
# I strongly encourage you to play around with the code. Playing with the code is the best way to learn from it.

# ***

# # Import the modules that will do all the work
# The very first thing we do is load in a bunch of python modules. Python, itself, just gives us a basic programming language. These modules give us extra functionality to import the data, clean it up and format it, and then build, evaluate and draw the support vector machine. 
# 
# **NOTE:** You will need **Python 3** and have at least these versions for each of the following modules: 
# - pandas >= 0.25.1
# - numpy >= 1.17.2
# - sklearn >= 0.22.1
#  
# If you installed **Python 3** with [Anaconda](https://www.anaconda.com/), you can check which version you have with the command: `conda list`. If, for example, your version of `scikit-learn` is older than 0.22.1, then the easiest thing to do is just update all of your **Anaconda** packages with the following command: `conda update --all`. However, if you only want to update `scikit-learn`, then you can run this command: `conda install scikit-learn=0.22.1`.

# In[ ]:


import pandas as pd # pandas is used to load and manipulate data and for One-Hot Encoding
import numpy as np # numpy is used to calculate the mean and standard deviation
import matplotlib.pyplot as plt # matplotlib is for drawing graphs
import matplotlib.colors as colors
from sklearn.model_selection import train_test_split # split  data into training and testing sets
from sklearn.preprocessing import scale # scale and center data
from sklearn.svm import SVC # this will make a support vector machine for classificaiton
from sklearn.model_selection import GridSearchCV # this will do cross validation
from sklearn.metrics import confusion_matrix # this creates a confusion matrix
from sklearn.metrics import plot_confusion_matrix # draws a confusion matrix
from sklearn.decomposition import PCA # to perform PCA to plot the data


# -----

# <a id="download-the-data"></a>
# # Import the data
# Now we load in a dataset from the **[UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)**.
# Specifically, we are going to use the **[Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)**. This dataset will allow us to predict if someone has heart disease based on their sex, age, blood pressure and a variety of other metrics.
# 
# **NOTE:** When **pandas** (**pd**) reads in data, it returns a **data frame**, which is a lot like a spreadsheet. The data are organized in rows and columns and each row can contain a mixture of text and numbers. The standard variable name for a **data frame** is the initials **df**, and that is what we will use here:

# In[ ]:


df = pd.read_csv('processed.cleveland.data', 
                 header=None)


# Now that we have loaded the data into a **data frame** called **df**, let's look at the first five rows using the `head()` function:

# In[ ]:


df.head()


# We see that instead of nice column names, we just have column numbers.  Since nice column names would make it easier to know how to format the data, let's replace the column numbers with the following column names:
# - **age**,
# - **sex**,
# - **cp**, chest pain
# - **restbp**, resting blood pressure (in mm Hg)
# - **chol**, serum cholesterol in mg/dl
# - **fbs**, fasting blood sugar
# - **restecg**, resting electrocardiographic results
# - **thalach**,  maximum heart rate achieved
# - **exang**, exercise induced angina
# - **oldpeak**, ST depression induced by exercise relative to rest
# - **slope**, the slope of the peak exercise ST segment.
# - **ca**, number of major vessels (0-3) colored by fluoroscopy
# - **thal**, this is short of thalium heart scan.
# - **hd**, diagnosis of heart disease, the predicted attribute

# In[ ]:


df.columns = ['age',
              'sex',
              'cp',
              'restbp',
              'chol',
              'fbs',
              'restecg',
              'thalach',
              'exang',
              'oldpeak',
              'slope',
              'ca',
              'thal',
              'hd']
df.head()


# Hooray! We have replaced the column numbers with nice, easy to remember names. Now that we have the data in a **data frame** called **df**, we are ready to identify and deal with **Missing Data**.

# ----

# In[ ]:





# <a id="identify-and-deal-with-missing-data"></a>
# # Missing Data Part 1: Identifying Missing Data
# Unfortunately, the biggest part of any data analysis project is making sure that the data is correctly formatted and fixing it when it is not. The first part of this process is identifying and dealing with **Missing Data**.
# 
# **Missing Data** is simply a blank space, or a surrogate value like **NA**, that indicates that we failed to collect data for one of the features. For example, if we forgot to ask someone's age, or forgot to write it down, then we would have a blank space in the dataset for that person's **age**.
# 
# There are two main ways to deal with missing data:
# 1. We can remove the rows that contain missing data from the dataset. This is relatively easy to do, but it wastes all of the other values that we collected. How a big of a waste this is depends on how important this missing value is for classification. For example, if we are missing a value for **age**, and **age** is not useful for classifying if people have heart disease or not, then it would be a shame to throw out all of someone's data just because we do not have their **age**.
# 2. We can **impute** the values that are missing. In this context **impute** is just a fancy way of saying "we can make an educated guess about about what the value should be". Continuing our example where we are missing a value for **age**, instead of throwing out the entire row of data, we can fill the missing value with the average age or the median age, or use some other, more sophisticated approach, to guess at an appropriate value.
# 
# In this section, we'll focus on identifying missing values in the dataset. 
# 
# First, let's see what sort of data is in each column.

# In[ ]:


df.dtypes


# We see that that they are almost all `float64`, however, two columns, **ca** and **thal**, have the `object` type and one column, **hd** has `int64`.
# 
# The fact that the **ca** and **thal** columns have `object` data types suggests there is something funny going on in them. `object` datatypes are used when there are mixtures of things, like a mixture of numbers and letters. In theory, both **ca** and **thal** should just have a few values representing different categories, so let's investigate what's going on by printing out their unique values. We'll start with **ca**:

# In[ ]:


df['ca'].unique()


# We see that **ca** contains numbers (0.0, 3.0, 2.0 and 1.0) and questions marks (?). The numbers represent the number of blood vessels that we lit up by fluoroscopy and the question marks represent missing data.
# 
# Now let's look at the unique values in **thal**.

# In[ ]:


df['thal'].unique()


# Again, **thal** also contains a mixture of numbers, representing the different diagnoses from the thalium heart scan, and question marks, which represent missing values.
# 
# Now that we have identified some missing value, we need to deal with them.

# ----

# # Missing Data Part 2: Dealing With Missing Data
# 
# Since scikit-learn's support vector machines do not support datasets with missing values, we need to figure out what to do these question marks. We can either delete these patients from the training dataset, or impute values for the missing data. First let's see how many rows contain missing values.

# In[ ]:


len(df.loc[(df['ca'] == '?') | (df['thal'] == '?')])


# Since only 6 rows have missing values, let's look at them.

# In[ ]:


df.loc[(df['ca'] == '?') | (df['thal'] == '?')]


# Now let's count the number of rows in the full dataset.

# In[ ]:


len(df)


# So 6 of the **303** rows, or **2%**, contain missing values. Since **303 - 6 = 297**, and **297** is plenty of data to build a support vector machine, we will remove the rows with missing values, rather than try to impute their values. We do this by selecting all of the rows that do not contain question marks in either the **ca** or **thal** columns:

# In[ ]:


df_no_missing = df.loc[(df['ca'] != '?') & (df['thal'] != '?')]


# Since `df_no_missing` has **6** fewer rows than the original `df`, it should have **297** rows.

# In[ ]:


len(df_no_missing)


# Hooray! The math works out. However, we can also make sure **ca** no longer contains question marks by printing its unique values:

# In[ ]:


df_no_missing['ca'].unique()


# And we can also do the same thing for **thal**:

# In[ ]:


df_no_missing['thal'].unique()


# BAM! We have verified that `df_no_missing` does not contain any missing values. **NOTE:** **ca** and **thal** still have the `object` data type. That's OK. Now we are ready to format the data for making a **Support Vector Machine**.

# ----

# <a id="format-the-data"></a>
# # Format Data Part 1: Split the Data into Dependent and Independent Variables
# 
# Now that we have taken care of the missing data, we are ready to start formatting the data for making a **Support Vector Machine**.
# 
# The first step is to split the data into two parts:
# 1. The columns of data that we will use to make classifications
# 2. The column of data that we want to predict.
# 
# We will use the conventional notation of `X` (capital **X**) to represent the columns of data that we will use to make classifications and `y` (lower case **y**) to represent the thing we want to predict. In this case, we want to predict **hd** (heart disease).
# 
# **NOTE** The reason we deal with missing data before splitting it into **X** and **y** is that if we remove rows, splitting after ensures that each row in **X** correctly corresponds with the appropriate value in **y**.
# 
# **ALSO NOTE:** In the code below we are using `copy()` to copy the data *by value*. By default, pandas uses copy *by reference*. Using `copy()` ensures that the original data `df_no_missing` is not modified when we modify `X` or `y`. In other words, if we make a mistake when we are formatting the columns for classification trees, we can just re-copy `df_no_missing`, rather than reload the original data and remove the missing values etc.

# In[ ]:


X = df_no_missing.drop('hd', axis=1).copy() # alternatively: X = df_no_missing.iloc[:,:-1].copy()
X.head()


# In[ ]:


y = df_no_missing['hd'].copy()
y.head()


# Now that we have created **X**, which has the data we want to use to make predictions, and **y**, which has the data we want to predict, we are ready ton continue formatting **X** so that it is suitable for making a **Support Vector Machine**.

# ----

# <a id="one-hot-encoding"></a>
# # Format the Data Part 2: One-Hot Encoding
# 
# Now that we have split the data frame into two pieces, `X`, which contains the data we will use to make, or predict, classifications, and `y`, which contains the known classifications in our training dataset, we need to take a closer look at the variables in `X`. The list bellow tells us what each variable represents and the type of data (**float** or **categorical**) it should contain:
# 
# - **age**, **Float**
# - **sex** - **Category**
#   - 0 = female
#   - 1 = male
# - **cp**, chest pain, **Category**
#   - 1 = typical angina
#   - 2 = atypical angina
#   - 3 = non-anginal pain
#   - 4 = asymptomatic
# - **restbp**, resting blood pressure (in mm Hg), **Float**
# - **chol**, serum cholesterol in mg/dl, **Float**
# - **fbs**, fasting blood sugar, **Category**
#   - 0 = >=120 mg/dl
#   - 1 = <120 mg/dl
# - **restecg**, resting electrocardiographic results, **Category**
#   - 1 = normal
#   - 2 = having ST-T wave abnormality
#   - 3 = showing probable or definite left ventricular hypertrophy
# - **thalach**,  maximum heart rate achieved, **Float**
# - **exang**, exercise induced angina, **Category**
#   - 0 = no
#   - 1 = yes
# - **oldpeak**, ST depression induced by exercise relative to rest. **Float**
# - **slope**, the slope of the peak exercise ST segment, **Category**
#   - 1 = upsloping
#   - 2 = flat
#   - 3 = downsloping
# - **ca**, number of major vessels (0-3) colored by fluoroscopy, **Float**
# - **thal**, thalium heart scan, **Category**
#   - 3 = normal (no cold spots)
#   - 6 = fixed defect (cold spots during rest and exercise)
#   - 7 = reversible defect (when cold spots only appear during exercise)
# 
# Now, just to review, let's look at the data types in `X` to remember how python is seeing the data right now.

# In[ ]:


X.dtypes


# So, we see that **age**, **restbp**, **chol** and **thalach** are all `float64`, which is good, because we want them to be floating point numbers. All of the other columns, however, need to be inspected to make sure they only contain reasonable values, and some of them need to change. This is because, while **scikit learn Support Vector Machines** natively support continuous data, like resting blood preasure (**restbp**) and maximum heart rate (**thalach**), they do not natively support categorical data, like chest pain (**cp**), which contains 4 different categories. Thus, in order to use categorical data with **scikit learn Support Vector Machines**, we have to use a trick that converts a column of categorical data into multiple columns of binary values. This trick is called **One-Hot Encoding**.
# 
# At this point you may be wondering, "what's wrong with treating categorical data like continuous data?" To answer that question, let's look at an example: For the **cp** (chest pain) column, we have 4 options:
# 1. typical angina
# 2. atypical angina
# 3. non-anginal pain
# 4. asymptomatic
# 
# If we treated these values, 1, 2, 3 and 4, like continuous data, then we would assume that 4, which means "asymptomatic", is more similar to 3, which means "non-anginal pain", than it is to 1 or 2, which are other types of chest pain. That means the support vector machine would be more likely to cluster the patients with 4s and 3s together than the patients with 4s and 1s together. In contrast, if we treat these numbers like categorical data, then we treat each one a separate category that is no more or less similar to any of the other categories. Thus, the likelihood of clustering patients with 4s with 3s is the same as clustering 4s with 1s, and that approach is more reasonable.
# 
# Now let's inspect and, if needed, convert the columns that contain categorical and integer data into the correct datatypes. We'll start with **cp** (chest pain) by inspecting all of its unique values:
# <!-- We'll start with the three colunms that should only contain 0s and 1s. **sex**. First, let's make sure it only contains `0` (for **female**) and `1` (for **male**). -->

# In[ ]:


X['cp'].unique()


# So, the good news is that **cp** only contains the values it is supposed to contain, so we will convert it, using **One-Hot Encoding**, into a series of columns that only contains **0s** and **1s**.

# <!-- Now we need to deal with **cp** (chest pain), **restecg** (resting electrocardiographic results), **slope** (the slope of the peak exercise ST segment) and **thal** (thalium heart scan).
#  -->
# **NOTE:** There are many different ways to do **One-Hot Encoding** in Python. Two of the more popular methods are `ColumnTransformer()` (from **scikit-learn**) and `get_dummies()` (from **pandas**), and the both methods have pros and cons. `ColumnTransformer()` has a very cool feature where it creates a persistent function that can validate data that you get in the future. For example, if you build your **Support Vector Machine** using a categorical variable **favorite color** that has **red**, **blue** and **green** options, then `ColumnTransformer()` can remember those options and later on when your **Support Vector Machine** is being used in a production system, if someone says their favorite color is **orange**, then `ColumnTransformer()` can throw an error or handle the situation in some other nice way. The downside of `ColumnTransformer()` is that it turns your data into an array and looses all of the column names, making it harder to verify that your usage of `ColumnTransformer()` worked as you intended it to. In contrast, `get_dummies()` leaves your data in a dataframe and retains the column names, making it much easier to verify that it worked as intended. However, it does not have the persistent behavior that `ColumnTransformer()` has. So, for the sake of learning how **One-Hot Encoding** works, I prefer to use `get_dummies()`. However, once you are comfortable with **One-Hot Encoding**, I encourage you to investigate using `ColumnTransformer()`.
# 
# First, before we commit to converting **cp** with **One-Hot Encoding**, let's just see what happens when we convert **cp** without saving the results. This will make it easy to see how `get_dummies()` works.

# In[ ]:


pd.get_dummies(X, columns=['cp']).head()


# As we can see in the printout above, `get_dummies()` puts all of the columns it does not process in the front and it puts **cp** at the end. It also splits **cp** into **4** columns, just like we expected it. **cp_1.0** is `1` for any patient that scored a **1** for chest pain and `0` for all other patients. **cp_2.0** is `1` for any patient that scored **2** for chest pain and `0` for all other patients. **cp_3.0** is `1` for any patient that scored **3** for chest pain and **cp_4.0** is `1` for any patient that scored **4** for chest pain.
# 
# Now that we see how `get_dummies()` works, let's use it on the four categorical columns that have more than 2 categories and save the result.
# 
# **NOTE:** In a real situation (not a tutorial like this), you should verify all 5 of these columns to make sure they 
# only contain the accepted categories. However, for this tutorial, I've already done that for us, so we can skip that step.

# In[ ]:


X_encoded = pd.get_dummies(X, columns=['cp',
                                       'restecg',
                                       'slope', 
                                       'thal'])
X_encoded.head()


# # BAM!!!
# Now we need to talk about the **3** categorical columns that only contain **0**s and **1**s: **sex**, **fbs** (fasting blood sugar), and **exang** (exercise induced angina). As we can see, **One-Hot Encoding** converts a column with more than **2** categories, like **cp** (chest pain) into multiple columns of **0**s and **1**s. Since **sex**, **fbs**, and **exang** only have **2** categories and only contain **0**s and **1**s to begin with, we do not have to do anything special to them, so we're done formatting the data for the **Support Vector Machine**.
# 
# **NOTE:** In practice we would use `unique()` to verify that they only contain **0**s and **1**s, but to save time...trust me!

# Now, one last thing before we build a **Support Vector Machine**.  `y` doesn't just contain **0**s and **1**s. Instead, it has **5** different levels of heart disease. **0 =** no heart disease and **1-4** are various degrees of heart disease. We can see this with `unique()`:

# In[ ]:


y.unique()


# Since we're only making a support vector machine that does simple classification and only care if someone has heart disease or not, we need to convert all numbers **> 0** to **1**.

# In[ ]:


y_not_zero_idx = y > 0
y[y_not_zero_idx] = 1
y.unique()


# # Double BAM!!!
# 
# We have finally finished formatting the data for making a **Support Vector Machine**, so let's do it!!!

# ----

# <a id="center-and-scale"></a>
# # Format the Data Part 3: Centering and Scaling
# 
# The **Radial Basis Function (RBF)** that we are using with our **Support Vector Machine** assumes that the data are centered and scaled, so we need to do this to both the training and testing datasets.
# 
# **NOTE:** We split the data into training and testing datasets and then scale them separately to avoid **Data Leakage**. **Data Leakage** occurs when information about the training dataset currupts or influences the testing dataset.

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, random_state=42)
X_train_scaled = scale(X_train)
X_test_scaled = scale(X_test)


# ----

# <a id="build-svm"></a>
# # Build A Preliminary Support Vector Machine
# At long last, the data is correctly formatted for making a **Support Vector Machine**!!! So let's do it.

# In[ ]:


clf_svm = SVC(random_state=42)
clf_svm.fit(X_train_scaled, y_train)


# OK, we've built a **Support Vector Machine** for classification. Let's see how it performs on the **Testing Dataset** and draw a **Confusion Matrix**.

# In[ ]:


plot_confusion_matrix(clf_svm, 
                      X_test_scaled, 
                      y_test, 
                      display_labels=["Does not have HD", "Has HD"])


# In the confusion matrix, we see that of the **40 + 2 = 42** people that did not have **Heart Disease**, **40 (95%)** were correctly classified. And of the **4 + 29 = 33** people that have **Heart Disease**, **29 (88%)** were correctly classified. So the support vector machine did pretty well without any optimization. That said, it is possible that we can improve predictions using **Cross Validation** to optimize the parameters.

# ----

# <a id="optimize-svm"></a>
# # Optimize Parameters with Cross Validation and GridSearchCV()
# 
# Optimizing a **Support Vector Machine** is all about finding the best value for **gamma**, and, potentially, the regularization parameter, **C**. So let's see if we can find better parameters values using cross validation in hope that we can improve the accuracy with the **Testing Dataset**.
# 
# Since we have two parameters to optimize, we will use `GridSearchCV()`. We specify a bunch of potential values for **gamma** and **C** and `GridSearchCV()` tests all possible combinations of the parameters for us.

# In[ ]:


num_features = np.size(X_train_scaled, axis=1)
param_grid = [
  {'C': [1, 10, 100, 1000], 
   'gamma': [1/num_features, 1, 0.1, 0.01, 0.001, 0.0001], 
   'kernel': ['rbf']},
]
## NOTE: We are includeing C=1 and gamma=1/(num_features * X_train_scaled.var())
## as possible choices since they are the default values.
## ALSO NOTE: Because X_train_scaled.var() = 1 [remember, X_train_scaled = scale(X_train)],
## 1/(num_features * X_train_scaled.var()) = 1/num_features

optimal_params = GridSearchCV(
        SVC(), 
        param_grid,
        cv=5,
        scoring='roc_auc', # NOTE: The default value for scoring results in worse performance...
        ## For more scoring metics see: 
        ## https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        verbose=0 # NOTE: If you want to see what Grid Search is doing, set verbose=2
    )

optimal_params.fit(X_train_scaled, y_train)
print(optimal_params.best_params_)


# And we see that the ideal value for `C` is **10** and the ideal value for `gamma` is **0.001**.

# ----

# <a id="draw-svm"></a>
# # Building, Evaluating, Drawing, and Interpreting the Final Support Vector Machine
# 
# Now that we have the ideal values for `C` and `gamma` we can build the final **Support Vector Machine**:

# In[ ]:


clf_svm = SVC(random_state=42, C=10, gamma=0.0001)
clf_svm.fit(X_train_scaled, y_train)


# Now let's draw another confusion matrix to see if the optimized support vector machine does better.

# In[ ]:


plot_confusion_matrix(clf_svm, 
                      X_test_scaled, 
                      y_test, 
                      display_labels=["Does not have HD", "Has HD"])


# And the results from the *optimized* **Support Vector Machine** are just a little bit better than before. Classifications for
# people that *do not have* **heart disease** are the same as before, but we are one classification better for people *with* **heart disease**, **91%**.

# The last thing we are going to do is draw the optimized support vector machine decision boundary and discuss how to interpret it.
# 
# The first thing we need to do is count the number of columns in **X**:

# In[ ]:


len(df.columns)


# So we see that there are **14** features, or columns, in **X**. 
# This is a problem because it would require a 14-dimensional graph, one dimension per feature used to make predictions, to plot the data in its raw form. If we wanted to, we could just pick two features at random to use as x and y-axes on our graph, but instead , we will use **PCA** (Principal Component Analysis) to combine the **14** features into **2** orthogonal meta-features that we can use as axes for a graph. If you don't already know about PCA, don't sweat it. For now, just know that it is a way to shrink a 14-dimensional graph into a 2-dimensional graph.
# 
# However, before we shrink the graph, let's first determine how accurate the shrunken graph will be. If it's relatively accurate, than it makes sense to draw the 2-Dimensional graph. If not, the shrunken graph will not be very useful. We can determine the accuracy of the graph by drawing something called a **scree plot**.

# In[ ]:


pca = PCA() # NOTE: By default, PCA() centers the data, but does not scale it.
X_train_pca = pca.fit_transform(X_train_scaled)

per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = [str(x) for x in range(1, len(per_var)+1)]
 
plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Components')
plt.title('Scree Plot')
plt.show()


# The scree plot shows that the first principal component, PC1, accounts for a relatively large amount of variation in the raw data, and this means that it will be a good candidate for the x-axis in the 2-dimensional graph. Since PC2 accounts for the next largest amount of variance, we will use that for the y-axis.
# 
# Now we will draw the PCA graph. NOTE: This code is quite technical, but we don't have to type it in and there are comments that explain each step.

# In[ ]:


train_pc1_coords = X_train_pca[:, 0] 
train_pc2_coords = X_train_pca[:, 1]

## NOTE:
## pc1 contains the x-axis coordinates of the data after PCA
## pc2 contains the y-axis coordinates of the data after PCA

## Now center and scale the PCs...
pca_train_scaled = scale(np.column_stack((train_pc1_coords, train_pc2_coords)))

## Now we optimize the SVM fit to the x and y-axis coordinates
## of the data after PCA dimension reduction...
num_features = np.size(pca_train_scaled, axis=1)
param_grid = [
  {'C': [1, 10, 100, 1000], 
   'gamma': [1/num_features, 1, 0.1, 0.01, 0.001, 0.0001], 
   'kernel': ['rbf']},
]

optimal_params = GridSearchCV(
        SVC(), 
        param_grid,
        cv=5,
        scoring='roc_auc', # NOTE: The default value for scoring results in worse performance...
        ## For more scoring metics see: 
        ## https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
        verbose=0 # NOTE: If you want to see what Grid Search is doing, set verbose=2
    )

optimal_params.fit(pca_train_scaled, y_train)
print(optimal_params.best_params_)


# In[ ]:


clf_svm = SVC(random_state=42, C=100, gamma=0.0001)
clf_svm.fit(pca_train_scaled, y_train)

## Transform the test dataset with the PCA...
X_test_pca = pca.transform(X_test_scaled)
test_pc1_coords = X_test_pca[:, 0] 
test_pc2_coords = X_test_pca[:, 1]

## Now create a matrix of points that we can use to show
## the decision regions.
## The matrix will be a little bit larger than the
## transformed PCA points so that we can plot all of
## the PCA points on it without them being on the edge
x_min = test_pc1_coords.min() - 1
x_max = test_pc1_coords.max() + 1

y_min = test_pc2_coords.min() - 1
y_max = test_pc2_coords.max() + 1

xx, yy = np.meshgrid(np.arange(start=x_min, stop=x_max, step=0.1),
                     np.arange(start=y_min, stop=y_max, step=0.1))

## now we will classify every point in that 
## matrix with the SVM. Points on one side of the 
## classification boundary will get 0, and points on the other
## side will get 1.
Z = clf_svm.predict(np.column_stack((xx.ravel(), yy.ravel())))
## Right now, Z is just a long array of lots of 0s and 1s, which
## reflect how each point in the mesh was classified.
## We use reshape() so that each classification (0 or 1) corresponds
## to a specific point in the matrix.
Z = Z.reshape(xx.shape)

fig, ax = plt.subplots(figsize=(10,10))
## now we will use contourf() to draw a filled contour plot
## using the matrix values and classifications. 
## The contours will be filled according to the 
## predicted classifications (0s and 1s) in Z
ax.contourf(xx, yy, Z, alpha=0.1)

## now create custom colors for the actual data points
cmap = colors.ListedColormap(['#e41a1c', '#4daf4a'])
## now draw the actual data points - these will
## be colored by their known (not predcited) classifications
## NOTE: setting alpha=0.7 lets us see if we are covering up a point 

scatter = ax.scatter(test_pc1_coords, test_pc2_coords, c=y_test, 
               cmap=cmap, 
               s=100, 
               edgecolors='k', ## 'k' = black
               alpha=0.7)

## now create a legend
legend = ax.legend(scatter.legend_elements()[0], 
                   scatter.legend_elements()[1],
                    loc="upper right")
legend.get_texts()[0].set_text("No HD")
legend.get_texts()[1].set_text("Yes HD")

## now add axis labels and titles
ax.set_ylabel('PC2')
ax.set_xlabel('PC1')
ax.set_title('Decison surface using the PCA transformed/projected features')
## plt.savefig('svm.png')
plt.show()


# # BAM!!!
# 
# The pink side of the graph on the left is the area were all datapoints will be predicted to *not have* heart disease. The yellow side of the graph on the right is the area where all datapoints will be predicted to *have* heart disease. The the dots are datapoints in the training dataset and are color coded by their known classifications: red is for those that did *not have* heart disease and green is for those that *did* have heart disease.
# 
# **NOTE:** The results are close to what we reported in the confusion matrix, but not exactly the same. This is because how we originall fit the SVM to all of the scaled data for the confusion matrix. For the picture, we only fit the SVM to the first two principal components.

# -----

# # In conclusion we...
# 
# - **[Loaded the Data From a File](#download-the-data)**
# 
# - **[Identified and Dealt with Missing Data](#identify-and-deal-with-missing-data)**
# 
# - **[Formatted the Data for a Support Vector Machine using One-Hot Encoding](#one-hot-encoding)**
# 
# - **[Built a Support Vector Machine for Classification](#build-svm)**
# 
# - **[Optimized the Support Vector Machine with Cross Validation](#optimize-svm)**
# 
# - **[Built, Drew, Interpreted and Evaluated the Final Support Vector Machine](#draw-svm)**

# # TRIPLE BAM!!!
