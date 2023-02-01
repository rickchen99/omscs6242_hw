########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "xchen864"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id int,title text,score real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast(movie_id int,cast_id int,cast_name text,birthday text,popularity real)"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]

    
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        
       ######################################################################
        movie_insertion_sql = "INSERT INTO movies (id,title,score) VALUES(?,?,?)"
        movie_cast_insertion_sql = "INSERT INTO movie_cast (movie_id,cast_id,cast_name,birthday,popularity) VALUES(?,?,?,?,?)"
       
        with open("data/movies.csv",'rt') as csvfile:
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                #print(line[1])
                
                #print(line[1])
                connection.execute(movie_insertion_sql,(line[0],line[1],line[2]))               
                connection.commit()
        
        #import to movie_cast table
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)                                                                                                                                                                                                                                                                                                                                                                                                                             
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        
        ######################################################################
        #import to movie_cast table
        movie_cast_insertion_sql = "INSERT INTO movie_cast (movie_id,cast_id,cast_name,birthday,popularity) VALUES(?,?,?,?,?)"
        with open("data/movie_cast.csv",'rt') as csvfile1:
            
            csv_reader1 = csv.reader(csvfile1)
            for line in csv_reader1:
                #print(line)
                connection.execute(movie_cast_insertion_sql,(line[0],line[1],line[2],line[3],line[4]))               
                connection.commit()    
        print('-----select statement-----')
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    
    def part_aiii(self,connection):
        #print('test')
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio(cast_id int,cast_name text,birthday text,popularity real);"
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = """
        insert into cast_bio
        select distinct cast_id,cast_name,birthday,popularity from movie_cast
        
        """
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        
        cursor = connection.execute(sql)
        
        return(cursor.fetchall()[0][0])
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "create  index movie_index on movies(id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "create  index cast_index on movie_cast(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "create  index cast_bio_index on cast_bio(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """with war_score8_movies as (select count(*) as count 
                        from movies 
                        where title 
                        like('%war%') and score > 50)
                        select printf("%.2f",round(cast (war_score8_movies.count as real)*100/ cast (count(id) as real),2))
                        from  war_score8_movies,movies

        """
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = """select cast_name,count(cast_id)
                        from movie_cast
                        where popularity > 10 
                        group by cast_name
                        order by count(cast_id) desc,cast_name asc 

                        limit 5
                    """
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """
                    select movie.title,printf("%.2f",score),count(cast_id)
                    from movies movie inner join movie_cast cast
                    on movie.id = movie_id
                    group by title
                    order by score desc,count(cast_id) asc
                    limit 5
                    """

        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """
                    select movie_cast.cast_id,movie_cast.cast_name, printf("%.2f",avg(movies.score))
                    from movie_cast 
                    inner join movies 
                    on movie_cast.movie_id = movies.id
                    where movies.score>=25 
                    group by movie_cast.cast_name
                    
                    having count(movie_cast.cast_name)>2
                    order by avg(movies.score) desc,movie_cast.cast_name asc
					limit 10

                    """
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """
       CREATE view good_collaboration as 
	   
		  with movie_collab as (
                    select DISTINCT m1.cast_id as cast1, m2.cast_id as cast2,score,movies.id
                    from movie_cast m1
                    inner join movie_cast m2
                    using(movie_id)
                    inner join movies on m1.movie_id = movies.id
                    where m1.cast_id < m2.cast_id
					)
		

			SELECT cast1,cast2,count(distinct id) as movie_count,avg(score) as new_score
			from movie_collab
			group by cast1,cast2
			having count(distinct id ) >=3
			and avg(score)>=40

        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """
                    with cast1_avg as 
                    (
                        select cast1 as id,cast_name,printf("%.2f",avg(new_score)) as avg_score
                        from good_collaboration
                        INNER JOIN movie_cast
                        on cast1 = cast_id
                        GROUP by cast1
                    ),
                    cast2_avg as 
                    (
                        select cast2 as id,cast_name,printf("%.2f",avg(new_score)) as avg_score
                        from good_collaboration
                        INNER JOIN movie_cast
                        on cast2 = cast_id
                        GROUP by cast2
                    )
                    SELECT *
                    from cast1_avg
                    UNION
                    select *
                    from cast2_avg
                    order by avg_score DESC,cast_name asc
limit 5
        """
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "create virtual table movie_overview using fts4(id,overview)"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        part_h_insertion_sql = 'insert into movie_overview(id,overview) values(?,?)'
        with open("data/movie_overview.csv",'rt') as csvfile:
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                connection.execute(part_h_insertion_sql,(line[0],line[1]))               
                connection.commit()
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "select count(*) from movie_overview where overview match 'FIGHT'"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "select count(*) from movie_overview where overview match 'space NEAR/5 program'"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
