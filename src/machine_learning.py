import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier


class MachineLearning:

    @staticmethod
    def test_methods():
        MachineLearning.run_classifier(lambda: BaggingClassifier(estimator=DecisionTreeClassifier(criterion='entropy'), n_estimators=10), 'bagging-dte')
        MachineLearning.run_classifier(lambda: AdaBoostClassifier(estimator=DecisionTreeClassifier(criterion='entropy'), n_estimators=10), 'adaboost-dte')
        MachineLearning.run_classifier(lambda: RandomForestClassifier(), 'rf')  #
        MachineLearning.run_classifier(lambda: AdaBoostClassifier(estimator=RandomForestClassifier(), n_estimators=10), 'adaboost-rf')
        MachineLearning.run_classifier(lambda: BaggingClassifier(estimator=RandomForestClassifier(), n_estimators=10), 'bagging-rf')

    @staticmethod
    def export_trained_model():
        clf = MachineLearning.run_classifier(lambda: RandomForestClassifier(), 'rf')  #
        dump(clf, 'trained_model.joblib')

    @staticmethod
    def read_data():
        data = pd.read_csv('data.csv')

        X = data.drop(['dark_activity'], axis=1)
        X = pd.get_dummies(X)

        y = data['dark_activity']
        y = LabelEncoder().fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=27)
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
        print(f'\033[35m{name}\033[0m')
        print('Training-set accuracy score: {0:0.4f}'.format(accuracy_score(y_train, y_pred_train_en)))
        print('Model accuracy score: {0:0.4f}'.format(accuracy_score(y_test, y_pred_en)))

        cm = confusion_matrix(y_test, y_pred_en)
        print('Confusion matrix\n', cm)

        # f, ax = plt.subplots(figsize=(10, 10))
        # sns.heatmap(cm, annot=True, linewidths=0.5, linecolor="red", fmt='.0f', ax=ax)
        # plt.savefig(f'0.6-{name}.png')

MachineLearning.test_methods()
