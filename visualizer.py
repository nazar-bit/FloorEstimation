import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


#!!!!!  DO NOT USE IT CONFIDANTLY. I ASKED AI TO VIBE CODE THIS TO TEST SOMETHING  !!!!



# Your building polygon data
polygons = [[(np.float64(-743721.936), np.float64(-1048382.483), np.float64(263.539)), (np.float64(-743721.936), np.float64(-1048382.483), np.float64(265.965)), (np.float64(-743723.683), np.float64(-1048378.407), np.float64(265.965)), (np.float64(-743723.683), np.float64(-1048378.407), np.float64(263.539))], [(np.float64(-743718.135), np.float64(-1048380.854), np.float64(263.539)), (np.float64(-743718.135), np.float64(-1048380.854), np.float64(265.965)), (np.float64(-743721.936), np.float64(-1048382.483), np.float64(265.965)), (np.float64(-743721.936), np.float64(-1048382.483), np.float64(263.539))], [(np.float64(-743719.835), np.float64(-1048376.888), np.float64(263.539)), (np.float64(-743719.835), np.float64(-1048376.888), np.float64(265.965)), (np.float64(-743718.135), np.float64(-1048380.854), np.float64(265.965)), (np.float64(-743718.135), np.float64(-1048380.854), np.float64(263.539))], [(np.float64(-743723.683), np.float64(-1048378.407), np.float64(263.539)), (np.float64(-743723.683), np.float64(-1048378.407), np.float64(265.965)), (np.float64(-743719.835), np.float64(-1048376.888), np.float64(265.965)), (np.float64(-743719.835), np.float64(-1048376.888), np.float64(263.539))], [(np.float64(-743725.45), np.float64(-1048391.473), np.float64(241.284)), (np.float64(-743713.289), np.float64(-1048386.664), np.float64(241.284)), (np.float64(-743713.289), np.float64(-1048386.664), np.float64(263.539)), (np.float64(-743725.45), np.float64(-1048391.473), np.float64(263.539))], [(np.float64(-743713.289), np.float64(-1048386.664), np.float64(263.539)), (np.float64(-743713.289), np.float64(-1048386.664), np.float64(241.284)), (np.float64(-743720.26), np.float64(-1048369.037), np.float64(241.284)), (np.float64(-743720.26), np.float64(-1048369.037), np.float64(263.539))], [(np.float64(-743720.26), np.float64(-1048369.037), np.float64(241.284)), (np.float64(-743732.421), np.float64(-1048373.846), np.float64(241.284)), (np.float64(-743732.421), np.float64(-1048373.846), np.float64(263.539)), (np.float64(-743720.26), np.float64(-1048369.037), np.float64(263.539))], [(np.float64(-743731.561), np.float64(-1048393.801), np.float64(240.683)), (np.float64(-743725.45), np.float64(-1048391.473), np.float64(240.683)), (np.float64(-743725.45), np.float64(-1048391.473), np.float64(243.43)), (np.float64(-743731.561), np.float64(-1048393.801), np.float64(243.43))], [(np.float64(-743732.421), np.float64(-1048373.846), np.float64(240.683)), (np.float64(-743738.094), np.float64(-1048376.653), np.float64(240.683)), (np.float64(-743738.094), np.float64(-1048376.653), np.float64(243.43)), (np.float64(-743732.421), np.float64(-1048373.846), np.float64(243.43))]]

# Convert numpy floats to standard Python floats for matplotlib
poly_coords = [[(float(pt[0]), float(pt[1]), float(pt[2])) for pt in poly] for poly in polygons]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Create the 3D polygon collection
collection = Poly3DCollection(poly_coords, alpha=0.6, edgecolor='k')
collection.set_facecolor('skyblue')
ax.add_collection3d(collection)

# Extract coordinates for bounds and scaling
all_x = [pt[0] for poly in poly_coords for pt in poly]
all_y = [pt[1] for poly in poly_coords for pt in poly]
all_z = [pt[2] for poly in poly_coords for pt in poly]

ax.set_xlim(min(all_x), max(all_x))
ax.set_ylim(min(all_y), max(all_y))
ax.set_zlim(min(all_z), max(all_z))

ax.set_xlabel('X (S-JTSK)')
ax.set_ylabel('Y (S-JTSK)')
ax.set_zlabel('Z (Elevation)')
plt.title('Building Surfaces 3D View')

plt.show()