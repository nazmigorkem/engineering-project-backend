import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class MachineLearning:

    @staticmethod
    def test_methods():
        MachineLearning.run_classifier(lambda: KNeighborsClassifier(), 'knn')
        MachineLearning.run_classifier(lambda: GaussianNB(), 'nb')
        MachineLearning.run_classifier(lambda: MLPClassifier(), 'nn')
        MachineLearning.run_classifier(lambda: DecisionTreeClassifier(), 'dt')  #
        MachineLearning.run_classifier(lambda: DecisionTreeClassifier(criterion='entropy'), 'dte')
        MachineLearning.run_classifier(lambda: RandomForestClassifier(), 'rf')  #
        MachineLearning.run_classifier(lambda: SVC(kernel='rbf'), 'svc-rbf')
        MachineLearning.run_classifier(lambda: SVC(kernel='poly'), 'svc-poly')  #

    @staticmethod
    def export_trained_model():
        clf = MachineLearning.run_classifier(lambda: BaggingClassifier(estimator=MLPClassifier(), n_estimators=10), 'bagging-nn')
        dump(clf, 'trained_model.joblib')

    @staticmethod
    def read_data():
        data = pd.read_csv('data.csv')

        X = data.drop(['dark_activity'], axis=1)
        X = pd.get_dummies(X)

        y = data['dark_activity']
        y = LabelEncoder().fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=27)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def run_classifier(classifier, name):
        X_train, X_test, y_train, y_test = MachineLearning.read_data()
        c = classifier()
        c.fit(X_train.values, y_train)
        y_pred_en = c.predict(X_test.values)
        y_pred_train_en = c.predict(X_train.values)
        MachineLearning.print_metrics(c, X_test, y_train, y_test, y_pred_train_en, y_pred_en, name)
        return c

    @staticmethod
    def print_metrics(classifier, X_test, y_train, y_test, y_pred_train_en, y_pred_en, name):
        print(f'0.6-{name}')
        print('Training-set accuracy score: {0:0.4f}'.format(accuracy_score(y_train, y_pred_train_en)))
        print('Model accuracy score: {0:0.4f}'.format(accuracy_score(y_test, y_pred_en)))

        cm = confusion_matrix(y_test, y_pred_en)
        print('Confusion matrix\n\n', cm)

        f1score = f1_score(y_test, y_pred_en)
        print("F1 Score:", f1score)

        r2score = r2_score(y_test, y_pred_en)
        print("R2 Score:", r2score)

        score = classifier.score(X_test, y_test)
        print(score)
        # f, ax = plt.subplots(figsize=(10, 10))
        # sns.heatmap(cm, annot=True, linewidths=0.5, linecolor="red", fmt='.0f', ax=ax)
        # plt.savefig(f'0.6-{name}.png')

MachineLearning.export_trained_model()
