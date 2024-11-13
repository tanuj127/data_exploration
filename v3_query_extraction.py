# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:32:42 2024

@author: TANUJ
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 18:39:07 2024

1. If there are double arrows, it means it's an inner join.
2. If there is only 1 arrow, it means it's either a left join or right join.
3. Join condition is mentioned on the edges.
4. Extract calculations such as aggregate functions like COUNT(), SUM(), etc.
5. Add calculated columns to the legend.

@author: TANUJ
"""
from sql_metadata import Parser
import re
import networkx as nx
import matplotlib.pyplot as plt

# Sample SQL query with calculations
str1 = '''
SELECT t1.NEW_HPANO,  count(t3.host_entry) as host_count 
FROM table_1 t1
LEFT JOIN table_2 t2 
ON t1.id = t2.cust_id
LEFT JOIN table_3 t3
ON t1.id = t3.host_id
LEFT JOIN table_4 t4
ON t1.id = t4.host_id
LEFT JOIN table_5 t5
ON t1.id = t5.id
INNER JOIN table_6 t6
ON t1.id = t6.id
INNER JOIN table_7 t7
ON t1.id = t7.id
Group by t1.NEW_HPANO
'''

# Initialize the parser
parser = Parser(str1)

# Extract tables and columns
tables = parser.tables
columns = parser.columns

# Dynamically create variables for tables
for i, table in enumerate(tables):
    globals()[f"table_{i+1}"] = table

# Dynamically create variables for columns
for i, column in enumerate(columns):
    globals()[f"column_{i+1}"] = column

# Extract calculations (aggregate functions, column aliases) using regex
calculation_info = []
calculation_patterns = [
    r"(\w+)\((\w+\.\w+)\)\s+as\s+(\w+)",  # Matches functions like COUNT(t3.host_entry) as host_count
    r"(\w+)\((\w+)\)\s+as\s+(\w+)",      # Matches functions like COUNT(id) as count_id
    r"(\w+)\s*\((.*?)\)\s+as\s+(\w+)",    # Matches functions with complex arguments
]

# Extracting the base table (first table in the FROM clause before any JOINs)
base_table = str1.split("FROM")[1].split("JOIN")[0].strip().split()[0]

# Search for calculation patterns in the query
for pattern in calculation_patterns:
    matches = re.finditer(pattern, str1, re.IGNORECASE)
    for match in matches:
        function = match.group(1)  # Aggregation function like COUNT, SUM
        column = match.group(2)    # Column name being operated on
        alias = match.group(3)     # Alias for the calculation (e.g., host_count)
        
        # Store calculation information
        calculation_info.append({
            "function": function,
            "column": column,
            "alias": alias
        })

# Print the extracted calculations (aggregate functions and aliases)
print("Extracted Calculations:")
for calc in calculation_info:
    print(calc)

# Create a directed graph to represent the direction of joins
G = nx.DiGraph()

# Identify join types and conditions using regex for joins
join_info = []
join_patterns = [
    r"(INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN|CROSS JOIN|JOIN)\s+(\w+)\s+(\w+)?\s*ON\s+(.+)",
]

# Extracting the base table (first table in the FROM clause before any JOINs)
for pattern in join_patterns:
    matches = re.finditer(pattern, str1, re.IGNORECASE)
    for match in matches:
        join_type = match.group(1)
        joined_table = match.group(2)
        alias = match.group(3) if match.group(3) else "N/A"
        join_condition = match.group(4)

        join_info.append({
            "base_table": base_table,
            "join_type": join_type,
            "joined_table": joined_table,
            "alias": alias,
            "join_condition": join_condition
        })

# Add nodes and edges based on join_info (same as before)
for join in join_info:
    n1 = join['base_table']
    n2 = join['joined_table']
    
    G.add_node(n1)
    G.add_node(n2)
    
    # Add directed edge for INNER JOIN
    if join['join_type'] == "INNER JOIN":
        G.add_edge(n1, n2, label=join['join_condition'], condition=join['join_condition'])
        G.add_edge(n2, n1, label=join['join_condition'], condition=join['join_condition'])
    else:
        G.add_edge(n1, n2, label=join['join_condition'], condition=join['join_condition'])

# Draw the graph with increased figure size
plt.figure(figsize=(14, 14))  # Increased figure size for better clarity
pos = nx.spring_layout(G, k=1.5, iterations=15)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=20, font_weight="bold", 
        arrows=True, width=2, arrowsize=20)

# Add edge labels (join conditions)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Prepare the legend for calculated columns
calculation_labels = [f"{calc['function']}({calc['column']}) as {calc['alias']}" for calc in calculation_info]

# Prepare the legend for regular columns
column_names = [f"Column: {column}" for column in columns]

# Combine both legends into one list
combined_labels = calculation_labels + column_names

# Display the combined legend in a single location
plt.legend(combined_labels, loc='upper right', fontsize=12, title="Columns and Calculations")

# Show the graph
plt.show()

# Print join info for debugging purposes
print("Join Information:")
for join in join_info:
    print(join)

# Print the calculation info for debugging purposes
print("Extracted Calculations:")
for calc in calculation_info:
    print(calc)
