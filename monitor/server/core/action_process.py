
import pickle 
import serialize
def action_process(server_instance,msg):
    
    msg = pickle.loads(msg[2])
    #print msg
    func_name = msg.keys()[0]
    func = getattr(serialize,func_name)
    
    func(server_instance,msg[func_name])
   
    #server_instance.redis.set('10.168.66.92', 'test')

