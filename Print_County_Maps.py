#Example of QGIS/Python Functionalities
#This Python 2.7 example requires the attached Texas_Counties_QGIS_21824.qgs file.
#Guillermo Martinez
#An Evening of Python Coding, 10-16-2018

#QGIS libraries are already loaded in the QGIS/Python Console
import os;

#Figure out current path and set folder to store county maps
print(os.getcwd())
prjpath = QgsProject.instance().fileName()
print(prjpath)
outdir = os.path.dirname(prjpath)
print(outdir)

#List of selected Texas counties, add your favorite!
Counties =['Travis','Llano','Midland','Jefferson']

#Obtain instance of layer with county data
layer = QgsMapLayerRegistry.instance().mapLayersByName("Counties (Polygons)")[0]
print(layer.source())

#Check field names in the county data
for field in layer.fields():
    print(field.name(), field.typeName())

#Iterate through list and zoom at each county so we can save an save image.
for county in Counties:
    #Select county feature
    query =u'"CNTY_NM" = \'' + county + '\' '
    print(query)
    layer.selectByExpression(query, QgsVectorLayer.SetSelection)
    box = layer.boundingBoxOfSelected()
    layer.removeSelection()
    
    #Access predefined map, there is only one
    c = iface.activeComposers()[0].composition()
    
    #Access map element    
    map_item = c.getComposerItemById('Map')
    map_item.zoomToExtent(box)
    
    #Update test element
    text_item = c.getComposerItemById('Text County')
    text_item.setText(county + ' County')    
    
    #Save image
    image = c.printPageAsRaster(0)
    pathout = os.path.join(outdir,county + '.png')
    image.save(pathout,'png')  
print('Check for images in ' +outdir)