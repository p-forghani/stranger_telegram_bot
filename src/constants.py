from types import SimpleNamespace

from utils.keyboard import create_keyboard

keys = SimpleNamespace(
    random_connect=":busts_in_silhouette: Random Connect",
    settings = ":gear: Settings",
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.settings)
)