from py2neo import Graph, Node, Relationship, cypher, Path


# import neo4j


class Neo4j():
    graph = None

    def __init__(self):
        print("create neo4j class ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="Trueshn1022")

    # 返回所有实体和关系
    def searchAll(self):
        sql = "MATCH (e1:Title)-[r]-(e2) RETURN e1.name,e2.name,r.name"
        res = self.graph.run(sql).data()
        return res

    # 根据文章名返回实体及关系
    def searchByTitle(self, title, level):
        sql_1 = "MATCH p=(n:Title)-[*1..1]-(m)where n.name=~{title} RETURN extract(x IN relationships(p)) as rels"
        sql_2 = "MATCH p=(n:Title)-[*1..2]-(m)where n.name=~{title} RETURN extract(x IN relationships(p)) as rels"
        sql_3 = "MATCH p=(n:Title)-[*1..3]-(m)where n.name=~{title} RETURN extract(x IN relationships(p)) as rels"
        title = ".*" + title + ".*"
        data = {'title': title}
        res = {}
        if level == '1':
            res = self.graph.run(sql_1, data).data()
        elif level == '2':
            res = self.graph.run(sql_2, data).data()
        elif level == '3':
            res = self.graph.run(sql_3, data).data()
        return res

    # 根据关键词返回实体及关系
    def searchByKeyword(self, keyword, level):
        sql_1 = "MATCH p=(n:Keyword)-[*1..1]-(m)where n.name=~{keyword} RETURN extract(x IN relationships(p)) as rels"
        sql_2 = "MATCH p=(n:Keyword)-[*1..2]-(m)where n.name=~{keyword} RETURN extract(x IN relationships(p)) as rels"
        sql_3 = "MATCH p=(n:Keyword)-[*1..3]-(m)where n.name=~{keyword} RETURN extract(x IN relationships(p)) as rels"
        keyword = ".*" + keyword + ".*"
        data = {'keyword': keyword}
        res = {}
        if level == '1':
            res = self.graph.run(sql_1, data).data()
        elif level == '2':
            res = self.graph.run(sql_2, data).data()
        elif level == '3':
            res = self.graph.run(sql_3, data).data()
        return res

    # 根据关键词返回实体及关系
    def searchByAuthor(self, author, level):
        sql_1 = "MATCH p=(n:Author)-[*1..1]-(m)where n.name=~{author} RETURN extract(x IN relationships(p)) as rels"
        sql_2 = "MATCH p=(n:Author)-[*1..2]-(m)where n.name=~{author} RETURN extract(x IN relationships(p)) as rels"
        sql_3 = "MATCH p=(n:Author)-[*1..3]-(m)where n.name=~{author} RETURN extract(x IN relationships(p)) as rels"
        author = ".*" + author + ".*"
        data = {'author': author}
        res = {}
        if level == '1':
            res = self.graph.run(sql_1, data).data()
        elif level == '2':
            res = self.graph.run(sql_2, data).data()
        elif level == '3':
            res = self.graph.run(sql_3, data).data()
        return res

    # 根据算法分类返回文章
    def searchTitleByAlgorithm(self, algorithm=''):
        sql = "MATCH p=(n:Algorithm)-[*1..1]-(m:Title) where n.name=~{algorithm} " \
              "RETURN extract(x IN relationships(p)) as rels"
        algorithm = ".*" + algorithm + ".*"
        data = {'algorithm': algorithm}
        res = self.graph.run(sql, data).data()
        return res

    # def matchItembyTitle(self, value):
    #     sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
    #     answer = self.graph.run(sql).data()
    #     return answer
    #
    # # 根据title值返回互动百科item
    # def matchHudongItembyTitle(self, value):
    #     sql = "MATCH (n:HudongItem { title: '" + str(value) + "' }) return n;"
    #     answer = self.graph.run(sql).data()
    #     return answer
    #
    # # 根据entity的名称返回关系
    # def getEntityRelationbyEntity(self, value):
    #     answer = self.graph.run(
    #         "MATCH (entity1:Keyword) - [rel] -> (entity2:Title)  WHERE entity1.name = \"" + str(
    #             value) + "\" RETURN rel,entity2").data()
    #     return answer
    #
    # # 查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
    # def findRelationByEntity(self, entity1):
    #     answer = self.graph.run(
    #         "MATCH (n1:LoreEntity1 {title:\"" + str(
    #             entity1) + "\"})- [rel] -> (n2:LoreEntity2) RETURN n1,rel,n2").data()
    #     # if(answer is None):
    #     # 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
    #     return answer
    #
    # # 查找entity2及其对应的关系
    # def findRelationByEntity2(self, entity1):
    #     answer = self.graph.run(
    #         "MATCH (n1:LoreEntity2 {title:\"" + str(
    #             entity1) + "\"})- [rel] -> (n2:LoreEntity1) RETURN n1,rel,n2").data()
    #
    #     # if(answer is None):
    #     # 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
    #     return answer
    #
    # # 根据entity1和关系查找enitty2
    # def findOtherEntities(self, entity, relation):
    #     answer = self.graph.run(
    #         "MATCH (n1:LoreEntity1 {title:\"" + str(entity) + "\"})- [rel {type:\"" + str(
    #             relation) + "\"}] -> (n2:LoreEntity2) RETURN n1,rel,n2").data()
    #     # if(answer is None):
    #     #	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
    #
    #     return answer
    #
    # # 根据entity2和关系查找enitty1
    # def findOtherEntities2(self, entity, relation):
    #     answer = self.graph.run("MATCH (n1:LoreEntity2)- [rel {type:\"" + str(relation) +
    #                             "\"}] -> (n2:LoreEntity1 {title:\"" + str(entity) + "\"}) RETURN n1,rel,n2").data()
    #     # if(answer is None):
    #     #	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()
    #
    #     return answer
    #
    # # 根据两个实体查询它们之间的最短路径
    # def findRelationByEntities(self, entity1, entity2):
    #     answer = self.graph.run(
    #         "MATCH (p1:LoreEntity1 {title:\"" + str(entity1) + "\"}),(p2:LoreEntity2{title:\"" + str(
    #             entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel").evaluate()
    #     # answer = self.graph.run("MATCH (p1:LoreEntity1 {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()
    #
    #     if (answer is None):
    #         answer = self.graph.run(
    #             "MATCH (p1:LoreEntity1 {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\"" + str(
    #                 entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
    #     if (answer is None):
    #         answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:HudongItem{title:\"" + str(
    #             entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
    #     if (answer is None):
    #         answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\"" + str(
    #             entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
    #     # answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
    #     # if(answer is None):
    #     #	answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
    #     # if(answer is None):
    #     #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
    #     # if(answer is None):
    #     #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
    #     relationDict = []
    #     if (answer is not None):
    #         for x in answer:
    #             tmp = {}
    #             start_node = x.start_node
    #             end_node = x.end_node
    #             tmp['n1'] = start_node
    #             tmp['n2'] = end_node
    #             tmp['rel'] = x
    #             relationDict.append(tmp)
    #     return relationDict
    #
    # # 查询数据库中是否有对应的实体-关系匹配
    # def findEntityRelation(self, entity1, relation, entity2):
    #     answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
    #         relation) + "\"}] -> (n2:HudongItem{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
    #     if (answer is None):
    #         answer = self.graph.run(
    #             "MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
    #                 relation) + "\"}] -> (n2:NewNode{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
    #     if (answer is None):
    #         answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
    #             relation) + "\"}] -> (n2:HudongItem{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
    #     if (answer is None):
    #         answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
    #             relation) + "\"}] -> (n2:NewNode{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
    #
    #     return answer
