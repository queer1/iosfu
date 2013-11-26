from importlib import import_module

from iosfu.utils import slugify
from .components.base import GUIPanel


class GUIController(object):
    """
    Object that store and control all the UI compoennts.
    """

    _panels = {}
    _sections = {}
    _categories = {}

    def register_panel(self, panel_component):
        """
        Decorator to register GUIPanels.
        """
        ins = panel_component()
        assert isinstance(ins, GUIPanel), "{}.{} is not a GUIPanel insance"\
            .format(ins.__module__, panel_component.__name__)
        slug = ins.__slug__

        # Append panel to instance manager
        self._panels[slug] = panel_component

        # Category handling
        category = slugify(ins.category)
        if ins.category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(slug)

    def load_from_library(self, library):
        """
        Loads all available GUI modules from plugins loaded by the library.
        """
        for k, plugin in library.plugins.items():
            plugin_module = plugin.__module__
            gui_module = "{0}.{1}".format(
                plugin_module.rsplit('.', 1)[0],
                'gui'
            )
            try:
                import_module(gui_module)
            except ImportError as error:
                # Plugin with no GUI module.
                print(error)

    def load_panel(self, panel_id):
        """
        Returns the given GUIPanel instance.
        """
        if panel_id in self._panels:
            return self._panels[panel_id]()
