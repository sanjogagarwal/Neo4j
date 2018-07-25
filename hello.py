# -*- coding: utf-8 -*-
import json
import os
from py2neo import Graph,Path,authenticate,Node,Relationship,NodeSelector

from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask (__name__)

#fun var

	
@app.route("/")
def index():

	return render_template('test.html')


@app.route("/query1" , methods = ['POST','GET'])
def query1():
	user = request.form['query1']
	
	authenticate("localhost:7474","neo4j","qwertyuiop")
	g = Graph()

	a = g.data("""match (u1:User)<-[:MENTIONS]-(t:Tweet)-[:MENTIONS]-(u2:User)
       			 where u1.screen_name='%s'
       			return u1.screen_name as User1,u2.screen_name as User2,
       			Collect(t.tid) as Tid,count(*) as co_mentioncount Order by co_mentioncount DESC"""%user)	
	
	
	page = " <style> table, th, td { border: 1px solid black; } </style>"

	page = page + "<table> <tr> <th> Mentioned_User1 </th> <th> Mentioned_User2 </th> <th> Tid's </th>  <th> Total_Mentions </th> </tr> "

	for row in a:
	
		page = page + "<tr> "
		page += "<td> %s </td>" % repr(json.dumps(row['User1']))
		page += "<td> %s </td>" % repr(json.dumps(row['User2']))
		page += "<td> %s </td>" % repr(json.dumps(row['Tid']))
		page += "<td> %s </td>" % repr(json.dumps(row['co_mentioncount']))
		page += "</tr>"

	
	
	page += "</table>"
	page=page+"<img src=\"/static/graph_query1.png\" width=1000px height=700px >"
	return page






@app.route("/query8" , methods = ['POST','GET'])
def query8():
	hashtag = request.form['query8']
	
	authenticate("localhost:7474","neo4j","qwertyuiop")
	g = Graph()

	a = g.data("""match(u:User)-[:POSTS]->(t:Tweet)-[:HAS_HASH]->(h:Hashtag)
       where h.hashtag=\'%s\' return h.hashtag as Hashtag,u.screen_name as User,Collect(t.tid) as Tid,count(*) as Tweet_count
       order by Tweet_count Desc LIMIT 3 """%hashtag)	
	
	
	page = " <style> table, th, td { border: 1px solid black; } </style>"

	page = page + "<table> <tr> <th> Hashtag </th> <th> User </th> <th> Tid's </th>  <th> Tweet_Count </th> </tr> "

	for row in a:
	
		page = page + "<tr> "
		page += "<td> %s </td>" % repr(json.dumps(row['Hashtag']))
		page += "<td> %s </td>" % repr(json.dumps(row['User']))
		page += "<td> %s </td>" % repr(json.dumps(row['Tid']))
		page += "<td> %s </td>" % repr(json.dumps(row['Tweet_count']))
		page += "</tr>"

	
	page += "</table>"
	
	page=page+"<img src=\"/static/graph_query8.png\" width=1000px height=700px >"
	return page


if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 8007)