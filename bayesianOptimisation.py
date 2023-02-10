import json
import shutil

import sympy as sy
from bayes_opt import BayesianOptimization
from bayes_opt.event import Events
from bayes_opt.logger import JSONLogger
from bayes_opt.util import load_logs
from bayes_opt.util import UtilityFunction

import display

JSONDir = "C:\\SABYDOMA Data\\bayes\\"
logger = JSONLogger(path = JSONDir + "logs.json")

def initOptimizer(bounds_JSON,kappa,xi):
    global optimizer
    global utility
    global pbounds

    pbounds = json.loads(bounds_JSON)
    
    optimizer = BayesianOptimization(
        f=None,
        pbounds=pbounds,
        verbose=2,
        random_state=1,
    )

    optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)

    utility = UtilityFunction(kind="ucb", kappa=kappa, xi=xi)

    return 0

def setBounds(bounds_JSON):
    bounds_body = json.loads(bounds_JSON)
    optimizer.set_bounds(new_bounds=bounds_body)
    return 0

def registerPoint(register_JSON):
    register_body = json.loads(register_JSON)
    optimizer.register(
                params=register_body["params"],
                target=register_body["target"],
            )
    return 0
    
def suggestNextPoint():
    next_point = optimizer.suggest(utility)
    return json.dumps(next_point)

def getOptimizerMax():
    return json.dumps(optimizer.max)

def getOptimizerSpace():
    return json.dumps(optimizer.space.res())

def saveSpace(filename):
    shutil.copyfile(JSONDir + "logs.json", JSONDir + "\\saved\\" + filename + ".json", follow_symlinks = True)
    return

def backupSpace(filename):
    shutil.copyfile(JSONDir + "logs.json", JSONDir + "\\saved\\backup\\" + filename + ".json", follow_symlinks = True)
    return

def loadSpace(filename):
    load_logs(optimizer, logs = JSONDir + "\\saved\\" + filename + ".json")
    return

def plotGP():
    optimizer.suggest(utility) # calling the suggest function fits the gp
    display.setGrid(pbounds, 20)
    display.getTargetsFromGP(optimizer)
    display.contourPlot(optimizer)
    return 0

def target_function(x, y):
    expr = sy.sympify(selfFunction)
    return expr.evalf(subs={"x": x, "y": y})

def selfMaximise(functionString,bounds_JSON,init_points,n_iter,kappa,xi):
    global selfFunction
    selfFunction = functionString
    
    selfOptimizer = BayesianOptimization(
        f=target_function,
        pbounds=json.loads(bounds_JSON),
        verbose=2,
        random_state=1,
    )

    selfOptimizer.maximize(
        init_points=init_points,
        n_iter=n_iter,
        kappa=kappa,
        xi=xi,
    )

    display.setGrid(json.loads(bounds_JSON), 50)
    display.getTargetsFromFunc(target_function)
    display.contourPlot(selfOptimizer)

    return 0