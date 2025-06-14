# Ce fichier corrige un problème de compatibilité en supprimant une option obsolète dans la configuration du modèle .h5.
# Il permet son chargement avec une version plus récente de Keras.
import h5py
f = h5py.File("keras_model.h5", mode="r+")
model_config_string = f.attrs.get("model_config")
if model_config_string.find('"groups": 1,') != -1:
    model_config_string = model_config_string.replace('"groups": 1,', '')
    f.attrs.modify('model_config', model_config_string)
    f.flush()
    model_config_string = f.attrs.get("model_config")
    assert model_config_string.find('"groups": 1,') == -1

f.close()
