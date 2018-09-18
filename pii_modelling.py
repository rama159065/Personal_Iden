
# coding: utf-8



import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
np.random.seed(0)
filename = 'pii_feature_current.csv'
#dataset = load_csv(filename)

input_df = pd.read_csv(filename,',')


y = pd.factorize(input_df['label'])[0]
#print(y)
input_data_columns=['email','phone','ip']
input_df['label'] = pd.Categorical.from_codes(y,input_data_columns)

#print(input_df.head())

input_df['is_train'] = np.random.uniform(0, 1, len(input_df)) <= .60
train, test = input_df[input_df['is_train']==True], input_df[input_df['is_train']==False]

#print(test.head())

# Show the number of observations for the test and training dataframes
print('Number of observations in the training data:', len(train))
print('Number of observations in the test data:',len(test))

# Create a list of the feature column's names
features = train.columns[:9]
#print("features: ",features)


# In[2]:


def random_forest_classifier(features, target):
    
    clf = RandomForestClassifier(n_jobs=3,criterion='entropy',random_state=0)
    clf.fit(features, target)
    return clf


# In[3]:


# Create random forest classifier instance
y = pd.factorize(train['label'])[0]
trained_model = random_forest_classifier(train[features], y)
print("Trained model :: ", trained_model)


# In[6]:


from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

test_y = pd.factorize(test['label'])[0]
predictions = trained_model.predict(test[features])
print((predictions))
print("-"*20)
predictions_prob = trained_model.predict_proba(test[features])
print((predictions_prob))
print("-"*20)
for i in range(0, 5):
    print("Actual outcome :: {} and Predicted outcome :: {}".format(list(test_y)[i], predictions[i]))


# In[7]:


# Train and Test Accuracy
print ("Train Accuracy :: ", accuracy_score(y, trained_model.predict(train[features])))
print ("Test Accuracy  :: ", accuracy_score(test_y, predictions))
print ("Confusion matrix \n", confusion_matrix(test_y, predictions))

