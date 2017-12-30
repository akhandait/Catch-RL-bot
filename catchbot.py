import tensorflow as tf
import catch
import pickle

#hyperparameters
H = 200 #number of hidden layer neurons
batch_size = 100 # after how many episodes to do a parameter update
# define what is an episode 
learning_rate = 1e-4 
gamma = 0.99 # discount factor for reward
decay_rate = 0.99 # ?
resume = False
render = False

# model initialization
D = 160 * 120 # input grid
if resume:
	model = pickle.load(open('save.p', 'rb'))
else:
    model = {}
    model['W1'] = np.random.randn(H, D) / np.sqrt(D)	
    model['W2'] = np.random.randn(H) / np.sqrt(H)

grad_buffer = {k : np.zeros_like(v) for k,v in model.items()}
rmsprop_cache = {k : np.zeros_like(v) for k,v in model.items()}    
	
def sigmoid(x):
	return 1.0/(1.0 + np.exp(-x))

def preprocess(A):
    # preprocess 800x600x3 uint frame into 160x120
    A = A[::5, ::5, 0] # downsample by a factor of 4
    A[A==106] = 0 # erase background
    return A.astype(np.float).ravel()

def discount_reward(r):
    # take 1D float array of rewards and compute discounted reward
    discounted_r = np.zeros_like(r)

def policy_forward(x):
    h = np.dot(model['W1'], x)    
    h[h<0] = 0 # ReLU nonlinearity
    logp = np.dot(model['W2'], h)
    p = sigmoid(logp)
    return p, h # return probability of taking action right, and hidden state
    
def policy_backward(eph, epdlogp):
    # backward pass (eph is an array of intermediate hidden states)
    dW2 = np.dot(eph.T, epdlogp).ravel()
    dh = np.outer(epdlogp, model['W2'])
    dh[eph <= 0] = 0 
    dW1 =     




