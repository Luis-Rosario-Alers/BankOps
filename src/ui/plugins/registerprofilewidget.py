from profile_widget import QProfileButton
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

TOOLTIP = "A cool wiggly widget (Python)"
DOM_XML = """
<ui language='c++'>
    <widget class='QProfileButton' name='ProfileButton'>
    </widget>
</ui>
"""

# TODO: add function that automatically adds widgets

QPyDesignerCustomWidgetCollection.registerCustomWidget(
    QProfileButton,
    module="src/ui/plugins.profile_widget",
    tool_tip=TOOLTIP,
    xml=DOM_XML,
    container=False,
    group="Custom Widgets",
)
