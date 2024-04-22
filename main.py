import re
import glob

def convertSCSS2CSS(rawDatas):

    keyList = []
    keyString = ''
    keyFlag = False

    cssObj = {}

    for data in rawDatas:
        keyFlag = False
        if data == '\n' or data == ' ' or data == '\t':
            continue

        if re.match(r'^\s*//', data):
            continue

        for char in data:
            
            if re.match(r'^\s{4,}[\.#&]', data) or re.match(r'^[\.#&]', data):
                keyFlag = True
            
            if char == '{':
                keyFlag = False
                keyList.append(keyString.replace(' ', ''))
                keyString = ''
                continue

            if char == '}':
                keyFlag = False
                if len(keyList) > 0:
                    keyList.pop()
                keyString = ''
                continue

            if keyFlag:
                keyString += char
                continue
            else:
                if len(keyList) > 0:
                    key = ' '.join(keyList).replace(' &', '')
                    cssObj[key] = cssObj.get(key, '') + char

    css = ''
    for key, value in cssObj.items():
        css += key.replace('\n', '') + '{' + value.replace('\n', '').replace("    ", "") + '}'

    return css

def fileAnalyze(path):
    with open(path, 'r') as f:
        text = f.read()
    
    rawDatas = text.split('\n')

    html = []
    controller = []
    css = []

    typeCode = 0
    for data in rawDatas:
        if re.match(r'^<html', data):
            typeCode = 1
            continue
        if re.match(r'^</html', data):
            typeCode = 0
        if re.match(r'^<controller', data):
            typeCode = 2
            continue
        if re.match(r'^</controller', data):
            typeCode = 0
        if re.match(r'^<scss', data):
            typeCode = 3
            continue
        if re.match(r'^</scss', data):
            typeCode = 0

        if typeCode == 1:
            html.append(data)
        if typeCode == 2:
            controller.append(data)
            if len(controller) == 1:
                controller[0] = "controller: " + controller[0]
        if typeCode == 3:
            css.append(data)

    return html, controller, css

def componentName(fname):
    for char in fname:
        if char.isupper():
            fname = fname.replace(char, '-' + char.lower())

    return fname

components = {}

files = glob.glob('components/*.ng')

for path in files:
    fName = path.replace('.ng', '')
    html, controller, css = fileAnalyze(path)
    name = componentName(fName)
    components[fName] = {
        'name': name,
        'template': html,
        'controller': controller,
        'css' : css
    }

cssfName = 'prod/result.css'
cssFile = open(cssfName, 'w')

with open('prod/result.js', 'w') as f:
    f.write("window.components = {\n")
    
    for fName, data in components.items():
        f.write(f"{fName}: {{\n")
        f.write(f"template: `\n")
        for line in data['template']:
            f.write(line + '\n')
        f.write("`,\n")
        f.write(f"controllerName: \"ctrl-" + data['name'] + "\",\n")
        for line in data['controller']:
            f.write(line + '\n')
        f.write("},\n")
        
        cssFile.write(convertSCSS2CSS(data["css"]) + '\n')
    
    f.write("};")