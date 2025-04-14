from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from src.ui.plugins.widgets.profile_widget import QProfileButton

TOOLTIP = "A cool wiggly widget (Python)"
DOM_XML = """
<ui language='c++'>
    <widget class='QProfileButton' name='ProfileButton'>
    </widget>
</ui>
"""

# TODO: add function that automatically adds widgets


def addCustomWidgets() -> None:
    QPyDesignerCustomWidgetCollection.registerCustomWidget(
        QProfileButton,
        module="src/ui/plugins/widgets.profile_widget",
        tool_tip=TOOLTIP,
        xml=DOM_XML,
        container=False,
        group="Custom Widgets",
    )


addCustomWidgets()
# This is a placeholder for the actual implementation of the custom widgets function.
