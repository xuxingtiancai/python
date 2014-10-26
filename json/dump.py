#dump json

import json
 
obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
print json.dumps(obj, separators=(', ',': '))
obj = {1:2}
print json.dumps(obj)
obj = (1,2)
print json.dumps(obj)
