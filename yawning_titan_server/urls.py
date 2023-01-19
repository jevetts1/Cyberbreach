from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from yawning_titan_gui.views import (
    GameModeConfigView,
    GameModesView,
    HomeView,
    DocsView,
    NetworksView,
    config_file_manager,
    NodeEditor
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("docs/",DocsView.as_view(),name="docs"),
    path("game_modes/", GameModesView.as_view(), name="Manage game modes"),
    path("networks/", NetworksView.as_view(), name="Manage networks"),
    path(
        "game_mode_config/<str:game_mode_file>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path(
        "game_mode_config/<str:game_mode_file>/<str:section>/",
        GameModeConfigView.as_view(),
        name="game mode config",
    ),
    path("game_mode_config/", GameModeConfigView.as_view(), name="game mode config"),
    path("manage_files/", config_file_manager, name="file manager"),
    path("node_editor/", NodeEditor.as_view(), name="node editor"),
]
