"""
Author: Tarun Ambati
Last updated: July 26, 2026
Description: Imports Engineering faculty information from an Excel file,
stores professor records in a dictionary, builds the School of Engineering
program tree, and launches the faculty visualizer.
"""

import pandas as pd

from professor import Professor
from faculty_visualizer import FacultyVisualizer
from tree_node import TreeNode
from preferences import Preferences

class ENGR_Faculty:
    def __init__(self):
        
        # Dictionary containing the faculty nodes
        # Keys are last names, values are Professors
        self.faculty_dict = self.import_faculty()

        # Tree representing the Engineering faculty
        self.program_structure = self.build_structure()

        # Visualize the faculty tree
        self.visualizer = FacultyVisualizer(
            self.program_structure, self.faculty_dict)

        
    def import_faculty(self):
        """ Reads the Excel file containing the faculty member information
            and adds them to the faculty dictionary """
        
        # The dictionary to store the faculty
        faculty_dict = {}

        # Read the Excel file into a pandas data frame
        df = pd.read_excel(Preferences.FACULTY_FILE)

        # Add each row of the data frame (professor) to the dictionary
        df.apply((lambda x: self.add_prof(x, faculty_dict)), axis=1)

        return faculty_dict


    def add_prof(self, prof, faculty_dict) -> None:
        """Create a Professor object and add it to the faculty dictionary.

        The prof argument is one row from the pandas DataFrame. Its name,
        program, rank, and office fields are used to create a Professor.
        The Professor is then stored in faculty_dict using the professor's
        last name as the key.
        """
        professor = Professor(
            prof["FirstName"],
            prof["LastName"],
            prof["Rank"],
            prof["Program"],
            prof["Office"]
        )

        faculty_dict[professor.last_name] = professor


    def build_structure(self) -> TreeNode:
        """Build and return the School of Engineering faculty tree.

        The root node represents the School of Engineering. Each program
        is added as a child of the root, and each professor is added as a
        child of the program that matches their Professor.Program value.
        Faculty nodes store the related Professor object as their data so
        the visualizer can display names, information, and headshots.
        """

        # We are all under the School of Engineering
        root = TreeNode("School of Engineering", TreeNode.NodeType.SCHOOL)
        program_nodes = {}
        
        # Create a node for each SoE program
        for program in Professor.Program:
            program_node = TreeNode(program.value, TreeNode.NodeType.PROGAM)
            root.add_child(program_node)
            program_nodes[program] = program_node

        for professor in self.faculty_dict.values():
            faculty_node = TreeNode(
                professor.last_name,
                TreeNode.NodeType.FACULTY,
                professor
            )
            program_nodes[professor.program].add_child(faculty_node)

        return root


    def visualize_faculty(self):
        """ Build and show the tree visualizing the faculty """
        self.visualizer.run()
        

if __name__ == '__main__':
    f = ENGR_Faculty()
    f.visualize_faculty()