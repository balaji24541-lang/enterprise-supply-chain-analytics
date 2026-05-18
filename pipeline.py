import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

print("🏁 Script has officially started initialized...")

def run_enterprise_pipeline():
    raw_data_path = "data/DataCoSupplyChainDataset.csv"
    output_data_path = "data/supply_chain_predictions.csv"
    
    print(f"🔍 Checking workspace directory...")
    if not os.path.exists(raw_data_path):
        print(f"❌ Error: Looked for '{raw_data_path}' but it wasn't there.")
        return

    try:
        print("📦 [1/4] Loading DataCo Supply Chain Records into memory...")
        df = pd.read_csv(raw_data_path, encoding="latin1")
        print(f"✅ Successfully loaded data! Shape: {df.shape}")

        # HOTFIX: Changed 'Customer Region' to 'Order Region' to match DataCo Schema
        target_columns = [
            'Days for shipping (real)', 'Days for shipment (scheduled)', 
            'Delivery Status', 'Category Name', 'Order Region', 
            'Order Item Quantity', 'Sales', 'Order Item Profit Ratio', 'Shipping Mode'
        ]
        df = df[target_columns].dropna()

        print("⚙️ [2/4] Engineering Advanced Operational & Risk Features...")
        df['Scheduled_Transit_Window'] = df['Days for shipment (scheduled)']
        df['Order_Density'] = df['Order Item Quantity'] * df['Sales']
        df['Is_Delayed'] = np.where(df['Delivery Status'] == 'Late delivery', 1, 0)

        # HOTFIX: Updated categorical encoder target to 'Order Region'
        categorical_features = ['Order Region', 'Shipping Mode', 'Category Name']
        df_encoded = pd.get_dummies(df, columns=categorical_features, drop_first=True)

        print("🧠 [3/4] Initializing ML Engine (Random Forest)...")
        features_to_drop = ['Days for shipping (real)', 'Delivery Status', 'Is_Delayed']
        X = df_encoded.drop(columns=features_to_drop)
        y = df_encoded['Is_Delayed']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        print("\n" + "="*20 + " SYSTEM PERFORMANCE MATRIX " + "="*20)
        print(classification_report(y_test, y_pred))
        print(f"Validated Model ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
        print("="*67 + "\n")

        print("📊 [4/4] Mapping Predictive Output to Financial Risk Framework...")
        df['Delay_Probability'] = model.predict_proba(X)[:, 1]
        df['Revenue_At_Risk'] = df['Delay_Probability'] * df['Sales']
        df['Net_Profit'] = df['Sales'] * df['Order Item Profit Ratio']

        df.to_csv(output_data_path, index=False)
        print(f"🚀 Pipeline Complete! Output written to: {output_data_path}")

    except Exception as e:
        print(f"💥 CRASH DETECTED! Error details: {str(e)}")

run_enterprise_pipeline()