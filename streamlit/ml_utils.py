import pickle

def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def predict_gravity(model, X_df):
    return model.predict(X_df)[0]
