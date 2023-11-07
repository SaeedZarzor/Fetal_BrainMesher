#!/opt/homebrew/bin/Python3.10
# change the directory above #
######################################

from readers.Importer import ImportFromFile
from point_cloud.PointCloud import PointCloud
from mesh.Mesh import Mesh
from writers.Writer import Writer
from writers import aseg_manipulate
import configparser, sys, os

configFilePath = sys.argv[1]
config = configparser.ConfigParser()
if configFilePath.split(".")[-1] != "ini":
    configFilePath = configFilePath.split(".")[0] + ".ini"

config.read(configFilePath)
curr_config = config['DEFAULT']
file_in_path = curr_config.get("file_in_path")
file_in_name = curr_config.get("file_in")

file_in_name_no_ext = file_in_name.split(".")[0]

# Getting output file directory
file_out_path = "/".join([file_in_path, file_in_name_no_ext])
if not os.path.exists(file_out_path):
    os.mkdir(file_out_path)

curr_config["file_out_path"] = file_out_path

fileout = file_in_name_no_ext + "_mesh"
curr_config["fileout"] = fileout
f = open("/".join([file_out_path, fileout + "_log"]) + ".txt", 'w')

# Importing data from mri images
importer = ImportFromFile(curr_config.get("file_in_path"), curr_config.get("file_in"))
data = importer.getData()
f.write("Reading file: " + "/".join([curr_config.get("file_in_path"), curr_config.get("file_in")]) + "\n")

# Creating binary image based on binary threshold set in config file
threshold = curr_config.getfloat("binary_threshold")
f.write("Binary threshold: " + str(threshold) + "\n")
print("Creating cleaned voxel images")
print("Binary threshold set at", threshold)
dimensions = data.shape
for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        for z in range(dimensions[2]):
            if data[x,y,z] >= threshold:
                data[x,y,z] = 1
            else:
                data[x, y, z] = 0

# Creating point cloud from images
pointCloud = PointCloud()
pointCloud.create_point_cloud_from_voxel(data)

# Creates mesh from point cloud
print("Creating mesh")
mesh = Mesh()
mesh.create_mesh_from_Point_Cloud(pointCloud.pcd, 1)

# Smooths mesh
if curr_config.getboolean("smooth"):
    iterations = curr_config.getint('iterations')
    smooth_co_effs = [float(x.strip()) for x in curr_config.get("co_effs").split(",")]
    mesh.smooth_mesh(smooth_co_effs, iterations)

# Writing mesh into specified file types
types_string = curr_config.get('fileout_types')
types = [x.strip() for x in types_string.split(",")]
print("Writing data to", file_out_path)
for t in types:
    writer = Writer()
    writer.openWriter(t, fileout, file_out_path)
    writer.writeMeshData(mesh)
    writer.closeWriter()
    f.write("New {} file written to \n".format(t, file_out_path + fileout).replace("\\", "/"))

for keys in curr_config:
    f.write(keys + ": " + curr_config.get(keys) + "\n")
f.write("Model creation complete")
f.close()

# Creating .ii image of cleaned mri using chosen binary threshold
aseg_manipulate.create_aseg(file_in_path, file_in_name, file_out_path, data)
