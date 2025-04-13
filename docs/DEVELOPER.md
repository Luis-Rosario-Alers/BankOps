# **Important things to know** ❗

### how to import custom plugins to QT Designer

1. Go into your IDE

2. Start a terminal session

3. Input one of the following

**Linux/Mac**

`
export PYSIDE_DESIGNER_PLUGINS=/path/to/repo/src/ui/plugins
`

**Windows/Powershell**

`
$Env:PYSIDE_DESIGNER_PLUGINS = "/path/to/repo/src/ui/plugins"
`

After setting the environment variable

run `pyside6-designer` in your terminal to use our custom widgets.
