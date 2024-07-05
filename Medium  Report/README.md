We've now completed the first part of our experiment
I'll go through our code separately
In the compare_stop.py
We first imported the necessary libraries: 'csv', 'os', 'sys', 'panda as pd'
The file path is set with the code, as follows:
1. 'current_dir' is set to the directory path where the script is located.
2. 'project_root' is set as the parent directory path of 'current_dir'.
3. Add the parent directory (project root) to 'sys.path' so that the import takes place relative to the project root.
Then import the read_csv.
Then define a 'Stop' class with properties ('stop_id, name', 'latitude', 'longitude', 'zone_type').
Implement the __repr__ method in order to provide a printable representation of the object. Implement the '__eq__' method for equality comparisons based on instance variables. Implement the __lt__ method, which is used for stop_id-based comparisons, for sorting.
Finally, set 'csv_file_path' to the CSV file path containing the city's transit station data. Call the 'read_stops_from_csv' function to read data from the CSV file and return a list of 'Stop' instances.
Iterate through each Stop instance in the transport_stops list and print each instance using its __repr__ method
To summarize, we use object-oriented programming principles in our compare_stop.py to encapsulate data in a 'stop' class and utilize custom functions for data processing. It is used to read the city transit station data, and each stop is also represented as an instance of the 'Stop' class for further processing or analysis.

In the directed_graph.py
We first imported 'networkx' for network analysis and 'matplotlib', 'pyplot' for plotting, and 'pandas' for data processing.
A dictionary 'node_labels' is then defined to map the number of the node to the corresponding site name.
Once this is done, pandas is used to read two CSV files containing the latitude and longitude information of the stations (stops_df) and the distance between the stations (routes_df). Create a directed graph object 'G' and use 'DiGraph()' to indicate that this is a directed graph.
Nodes are then added using the data from the 'stops_df', each node is identified with the site ID and the latitude and longitude as the node attribute 'pos'. Add directed edges using the data from the routes_df, with the start and end nodes specified by the start_stop_id and end_stop_id, and the weights of the edges represented by distance.
Create a dictionary labels that maps each node to the corresponding site name, or the node ID if not defined.
Finally, use 'nx.get_node_attributes()' to get the node's location property 'pos'. Use the nx.draw() function to draw a directed graph, specifying the position of the nodes, whether to display the node labels, the content of the node labels, the node size, the node color, the font size and color, and the display of arrows. Use plt.title() to set the title of the diagram and display the graph via plt.show().
To summarize, in the directed_graph.py, we created and plotted a directed graph using NetworkX and Matplotlib to show the connections and distances between stations in the urban transportation network. It builds a graph structure by reading data from a CSV file, and presents visualizations using node location information and custom node labels.
In the read_csv.py
We first introduced 'os' for OS-related functions, such as getting file paths.
'sys' is used to add or adjust the module search path of the Python interpreter. 'pandas as pd' is used for data processing, in particular for reading and manipulating CSV files.
Second, use 'os.path.abspath(__file__)' to get the absolute path to the current script file.
The os.path.dirname() function is used to get the directory portion of the path.
'project_root' is set to the root directory of the project, which is the parent directory of the directory where the current script file is located.
'sys.path.append(project_root)' adds the project root to the system path to be able to import modules within the project.
Then import the ZoneType enumeration and the TransportStop class from the transportstop.py.
The 'read_stops_from_csv' function then accepts a parameter 'file_path' indicating the path of the CSV file to be read. Use 'pd.read_csv(file_path)' to read the contents of the CSV file and store them in the 'data' variable. Loop through each row of data to create an instance of the TransportStop object, converting each row of data into a property of the object. ZoneType[row['zone_type'].upper()] converts the value of the zone_type column to uppercase and sets the zone_type property based on the value enumerated by the ZoneType. If the file is not found, catch the 'FileNotFoundError' exception and print an error message, then return an empty list [].
Finally, store the path of the CSV file to be read in the 'csv_file_path' variable. The 'read_stops_from_csv(csv_file_path) function is called to store the returned list of site objects in the 'transport_stops' variable.
To summarize, in the directed_graph.py, we have converted the urban transit station data into objectified station information by using the 'pandas' library to read the CSV file data, combined with custom classes and enumeration types.

In the transportstop.py
Let's start by importing 'Enum' to define the enumeration type. 'Auto' automatically assigns values to enumerated members. 'csv' is used to read and write the module to the CSV file.
THEN FOUR ZONE TYPES ARE DEFINED BY THE 'ZONETYPE' ENUMERATION: 'RESIDENTIAL', 'COMMERCIAL', 'INDUSTRIAL', AND 'MIXED'. Use 'auto()' to automatically assign an incrementing value to each enumeration member.
A transit stop is represented by the 'TransportStop' class, with the attributes 'stop_id, name', 'latitude', 'longitude', and 'zone_type'. The __init__ method is used to initialize an object, where the zone_type must be an instance of the ZoneType enumeration type, otherwise a ValueError exception will be thrown. The __str__ method returns a string representation of the object, showing the ID, name, latitude and longitude, and zone type of the site. The '__repr__' method returns a detailed representation of the object for debugging and output. The __lt__ method defines the rules for comparison between objects, and the comparison is made in terms of the stop_id.
Have the read_transport_stops_from_csv function accept a filename, read the data from the CSV file and create a list of TransportStop objects. Use 'csv. DictReader 'to read the CSV file, with each row of data as a dictionary 'row'. Try to get the 'start_stop_id' (start station ID), 'end_stop_id' (end station ID), and 'distance' (distance' from 'row', and create a 'TransportStop' object and add it to the 'stops' list. If the value cannot be converted to an integer or floating-point number, the 'ValueError' exception is caught and an error message is printed.
Finally, in the main program, when the script is run directly, '(__name__ == "__main__")', the file name 'urban_transport_network_routes.csv' of the CSV file is specified, and the 'read_transport_stops_from_csv' function is called to get the list of site objects 'transport_stops'. Traverse the transport_stops list and print each site object, showing a string representation of the site (defined by the __str__ method).
To summarize, in the transportstop.py, we show how to use enumerations and classes to model station and area types in an urban transportation network, and create station objects by reading a CSV file. It also provides a foundational framework that can be further extended to process and analyze complex transportation network data.ji
# Urban-Transportation-Network-Analysis