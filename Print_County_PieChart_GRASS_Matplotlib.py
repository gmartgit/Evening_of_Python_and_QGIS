#Example of QGIS/Python Functionalities
#Create pie chart by county to show total developed area
#This Python 2.7 example requires the attached Texas_Counties_QGIS_21824_GRASS_plt.qgs file.
#Note Texas_Counties_QGIS_21824_GRASS_plt.qgs has a newly created layer of counties
# reprojected in the same coordinate system as the counties.
#Guillermo Martinez
#An Evening of Python Coding, 10-16-2018

#QGIS libraries are already loaded in the QGIS/Python Console
import os
import processing
import numpy as np
import matplotlib.pyplot as plt
import osgeo

#Figure out current path and set folder to store county maps
print(os.getcwd())
prjpath = QgsProject.instance().fileName()
print(prjpath)
outdir = os.path.dirname(prjpath)
print(outdir)

#List of selected Texas counties, add your favorite!
Counties =['Travis','Llano']

#Obtain instance of layer with county data in the same coordinate system as Land Use
#This step was done using qgis interface
layer = QgsMapLayerRegistry.instance().mapLayersByName("Counties reprojected")[0]
print(layer.source())

raster = QgsMapLayerRegistry.instance().mapLayersByName("Land Use (Raster)")[0]
print(raster.source())

#Checked Metadata to know Land Use  coordinate system 
crs = QgsCoordinateReferenceSystem(5070, QgsCoordinateReferenceSystem.EpsgCrsId)
temp_path =  os.path.join(outdir,'temp.shp')

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
    extstr ="%f,%f,%f,%f" %(box.xMinimum(), box.xMaximum(),box.yMinimum(), box.yMaximum()) 
    print(extstr)
    
    #clip raster to obtain detailed land use statistics
    outraster=os.path.join(outdir,county + '.tif')
    processing.runalg('saga:clipgridwithpolygon','Land Use (Raster)',layer,0,outraster)
    layer.removeSelection()
    
    #get raster statistics using GRASS, code generated Graphical Modeler (Processing Menu)
    outcsv = os.path.join(outdir,'temp.csv')
    processing.runalg('grass7:r.stats', outraster,',','NaN','255',False,False,True,False,False,False,False,False,False,False,False,False,False,extstr,None,outcsv)
    
    #Plot pie chart
    arr = np.genfromtxt(outcsv, delimiter=',')
    arr = arr[0:-1,:]
    dev = np.sum(arr[(arr[:,0] >= 21) &  (arr[:,0] <= 22)  , 1]) #area developed
    nodev = np.sum(arr[(arr[:,0] < 21) | (arr[:,0]  > 22)  , 1]) #area no developed
    fig, ax = plt.subplots(figsize=(8,4))
    ax.pie([dev, nodev],  labels=['Developed','No developed'],colors=['red','gray'],autopct='%1.1f%%',textprops={'fontsize': 18});
    ax.axis('equal');
    ax.set_title(county)
    plt.savefig(os.path.join(outdir,county + '_pie.png'))
    plt.close(fig)
    
    
print('Check for pie charts in ' +outdir)