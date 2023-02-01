import http.client
import json
import csv
import ast
from urllib import request
from wsgiref.util import request_uri


#############################################################################################################################
# cse6242 
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################


imdb_connection = http.client.HTTPConnection("api.themoviedb.org")
"""
imdb_connection.request("GET","/3/movie/550?api_key=7cef50f36914f58fcdace9fb6a37c7e5&language=en-US")
r1 = imdb_connection.getresponse()
print(r1.status, r1.reason)
if r1.status == 200:
    data1 = r1.read()
print(data1)
"""
class Graph:
    
    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        new_node = (id,name)
        if new_node not in self.nodes:
            self.nodes.append((id,name))
            print(f'{new_node} has been added')
        else:
            print(f"debugger: node {new_node} exsit in current graph")


    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        new_edge = (source,target)
        new_edge_reverse = (target,source)
        #generate a list only contain id for comparison
        temp_id_list = [item[0] for item in self.nodes]
         
        if new_edge not in self.edges and source != target:
            if new_edge_reverse not in self.edges and target != source:
                self.edges.append(new_edge)
            else:
                print(f'reversed edge found : {new_edge_reverse}')
        elif source not in temp_id_list:
            print(f'source node {source} not found in the graph ')
        elif target not in temp_id_list:
            print(f'target node {target} not found in the graph ')
        else:
            print(f'edge found : {new_edge}')
        


    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)


    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)


    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        temp_id_list = [item[0] for item in self.nodes]
        #temp_counter = 0
        edge_count_dict = {}
        for node in temp_id_list:
            edge_count_dict[node] = 0
        
        for edges in self.edges:
            for node in temp_id_list:
                if node in edges:
                    edge_count_dict[node] = edge_count_dict[node] + 1
        
        #print(temp_id_list)

        max_edges = max(edge_count_dict.values())
        max_node = {key for key, value in edge_count_dict.items() if value == max_edges }
        max_node_dict={}
        for item in max_node:
            max_node_dict[item] = max_edges
        return max_node_dict

    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)

    def return_k_nodes(self):
        temp_counter = 0
        degree_count = 0
        for node in self.nodes:
            for edge in self.edges:
                if (node[0] is edge[0]) or (node[0] is edge[1]):
                    degree_count = degree_count + 1
                    #print(degree_count)
                    if degree_count>=2:
                        temp_counter=temp_counter+1
                        degree_count=0
        return temp_counter


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")

class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key
       # print(f"initiation done, api key is {self.api_key}")


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """
        #https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=<<api_key>>&language=en-US
        if movie_id != 939258:
            request_url = f"/3/movie/{movie_id}/credits?api_key={self.api_key}&language=en-US"
        else:
            return None
        #print(request_url)
        imdb_connection.request("GET",request_url)
        raw_data = imdb_connection.getresponse()
        print(raw_data.status, raw_data.reason)
        if raw_data.status == 404:
            print(f'movie id is {movie_id}')
            print(f'limit is {limit}')
            print(f'exclude_id is  {exclude_ids}')
            return None

        elif raw_data.status == 200:
            decoded_data= json.loads(raw_data.read())
            #need to clean data, only cast are needed
            cast_data = decoded_data['cast']
            if limit is not None:
                for cast in cast_data.copy():              
                    if cast.get('order') >=limit:                   
                        cast_data.remove(cast)
            if exclude_ids is not None:
                for ids in exclude_ids:
                    for cast in cast_data.copy():
                        if ids == cast.get('id'):
                            cast_data.remove(cast)
            return cast_data
        elif raw_data.status != 200:
            print(f'movie id is {movie_id}')
            print(f'limit is {limit}')
            print(f'exclude_id is  {exclude_ids}')
            return None
        

        ''' e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]'''
        
        #filter out all with value more than the limit


        #if len(cast_data)> limit:
         #   print("more cast than limit after exclusion and limit filtering")
          #  print(cast_data)
        
   


    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        request_url = f'/3/person/{person_id}/movie_credits?api_key={self.api_key}&language=en-US'
        imdb_connection.request("GET",request_url)
        person_raw_data = imdb_connection.getresponse()
        #print('------------------------')
        #print(person_raw_data.status, person_raw_data.reason)
        if person_raw_data.status == 200:
            person_data= json.loads(person_raw_data.read())
            #only saving the cast data
            person_cast_data = person_data['cast']
        #now clean for the vote avg
        if vote_avg_threshold is not None:
            for cast in person_cast_data.copy():
                if 'vote_average' not in cast:
                    person_cast_data.remove(cast)
                elif cast.get('vote_average') < vote_avg_threshold:
                    person_cast_data.remove(cast)
                
        #print(person_cast_data)
        return person_cast_data


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# GRAPH SIZE
# With each iteration of your graph build, the number of nodes and edges grows approximately at an exponential rate.
# Our testing indicates growth approximately equal to e^2x.
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We establish a bound for lowest & highest encountered numbers of nodes and edges with a
# margin of +/- 100 for nodes and +/- 150 for edges.  e.g., The allowable range of nodes is set to:
#
# Min allowable nodes = min encountered nodes - 100
# Max allowable nodes = max allowable nodes + 100
#
# e.g., if the minimum encountered nodes = 507 and the max encountered nodes = 526, then the min/max range is 407-626
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return 'xchen864'


def return_argo_lite_snapshot()->str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return 'https://poloclub.github.io/argo-graph-lite/#b2cc91cd-47b5-447b-a8a1-188a3011ea20'

def base_movie_list_generator(og_node):
    movie_list = []
    for records in og_node:
        movie_list.append(records.get('id'))
    return movie_list

def base_graph_generator(movie_list,tmdb_api_utils,graph,self_person_id):
    temp_node_counter = 0

    for ids in movie_list:
        print(f'movie id is {ids}')
        if ids != 939258:
            this_movie_cast = tmdb_api_utils.get_movie_cast(ids,3,self_person_id)
            for cast_member in this_movie_cast:
                temp_id = str(cast_member.get('id'))
                temp_name = cast_member.get('name')
                graph.add_node(id=temp_id,name=temp_name)
                #print(f'succeussfully added {temp_name} with id {temp_id}')
                graph.add_edge(source=self_person_id,target=temp_id)
                temp_node_counter = temp_node_counter + 1
                #print(f'node count is {temp_node_counter}')
    return graph

def graph_main_generator_rebuilt(tmdb_api:TMDBAPIUtils,base_graph:Graph,new_graph:Graph):


    #print(f'node list {base_graph.nodes[:][0]}')
    for cast_member_node in base_graph.nodes:
        member_cast_id = cast_member_node[0]
        #return movies with this cast member hae avg score > 8.0
        #print(f'node size is {len(base_graph.nodes)}')
        movie_credit_data = tmdb_api.get_movie_credits_for_person(person_id=member_cast_id,vote_avg_threshold=8.0)
        # return a list of movie ids
        movie_id_list = base_movie_list_generator(movie_credit_data)
        for movie_ids in movie_id_list:
            related_casts = tmdb_api.get_movie_cast(movie_ids,3)
            for cast_member in related_casts:
                temp_id = str(cast_member.get('id'))
                temp_name = cast_member.get('name')
                temp_name_refined = temp_name.replace(',','')
                print(f'actor id : {temp_id} name :{temp_name_refined}') 
                new_graph.add_node(temp_id,temp_name_refined)
                new_graph.add_edge(member_cast_id,temp_id)
        
        
        
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK

def graph_main_generator(tmdb_api:TMDBAPIUtils,graph:Graph):
    temp_node_counter = 0
    temp_nodes = graph.nodes
    for i in range(0,2,1):
        #kind of recalling itself here!!
        if i == 0 :
            
            for cast_node in temp_nodes:
                ###
                og_node = tmdb_api.get_movie_credits_for_person(person_id=cast_node[0],vote_avg_threshold=8.0)
                temp_movie_list = base_movie_list_generator(og_node)
                print('-------------')
                print(f'size of nodes is {len(temp_nodes)}')
                """
                for movie_ids in temp_movie_list.copy():
                    other_casts = tmdb_api.get_movie_cast(movie_id=movie_ids,limit=3,exclude_ids=cast_node[0])
                    if other_casts is not None :
                        for cast_member in other_casts:
                            print(cast_member)
                            temp_node_counter = temp_node_counter + 1
                            temp_id = str(cast_member.get('id'))
                            temp_name = cast_member.get('name')  
                            #print(type(temp_id))
                            #print(type(temp_name)) 
                            graph.add_node(id=temp_id,name=temp_name) 
                            #graph.add_edge(source=cast_node[0],target=temp_id)                    
                            

                            
                            #print(f'succeussfully added {temp_name} with id {temp_id}')
                            
                            temp_node_counter = temp_node_counter + 1
                            print(f'node count is {temp_node_counter}')
                    else:
                        temp_movie_list.remove(movie_ids)    """                

        else:
            # nodes = The nodes added in the previous iteration:
            break
        """
        for cast_node in temp_nodes:
            print(cast_node)
            og_node = tmdb_api.get_movie_credits_for_person(person_id=cast_node[0],vote_avg_threshold=8.0)
            temp_movie_list = base_movie_list_generator(og_node)
            print(temp_movie_list)
            for movie_ids in temp_movie_list.copy():
                other_casts = tmdb_api.get_movie_cast(movie_id=movie_ids,limit=3,exclude_ids=cast_node[0])
                if other_casts is not None :
                    for cast_member in other_casts:
                        print(cast_member)
                        temp_node_counter = temp_node_counter + 1
                        temp_id = str(cast_member.get('id'))
                        temp_name = cast_member.get('name')  
                        #print(type(temp_id))
                        #print(type(temp_name)) 
                        graph.add_node(id=temp_id,name=temp_name) 
                        #graph.add_edge(source=cast_node[0],target=temp_id)                    
                        

                        
                        #print(f'succeussfully added {temp_name} with id {temp_id}')
                        
                        temp_node_counter = temp_node_counter + 1
                        print(f'node count is {temp_node_counter}')
                else:
                    temp_movie_list.remove(movie_ids)
                #print(other_casts)
            #base_graph_generator(temp_movie_list,tmdb_api,graph,cast_node[0])
            #temp_counter = temp_counter + 1
            #print(f'loop for movie id {cast_node} done')
            """
    return None    


    
    
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH

# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":
    graph = Graph()
    graph.add_node(id='2975', name='Laurence Fishburne')
    tmdb_api_utils = TMDBAPIUtils(api_key='7cef50f36914f58fcdace9fb6a37c7e5')
    # example api request https://api.themoviedb.org/3/movie/550?api_key=7cef50f36914f58fcdace9fb6a37c7e5&language=en-US
    # call functions or place code here to build graph (graph building code not graded)
    # Suggestion: code should contain steps outlined above in BUILD CO-ACTOR NETWORK

    #tmdb_api_utils.get_movie_cast(movie_id='12921',limit=5)
    LF_og_node = tmdb_api_utils.get_movie_credits_for_person(person_id='2975',vote_avg_threshold=8.0)
    print(LF_og_node)
    movie_id_list = base_movie_list_generator(LF_og_node)
    print(movie_id_list)
    base_nodes =base_graph_generator(movie_id_list,tmdb_api_utils,graph,'2975')
    base_nodes.print_nodes()
    #graph_main_generator(tmdb_api_utils,graph)
    new_graph = Graph()
    #new_graph.print_nodes
    graph_main_generator_rebuilt(tmdb_api_utils,base_nodes,new_graph = new_graph)
    #base_nodes.print_nodes()
    #new_graph.write_nodes_file()
    #new_graph.write_edges_file()
    new_graph2 = Graph()
    graph_main_generator_rebuilt(tmdb_api_utils,new_graph,new_graph = new_graph2)
    graph = new_graph2
   
    new_graph2.write_nodes_file()
    new_graph2.write_edges_file()
    print(new_graph2.return_k_nodes())

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")
