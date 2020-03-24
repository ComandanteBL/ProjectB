import time

from keras.engine.saving import model_from_json

from utils.queries import save_model_to_db, load_best_model_from_db


def save_model(model, rmse):
    # SAVE MODEL TO DISK
    unix_time = int(time.time())  # unit time appended to name of settings and weights
    model_json = model.to_json()  # serialize model to JSON
    with open(f"../models/model-{unix_time}.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights(f"../models/model-{unix_time}.h5")  # serialize weights to HDF5

    # SAVE MODEL TO DB
    save_model_to_db(f'model-{unix_time}', '../models/', rmse)

    print(f"'model-{unix_time}' saved!")


def load_model(model_name=None, symbol=None, model_type=None):
    # LOAD MODEL FROM DB

    df = load_best_model_from_db(symbol, model_type)
    db_model_name = df['name'][0]
    db_model_path = df['path'][0]
    db_model_rmse = df['rmse'][0]

    # LOAD FILES AND CREATE MODEL
    json_file = open(f'{db_model_path}{db_model_name}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(f"{db_model_path}{db_model_name}.h5")
    print(f"'{db_model_name}' loaded! RMSE: {db_model_rmse}")
    return loaded_model
