

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2018
# v1.81 - 2018/11/18
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

import collections

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:

    def __init__(self,ldecl=[]):
        self.declarations = ldecl

    def __str__(self):
        return my_list2string(self.declarations)

    def insert(self,decl):
        self.declarations.append(decl)

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result

    def query_local_assoc(self, entity, relation):
        local_decl = self.query_local(e1=entity, rel=relation)
        if local_decl and isinstance(local_decl[0].relation, AssocOne):
            counter = collections.Counter([l.relation.entity2 for l in local_decl])
            return [(e, c/len(local_decl)) for e, c in counter.most_common(1)]
        elif local_decl and isinstance(local_decl[0].relation, AssocNum):
            return sum([l.relation.entity2 for l in local_decl])/len(local_decl)
        else:
            counter = collections.Counter([l.relation.entity2 for l in local_decl])
            fsum = 0
            valfrq = []
            for e, c in counter.items():
                if fsum < 0.75:
                    valfrq.append((e, c/len(local_decl)))
                    fsum += c/len(local_decl)
            return valfrq
    
    def query_cancel(self, entity, rel=None):
        query_result = self.query_local(user=None, e1=entity, rel=rel, e2=None)
        if not self.predecessors(entity):
            self.query_result = query_result
            return query_result
        for pre in self.predecessors(entity):
            q = self.query_cancel(pre, rel=rel)
            # print(f'{pre} is predecessor of {entity}')
            for dec in q:
                # print(dec)
                if not (dec.relation.entity1, dec.relation.name) in [(d.relation.entity1, d.relation.name) for d in query_result]:
                    query_result.append(dec)
        self.query_result = query_result
        return self.query_result

    # def query_cancel(self, entity, relation=None):
    #     inherited = [self.query_cancel(d.relation.entity2, relation) for d in self.declarations if d.relation.entity1 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]

    #     local = [d for d in self.declarations if d.relation.entity1 == entity and (relation==None or d.relation.name == relation)]

    #     local_rels = [l.relation.name for l in local]

    #     return [item for sublist in inherited for item in sublist if not item.relation.name in local_rels] + local

    def query_down(self, entity, association):             
        descendents = [self.query_down(d.relation.entity1, association) for d in self.declarations if d.relation.entity2 == entity and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
                                                   
        return [item for sublist in descendents for item in sublist] + [d for d in self.declarations if d.relation.entity1 == entity and d.relation.name == association]

    def query_induce(self, entity, relation=None):
        declarations = self.query_down(entity, relation)
        most_common = collections.Counter(declarations).most_common()
        self.query_result = most_common
        return self.query_result

    def query(self, e1, rel=None):
        self.query_result = \
                [d for d in self.declarations
                        if (
                            (d.relation.entity1 == e1) 
                            or (d.relation.entity2 == e1) 
                            or (e1 in self.successors_path(d.relation.entity1))
                            or (e1 in self.successors_path(d.relation.entity2))
                        )
                        and (rel is None or d.relation.name == rel)]
        return self.query_result
    
    def query2(self, entity, rel=None):
        q = self.query(e1=entity, rel=rel)
        self.query_result = \
                [d for d in q
                        if (d.relation.entity1 == entity)
                        or (isinstance(d.relation, Association))]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        return list(set( [d.relation.name for d in self.declarations if isinstance(d.relation, Association)] ))

    def list_entities(self):
        return list(set( [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)] ))

    def list_users(self):
        return list(set([d.user for d in self.declarations]))

    def list_types(self):
        return list(set( 
            [d.relation.entity2 for d in self.declarations if 
                isinstance(d.relation, Member) or 
                isinstance(d.relation, Subtype) ] + 
            [d.relation.entity1 for d in self.declarations if 
                isinstance(d.relation, Subtype)] ))

    def list_associations_entity(self, entity):
        return list(set( [d.relation.name for d in self.declarations if 
            isinstance(d.relation, Association) and (
            d.relation.entity1 == entity or 
            d.relation.entity2 == entity ) ] ))

    def list_declarations(self, user):
        return list(set( [d.relation.name for d in self.declarations if d.user == user] ))

    def list_associations_user(self, user):
        return list(set( [d.relation.name for d in self.declarations if 
            isinstance(d.relation, Association) and
            d.user == user] ))

    def count_associations(self, user):
        return len(self.list_associations_user(user))

    def list_associatios_name_user(self, entity):
        return list(set( [ (d.relation.name, d.user) for 
            d in self.declarations if 
            isinstance(d.relation, Association) and (
            d.relation.entity1 == entity or 
            d.relation.entity2 == entity ) ] ))

    def successors(self, entity):
        ret = list(set( 
            [ d.relation.entity1 for d in self.declarations if 
                (isinstance(d.relation, Member) or isinstance(d.relation, Subtype)) and
                d.relation.entity2 == entity ] ))
        # print(f"Successors of {entity}: {ret}")
        return ret

    def predecessors(self, entity):
        ret = list(set( 
            [ d.relation.entity2 for d in self.declarations 
                if (isinstance(d.relation, Member) 
                    or isinstance(d.relation, Subtype)) 
                and d.relation.entity1 == entity ] 
            ))
        return ret

    def successors_path(self, entity):
        if not self.successors(entity):
            return []
        ret = self.successors(entity)
        for e in ret:
            ret += self.successors(e)
        # print(f"Successors_path of {entity}: {ret}")
        return ret

    def predecessor(self, entity1, entity2):
        return entity2 in self.successors(entity1)

    def predecessor_path(self, entity1, entity2):
        if entity1 == entity2:
            return [entity2]
        path = [entity1]
        for entity in self.successors(entity1):
            sub_path = self.predecessor_path(entity, entity2)
            if entity2 in sub_path:
                path += sub_path
        return path

# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

