import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(file_path):

    df = pd.read_csv(file_path)

    df_numeric = df.select_dtypes(include=['int64','float64'])

    model = IsolationForest(contamination=0.05, random_state=42)

    df['anomaly'] = model.fit_predict(df_numeric)

    df['anomaly'] = df['anomaly'].map({1:'Normal', -1:'Anomaly'})

    anomalies = df[df['anomaly']=="Anomaly"]
    normal = df[df['anomaly']=="Normal"]

    total = len(df)

    return df, anomalies, normal, total