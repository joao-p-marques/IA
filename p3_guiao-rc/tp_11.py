
from bayes_net import *

# Exemplo dos acetatos:

bn = BayesNet()

bn.add('st',[],0.60)
bn.add('pt',[],0.05)

bn.add('pa',[('pt',True )],0.25)
bn.add('pa',[('pt',False )],0.004)

bn.add('cnl',[('st',True )],0.90)
bn.add('cnl',[('st',False )],0.001)

bn.add('cp',[('st',True ),('pa',True )],0.02)
bn.add('cp',[('st',True ),('pa',False)],0.01)
bn.add('cp',[('st',False),('pa',True )],0.011)
bn.add('cp',[('st',False),('pa',False)],0.001)

bn.add('ur',[('pt',True )],0.90)
bn.add('ur',[('pt',False),('pa',True )],0.10)
bn.add('ur',[('pt',False),('pa',False)],0.01)

# conjunction = [('pa',True)]

# print(bn.jointProb(conjunction))

print(bn.indiv_prob('pa', True))

