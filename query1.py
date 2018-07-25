import json
import os
from py2neo import Graph,Path,authenticate,Node,Relationship,NodeSelector

def create_user_node():

	authenticate("localhost:7474","neo4j","qwertyuiop")
	g = Graph()

	a = open('dataset.json')

	data = json.load(a)

	i=0

	for key,value in data.items():

		i=i+1

		u = Node("User",screen_name=value['author_screen_name'])
		t=Node("Tweet", tid = value['tid'])
		rel= Relationship(u,"POSTS",t)

		g.merge(u)
		g.merge(t)
		g.merge(rel)

		if(value['mentions'] is not None):

			for ment in value['mentions']:

				if(len(ment)>0):

					u2 = Node("User", screen_name=ment)
					rel = Relationship(t,"MENTIONS",u2)
					g.merge(u2)
					g.merge(rel)

		if(value['hashtags'] is not None):
				
			for hstg in value['hashtags']:
					
				if(len(hstg)>0):
					h = Node("Hashtag",hashtag=hstg)
					rel = Relationship(t,"HAS_HASH",h)
					g.merge(h)
					g.merge(rel)



	print(i)
    
create_user_node()






''' 
 Query1:-

        match(u1:User)-[:POSTS]->(t:Tweet)-[:MENTIONS]->(u2:User) 
        return u1.screen_name as User1,u2.screen_name as User2,Collect(t.tid) as Tid,
        Count(*) as Total_Mnt_count order by Total_Mnt_count DESC LIMIT 10;

 Query8:-

       match(u:User)-[:POSTS]->(t:Tweet)-[:HAS_HASH]->(h:Hashtag)
       where h.hashtag=\'%s\' return h.hashtag as Hashtag,u.screen_name as User,Collect(t.tid) as Tid,count(*) as Tweet_count
       order by Tweet_count Desc LIMIT 3 

'''